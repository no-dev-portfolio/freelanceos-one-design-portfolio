# CR-002 実行・分類・検証の詳細契約 v0.11

設計候補。実装なしの整合性検討であり動作実証ではない。本文正本はMarkdown、Cloud既定OFF。以下の契約はAPI_CONTRACT/DATA_MODEL/SCREEN_SPECと同時に扱う。

## 1. 分類・派生物・最終送信（R2-01）

分類はpublic < personal < confidential < restricted。unknown/欠落/由来不明は送信不可。sourceの有効分類は本文観測、DB権限、policyの最も厳しいもの。初期profileは**一度でも非public又はunknown入力に触れたjob全体をCloud不可**とする。jobのtaintは単調で、入力を削除・要約・匿名化しても低下しない。これは誤送信を避ける保守的な仕様で、分類引下げ機能は初期対象外。

派生物はartifact_id/content_hash/source_artifact_ids/source_hashes/effective_classification/policy_revision/job_taintを持つ。要約、prompt、tool結果、Embedding、export、ログ、再添付を同じ由来関係で追跡する。scope/ACLは元データより広げない。親jobからforkする場合も由来・taintを継承する。由来が欠落した外部fileを「public」と自己申告しただけではpublicへ採用しない。明示的なsource審査を経た独立のpublic入力以外はunknown扱い。既存秘密jobからの内容再包装を自動で分類引下げしない。

### 送信準備と同意
1. Provider adapterが送信bodyを最後まで構築する。system prompt、会話履歴、tool定義・結果、添付、モデル指定等、内容を持つ全要素を分類判定に含める。サービス用固定promptもpublic送信可能版として登録していなければdeny。
2. immutable egress envelopeにdestination_origin/path、provider、固定model_id、adapter/schema版、body_hash、attachment_hashes、content_headers、source依存hash、policy_revision、purpose、budget_reservation_id、expires_atを保持する。body_hashは最終UTF-8 bytes、添付は実送信bytesを対象とする。
3. 人間へ送信内容/宛先/目的/由来/機密区分をpreviewし、consentをenvelope_hashへ束縛する。認証tokenはpreview/監査へ含めない。固定transport認証・request-id等は内容を変えないallowlist項目だけ、別のsecret参照として管理する。adapterが同意後に本文・添付・会話・endpoint・modelを変えたら旧consentを失効し、envelope再生成・再同意。
4. 実送信直前にenvelope/body/添付hash、現在policy/ACL/失効、consent期限・取消、taint、費用予約を照合する。publicかつ全条件一致の場合のみ発注。redirect、自動provider fallback、内容を変えるretryは許可しない。非publicはlocal経路又はBlocked。
5. 送信と取消の境界は「送信claim」のDB確定で直列化。claim前取消は未送信を止める。claim後は実送信の結果が不明でも回収可能と表示せずOutcomeUnknown/既送信可能性を示す。network送信をDB transactionと原子的とは仮定しない。自動再送で二重処理しない。

payload原文を監査へ複製せずhashと最小摘要を記録する。localからの画像取得・描画・exportもegress対象としCONTENT_PRESENTATIONの初期遮断規則を適用。実通信の実証は実装後のTEST-AI-009。

## 2. 不変jobの再開と訂正（R2-02）

jobは実行開始時にexecution_manifest（入力hash、plan版/hash、model/prompt/tool版、scope、policy版、知識依存note/hash/検証hash/epoch）を凍結する。resumeはこのmanifestを変えない障害継続だけ。入力・plan・tool/modelを訂正する場合はPOST /jobs/{id}/forkで新jobへ分岐し、元jobを改変しない。新jobの計画と必要承認は新規に審査する。

| step kind | resumeでの扱い | forkでの扱い |
|---|---|---|
| pure（計算・検索・生成） | 成功結果はfingerprintと現在ACL/失効/証拠が一致する場合だけ再利用。変化すればBlocked→forkを案内 | 初期profileは旧計算結果を自動再利用せず再計算。旧出力は履歴参照だけ |
| effect（書込・送信・確定export） | 成功operationを再送しない。不明なら照合まで停止 | 元operation/effect_keyをledger参照で継承。同一論理副作用を新jobだからと再送しない |

fingerprintはstep入力、plan、model/prompt/tool、依存hash/検証版/policyを含む。同一入力のworker再起動でも、現在の失効や権限を再検査する。policyが変われば不変resume条件を満たさずBlocked。再計画はforkへ。

副作用は系譜を跨ぐeffect_ledger（logical_effect_key、origin_operation_id、owner、target、status、external_ref）を正本に照合する。forkによるkey再採番で不確定・完了済み副作用を迂回しない。新たな作用を意図する場合は旧作用と影響を人間へ提示し、別目的・別actionの明示承認を要求する。不明作用の存在中は同じtarget/論理作用の自動実行禁止。履歴の成功と再利用可能を別表示する。

結果保持を求めるREQ-UX-002と副作用再送禁止REQ-AI-005は維持する。古い計算を再利用し続けることを「保持」と解釈しない。実装後はTEST-AI-008/UX-002/KB-011で訂正・失効・並列再開を検証する。

## 3. 候補の技術検証と証拠採用（R2-03）

登録済みclaim_kind/scopeとsuiteの対応に限定する初期profile。汎用AIの自己採点だけではVerifiedへ進めない。claim_id、assertion_type、対象hash、適用条件を明示し、試験が主張の範囲をカバーするかを登録registryで照合する。登録にない主張はreviewedのまま保留し、技術実証済みと表示しない。

### validation operation
- request: candidate_id又はnote_id、expected_content_hash、claim_id、assertion_type、scope、suite_id/version、dataset_ref/hash、expected_state_version。
- response: validation_id、operation_id、status、target_hash、suite/version、evidence_refs、next_actions。
- 状態: Requested→Running→Passed/Failed/TimedOut/Cancelled。本文・scope・suite・出典/証拠失効はEvidenceStale。Passedは試験成功であってVerified採用ではない。
- runner identityは許可された検証service。固定架空datasetとallowlisted suiteのみ実行し、任意shell/networkなし。runnerはvalidation recordと不変evidence（target_hash/suite/dataset/scope/result/実行条件/hash）を発行する。user/LLMが「passed」と入力してもrunner証拠へ変換しない。
- 採用権限はownerの人間。採用APIでPassed、対象hash、scope適合、suite現行許可、証拠内容/由来/期限、出典失効、reviewed状態、expected versionを確定的gateで再確認。knowledge_validations作成とverified状態反映とauditを同一DB transactionにする。人間承認だけでも、runner成功だけでも昇格しない。
- 採用前に本文が変わったらEvidenceStaleとして拒否。後の本文変更・source失効・suite撤回・期限切れは検証を無効化し、公開gateも停止する。再検証は新validation_id、旧証拠を上書きしない。

assertion_typeはtechnical_fact/procedure/preference。旧表記technical-factは移行入力の別名としてdry-runでtechnical_factへ明示mappingし、未知値を自動採用しない。preferenceは本人確認でhuman_attestedとして表示し、技術Verifiedや技術回答根拠と同一扱いしない。

SCR-03/05で「検証を依頼」→SCR-08で対象/試験/結果→SCR-07で「証拠を採用」→SCR-05で対象hashと適用範囲を表示。失敗/timeoutはReviewed維持、修正は新候補へ。権限不足/未知suite/旧hash/不適合は理由を表示して戻せる。実装後のKB-004/012/EVAL-002で昇格と失効を確認する。

## 4. 実装前の机上ケース（期待する設計上の帰結）

以下は仕様の適用結果を文書上で確認したもの。runtime合格ではない。

| ID | 入力・操作 | 規則上の帰結 | 実装後TEST |
|---|---|---|---|
| D-01 | public依頼+confidentialノート→local要約→Cloud | job taint継承、送信不可 | AI-009.a |
| D-02 | 機密を削った要約を同jobでpublic指定 | taint低下なし、送信不可 | AI-009.b |
| D-03 | export→再添付、由来不明 | unknownとして送信不可 | AI-009.c |
| D-04 | 全public、同意後adapterが会話追加 | body/envelope hash変化、旧同意失効 | AI-009.d |
| D-05 | 同意後provider/model変更 | 新envelope/再同意 | AI-009.e |
| D-06 | 同意取消が送信claim前/後 | 前は停止、後は送信済み可能性と照合 | AI-009.f |
| D-07 | 同一入力・同一manifestでworker再起動 | 現依存一致時のみpure再利用、effect再送なし | AI-008.a |
| D-08 | 成功後に入力/plan/tool訂正 | resume 409、fork、旧pure結果自動再利用なし | AI-008.b |
| D-09 | 依存ノートが失効した後resume | Blocked、失効を除くforkへ | KB-011.a |
| D-10 | 不明副作用を持つjobからfork | ledger継承、同じ作用は照合まで停止 | AI-008.c |
| D-11 | 知識候補を人が承認しただけ | Reviewed、技術Verifiedにはしない | KB-004.a |
| D-12 | Passed証拠が旧hash/別scope/別suite | 採用拒否、EvidenceStale又は不適合 | KB-012.a |
| D-13 | 正しいsuite/対象hash、ownerが採用 | gate一致時のみVerified候補、原子的採用を要求 | KB-004.b |
| D-14 | 証拠発行中に本文変化 | 旧証拠採用不可、新validationへ | KB-012.b |
| D-15 | preferenceの本人確認 | human_attested、技術Verifiedとは別表示 | EVAL-002.a |

比較案・費用/新リスク・移行はCR-002。選択の効果や実装の正しさは実装後の試験で確認する。

## 補足：作用keyとsuite管理の権限

logical_effect_keyはPolicy serviceがlineage_root/target_ref/effect_type/business_operation_refから生成し、agent/clientが任意keyで元作用を隠せない。forkは旧系譜とledger参照を必須化する。別目的の新作用は旧作用との差と影響を明示承認し、不明な同対象作用が残る間は保守的にBlockedとする。

suite registryの更新はownerによる変更管理/版管理の対象で、agent/runnerにはsuiteの許可範囲を広げる権限を与えない。suite版・claim scope・datasetの変更は新registry版、影響するvalidationを再検査する。試験成功は宣言したscopeだけを裏付け、SQL製品全般の正しさを実証したと拡大解釈しない。


## 初期suite registryの設計例（未実装・未登録）

| suite候補 | claim / assertion_type | 証拠が裏付ける範囲 | 裏付けないこと |
|---|---|---|---|
| demo-rowcount-fixture-v1 | 特定fixtureの件数差 / technical_fact | 同じ入力hashのsource/target件数と差、runner版、期待値との一致 | 他の入力・実DB全体・SQL移行全般の正しさ |
| demo-rowcount-playbook-v1 | 件数差を調べる限定手順 / procedure | 登録した開発用架空ケース群/環境/ツール版で手順が期待結果に達する | 未見問題での性能/時間短縮、別環境への無条件一般化 |

上記はschema/適用範囲を確認する例で、実行可能suiteやPassed証拠は存在しない。登録/runnerの実装後に試験し、満たさなければ昇格しない。validation用fixtureは開発用に分離し、成長評価のholdout正解/証拠を通常agentやmemoryへ渡さない。

## CR-003 local可用性の前提

主要ペルソナの顧客由来jobはlocal-onlyを前提にする。単調taintは維持し、Cloudへの自動fallbackや匿名化による引下げを追加しない。localの成立性はFEASIBILITY_SPIKESの事前固定候補（件数/正答/待時間/メモリ）でI前に調査し、TEST-AI-002.localで統合後再試験。閾値の人間採用と実測は未了。