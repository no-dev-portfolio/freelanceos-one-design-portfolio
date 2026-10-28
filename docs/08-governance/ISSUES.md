# 未解決Issue / リスクレジスター

| ID | 重大度 | 未解決事項 | 必要な証拠 | 予定ゲート |
|---|---|---|---|---|
| ISSUE-001 | Critical | MacのVault同時編集/競合時の具体的なatomic write | Obsidian実機PoC、障害注入 | G2 |
| ISSUE-002 | Critical | 知識削除後のキャッシュ/索引/バックアップ整合 | 削除シナリオ・保持ポリシー | G3 |
| ISSUE-003 | High | 未見問題で記憶が本当に有効か | 記憶A/B評価データと結果 | G4 |
| ISSUE-004 | High | 重要承認が利用者の負担にならないか | タスク観察、所要時間 | G1 |
| ISSUE-005 | High | Macローカルモデルの性能/メモリ/費用 | 実機ベンチマーク | G4 |
| ISSUE-006 | High | UIアクセシビリティと日本語フォント | 手動/自動試験 | G1 |
| ISSUE-007 | High | バックアップ・復旧時のRPO/RTO・秘密保持 | 復元訓練と文書化 | G3 |
| ISSUE-008 | Medium | Obsidian Sync/iCloudでの競合方針 | ユーザー環境の確認 | G2 |
| ISSUE-009 | Medium | 法的/契約資料の保持期間、消去要求 | データ分類・保持方針 | G3 |
| ISSUE-010 | Medium | 初期ターゲットと有料化の妥当性 | 利用者インタビュー | G0 |

Issueを完了にするときは証拠URI、テストID、対応ADR、レビュー日時、検証者を追記する。記録なしで削除しない。


## 2026-10-25 Codex一次審査による統合・追加（すべて未解決）

対象commit: `f4847f32be8da16445c41749b43aeaeb80657415`。詳細根拠、3案、影響、受入証拠は [一次審査](../../reviews/codex/round-1/REVIEW.md) のF-01〜10を正本とする。指摘分類はCritical 3件/High 7件であり、既存台帳件数への単純加算ではない。設計採用・リスク受容は人間判断待ち。

| 既存Issue | 統合する所見と閉鎖条件 |
|---|---|
| ISSUE-001 | F-01：hash確認とrename間の非協調編集。照合直後の保存・クラッシュ注入で無言消失0件。未解決Critical |
| ISSUE-002 | F-02：生成中コンテキスト、回答公開、復元まで失効を伝播。受付後の新規公開・復元再有効化0件。未解決Critical |
| ISSUE-003 | F-08：系列分割、条件snapshot、盲検採点、劣化・停止基準を事前固定。未実測 |
| ISSUE-004 | F-07/04：全導線、承認一回消費、取消競合、差戻し、確認時間を検証 |
| ISSUE-005 | F-03：Cloud OFFかつlocal P1でのP0推論経路の選択を明確化 |
| ISSUE-006 | F-07：試作欠落。画面別のキーボード・読み上げ・320px・差分確認の実測が必要 |
| ISSUE-007 | F-02/09：Vault/DB/Evidence/tombstoneの整合復元、鍵、RPO/RTOを決定し復元訓練 |
| ISSUE-008 | F-01：同期方式を対応対象に含めるなら重大度再評価。現状は未決、対応済みとしない |
| ISSUE-009 | F-02/09：保持・消去・監査・バックアップ例外を決定、復元再露出を試験 |
| ISSUE-010 | F-08：実務頻度・人間確認時間・代替手段をG0で比較 |

| ID | 重大度 | 未解決事項 | 閉鎖に必要な証拠 | ゲート |
|---|---|---|---|---|
| ISSUE-011 | Critical | F-03 分類・同意・全egress経路とP0推論の不整合 | 未分類deny、通信観測、Cloud OFF初回導線 | G3/G4 |
| ISSUE-012 | High | F-04 承認一回消費・実行・取消の競合 | action envelopeと期限・再送・取消競合試験 | G3 |
| ISSUE-013 | High | F-05 attempt・停止・結果不明の永続復旧契約 | worker停止・旧worker復帰・並列resume試験 | G2/G3 |
| ISSUE-014 | High | F-06 ID・分類・知識状態・検証対象hashの権威 | 共通schema、複製・破損・未知状態試験 | G2/G4 |
| ISSUE-015 | High | F-09 ローカル認証・保持・監査・鍵・予算の境界 | 認証/Origin/権限/復元/費用予約の証拠 | G3 |
| ISSUE-016 | High | F-10 試作・検査・template・状態file欠落と段階ゲート矛盾 | 成果物整合、両検査の実出力、追跡・段階修正 | 全ゲート |

## CR-001 改修後の状態（2026-10-25）

F-01〜10を仕様・計画へ反映。全Issueは「設計改修案反映・実証/採否/再審査待ち」でありClosedではない。Critical 3/High 7のNo-Goを維持する。詳細は [REMEDIATION](../../reviews/codex/REMEDIATION.md)。

ISSUE-016の欠落script/template/stateと虚偽の試作完了表示は補修した。操作可能UI試作は新規作成せず、文書storyboardのみ作成。検査基盤の合格と操作試作・PoCの完了を分離する。保持日数/鍵責任者/rotation/RPO/RTO、writer方式とモデル能力、失効保証境界、実験閾値は引き続き人間判断/実証待ち。新たな失敗条件（公開済permitの送信遅延、非fencing tool、分類移行、監査anchor侵害）は対応設計に明記した。


## 2026-10-25 Round 2再審査（改修後commit edcebcc650ec123913ac0407daa32aa2055349a5）

[最新審査](../../reviews/codex/REVIEW.md)。新規記述欠陥はCritical 0/High 4/Medium 1。旧F-01〜10はRound 1の番号、R2-01〜05は今回の番号。仕様上解消と実証完了を区別し、既存Criticalを閉じない。

| 所見 | 重大度 | 統合先・状態 | 必要証拠 |
|---|---|---|---|
| R2-01 | High | ISSUE-011/015へ統合、未解決 | 派生物の分類由来、最終送信payloadと同意、混在→要約→再添付のAI-009子ケース |
| R2-02 | High | ISSUE-013へ統合、未解決 | 成功副作用と純粋計算再利用の分離、訂正/plan/tool/失効後のAI-008子ケース |
| R2-03 | High | ISSUE-014へ統合、未解決 | 検証要求/対象hash/証拠適合/採用者/再検証導線、KB-004/012子ケース |
| R2-04 | High | ISSUE-017 新規、未解決 | Markdown/LLM出力のUI/exportでscriptと外部resourceを遮断。SEC-001/AI-009子ケース |
| R2-05 | Medium | ISSUE-016へ統合、未解決 | phase組合せ、Round本文/実行digest/対象、要件別主試験と省略画面IDを照合する負例 |

ISSUE-017: 非信頼Markdownの表示・exportの実行/通信境界。G1/G3、ADR-017提案。根拠・3比較案・影響・人間採否はREVIEWのR2-04。raw HTML/危険scheme/外部画像/SVG/差分/引用/error/exportを対象とし、製品試験は未実施。

R2-05原文のclaude_complete/started=false見逃し疑義は、親fixtureで拒否を確認し撤回。通過を確認したのは別のphase/started矛盾とRound証拠の取り違え、および追跡表の2見逃し。コード修正なし。通常12ケースOKと追加probeの見逃しを別記。再審査自体は実施完了だが、解消実証・人間採否・独立反証が未完了なのでNo-Goを維持する。

## CR-002の二軸状態（2026-10-25）

| 所見/Issue | 設計記述の状態 | 動作実証/後工程 |
|---|---|---|
| R2-01 / 011,015 | job taint/由来/最終envelope・同意・送信claimを仕様化、採否/再審査待ち | AI-009.a〜f、通信試験not_run |
| R2-02 / 013 | 不変resume・訂正fork・pure/effect/ledgerを仕様化、採否/再審査待ち | AI-008.a〜c、KB-011.a not_run |
| R2-03 / 014 | registry適合/runner証拠/owner採用/対象hash/失効の縦断契約を仕様化 | KB-004/012、EVAL-002の子ケースnot_run |
| R2-04 / 017 | 初期plain text/安全URL専用操作/text exportを仕様化、採否/再審査待ち | renderer/CSP/egress/a11y not_run |
| R2-05 / 016 | 文書validatorを修復、主試験/省略画面/本文digest/対象/phaseの負例を確認 | reviewer本人性・人間採否・独立性は自動検査の保証外 |
| 旧001/002/011 | 安全境界/停止を仕様化。方式/保証範囲の人間採否はH-pending | 同時編集/削除/復元/モデル能力は実装後R-not_run |
| 003/004/006/007/010/015 | 評価/UX/保持/鍵/RPO/RTO/価値確認の設計を整理 | 人間判断/interviewはH-pending、実機/動的UI/効果はR-not_run |

動作実証が必要なIssueはClosedへ偽装せず、G5-Dの文書処置とG5-Rの実証を別列で追跡する。実装後台帳に従い実施して設計を改良する。今回の検査器修復は製品実装ではない。重要方式の人間採否と仕様再審査は未取得として保持する。

## 2026-10-28 CR-003 反証レビュー処置

CR-01はISSUE-001/005/010へ統合、S/H調査をI前に分離したが未実施。CR-02は005/011、local数値候補の人間採用と能力実測待ち。CR-03は015、認証要件/API/データ/画面契約と試験子ケースを補完、本体未検証。CR-04/05は016、M7の相互照合と現行source未審査WARNをコード修正、正式審査/真正性は未解決。CR-06は016/010、slice追跡を追加。CR-07は003/004、標本設計のfreezeを補完し実験未実施。CR-08は015、保持文の曖昧さだけ訂正。

すべて文書/検査修正と動作/採否を分離し、既存Critical/HighをClosedにしない。CR-003の仕様候補は再審査待ち、S/Hの未了はR-not_runと別。全8所見の対応はreviews/cr-003/REMEDIATION.md。
