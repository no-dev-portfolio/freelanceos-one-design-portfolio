# DOC-08 Agent / Tool / Workflow設計

## 初期の設計
単一Planner Agent + 許可ツール群 + 確定的Policy Engine。専門Agentの分割は実測でボトルネックが確認された場合に限定。

### 許可ツール（MVP）
| tool_id | 入力 | 副作用 | 安全策 |
|---|---|---|---|
| knowledge_search | query, scope, limit | なし | ACL、版、失効確認 |
| knowledge_get | note_id, revision | なし | 権限と現在hash照合 |
| evidence_attach | evidence_ref, job_id | 監査記録 | ファイル型、サイズ、PIIチェック |
| create_knowledge_candidate | content, source_refs, base_hash | 候補DBへ追加 | 自動検証済みにしない |
| request_approval | action_ref, payload_hash | 承認待ち登録 | ポリシー判定、期限 |
| preview_revision_diff | candidate_id | なし | 元版固定 |
| run_sandbox_test | approved_test_id, dataset_ref | 隔離環境のみ | 任意シェル/ネット接続不可、時間制限 |
| export_report | job_id, format | ローカル成果物作成 | 明示的な保存先、機密フィルタ |

任意SQL実行、ブラウザの自動応募・メール送信、秘密情報読取、任意コマンド実行はMVPでは許可しない。

## State machine
正式な状態と遷移は後述のv0.10永続状態表を用いる。不変manifestの再開は新attempt。成功副作用は再送せず、pure結果は依存一致時だけ再利用する。結果不明の副作用はOutcomeUnknownとして照合する。

## Safety gates
1. Model output schema validate 2. Tool allowlist 3. RBAC/user ownership 4. sensitivity & egress policy 5. scope bound 6. rate/cost limit 7. approval payload exact-match 8. audit append 9. execution result verification。

## Human in the loop
外部送信、ノートの重要な上書き、権限変更などには `target_id`, `base_hash`, `proposed_hash`, `summary`, `sources`, `expires_at` を提示。承認済みhash以外の実行禁止。

## Tool注入対策
取得したMarkdown、メール、ログは必ず非信頼コンテンツとしてタグ付け。記載されている「命令」は業務情報として引用可能でもAIへの権限付与としては無効。

## v0.10 永続状態・実行許可表

**改訂:** 2026-10-25 / CR-001 / 設計候補。重要ADRはProposed、実機未検証。審査基準・影響・比較案は [改修計画](../08-governance/DESIGN_REMEDIATION.md)。

| state | 許可操作・遷移 | 制約 |
|---|---|---|
| Draft | 計画作成→Planned、取消→Cancelled | 入力分類とモデル能力未確認なら実行不可 |
| Planned | 実行前gate→Running、拒否→Blocked | planとpolicy版固定 |
| Running | WaitingApproval/Blocked/Completed/Failed/CancelRequested/OutcomeUnknown | leaseとfencingが有効なworkerのみ |
| WaitingApproval | decision後にgate再確認→Running、期限切れ→Blocked、取消要求 | resumeだけで承認を迂回しない |
| CancelRequested | 安全境界で停止→Cancelled、副作用不明→OutcomeUnknown | 要求受付を停止完了と表示しない |
| OutcomeUnknown | 証拠照合→Completed/Failed/Blocked | 自動resume/副作用再送禁止 |
| Failed / Blocked / Cancelled | 原因解消・照合・policy再認可後、新attempt→Planned | 成功effectを保持、pure再利用は依存一致時だけ。入力/plan変更はfork |
| Completed | 閲覧・export・候補作成 | 再実行は別job、旧承認再使用不可 |

job state_versionと進捗sequenceは単調。attempt_no、lease_owner/until、fencing_tokenをDBへ永続化し、claimと更新を条件付きtransactionで行う。旧workerの更新・結果採用は拒否する。外部toolがfencingを解釈しないならlease失効でも旧処理が止まったと断定せずOutcomeUnknownへ。外部結果照合不能時は手動証拠を要求する。idempotency uniqueだけで外部副作用とDBの原子性を主張しない。

安全gateの順序はschema→toolと引数allowlist→owner/ACL→分類・同意・全egress→対象scope/版→予算予約→action/承認一回消費→監査永続化→副作用→結果照合。送信直前と結果公開直前に現在policyを再確認。ノート・添付・Embedding・ログ・エラー・telemetry・provider fallbackを同じ境界に含める。public以外をCloudへ送らない初期profile案とし、未知値はdeny。Cloud同意は送信先・目的・payload preview hash・期限に束縛し、取消は未送信分へ適用する。

max_steps/timeout/予算のどれか不明なら発注しない。外部有料callはjob/月の残枠を並列予約し、結果後に精算。料金不明・残枠不足はBlocked。P1 CostBudgetの高度分析と別に、P0実行安全条件として最小上限を要件へ追加する。

許可toolでもprompt injectionが引数へ混入し得る。公開可能ノート内の「別fileを読め」「URLへ送れ」等をschema/対象allowlist/egressで拒否する。テスト実行はapproved_test_idと固定架空datasetだけ、任意shell/network不可。TEST-AI-007/008/009、SEC-001が受入証拠。

## v0.11 CR-002の強制点

[EXECUTION_CONTRACTS](../03-architecture/EXECUTION_CONTRACTS.md) に従い、非publicを読んだjobは以後Cloud不可。要約・tool結果・export・forkでもtaint/由来を継承し、不明由来はdeny。provider adapter構築後の最終envelope/body/添付をconsent/actionへ束縛し、変更・redirect・fallbackは再審査する。

resumeはmanifest不変だけ。純粋計算結果はfingerprintと現認可一致時だけ再利用、副作用はeffect_ledgerで系譜を跨いで照合する。訂正は新jobのfork、旧副作用の完了/不明を新jobで迂回しない。

validation operationは登録suiteと固定datasetのみ。runnerのPassedとownerによる証拠採用を分離し、LLMや人の「成功した」という文字列だけでVerifiedへ昇格しない。新たなallowlist tool候補はrequest_validation/get_validation、agentはadopt_validation権限を持たない。既存run_sandbox_testも登録scope以外の主張を実証したとは扱わない。

LLM回答を含む全表示/exportはCONTENT_PRESENTATIONのplain text契約。network/renderer/worker/FSの実効性は実装後台帳で確認し、失敗は対応設計へ差戻す。今回コードは実装しない。
