# 二段階設計審査の証拠と状態

Codex一次審査は実行・保存済み。本文は [REVIEW](codex/REVIEW.md)、実行方法・初回失敗と成功は [execution](codex/execution.json)。最新Round 2の対象は`edcebcc650ec123913ac0407daa32aa2055349a5`。元の`f4847f32be8da16445c41749b43aeaeb80657415`に対するRound 1は [archive](codex/round-1/REVIEW.md) に実行証拠と対で保持。改修は別成果物 [REMEDIATION](codex/REMEDIATION.md) に追跡し、過去の指摘を上書きしない。

## 状態の意味
`review-state.json`のphase=codex_review_recordedは「実施記録が存在し、人間受容は未済」。codex_completeは受理された一次審査、claude_completeは別セッションの反証成果物と証拠、ready_for_design_approvalは人間の設計審査に出せる状態であり実装許可ではない。構造検査は本人性や独立性を証明しない。

順序：固定commit→AGENTS/全docs/画面設計を読取→一次審査→改修PRと人間処置→前提充足後だけ別Claudeセッション→設計採否。**現在は人間受容・実機証拠・独立反証待ち。Claudeを起動しない。** 自動状態昇格は禁止。

一次審査テンプレートは [CODEX_REVIEW_TEMPLATE](CODEX_REVIEW_TEMPLATE.md)。テンプレートを実レビューと偽らない。UI試作未作成・実機未試験は必ず明示。各所見は根拠file/section、重大度、反証可能シナリオ、3案、費用/新リスク、影響REQ/SCREEN/API/DB/Knowledge/Agent/TEST、PoC、人間決定を含む。

両scriptとvalidator負例試験を実行し、commit/環境/exit/outputを保存する。合格は文書構造だけ。改修してもIssueは実証・再審査なしで閉鎖しない。機密は架空例に限り、既定Cloud OFFと本文正本を無断変更しない。


Round 2はHigh 4/Medium 1の新規記述欠陥、No-Go継続。CLI原文R2-05の一部疑義は親fixtureで反証・訂正し、原文と訂正証拠を保存。独立Claude反証は未実施。

## CR-002以後の証拠束縛と段階

最新の正式審査は引き続きRound 2のedcebcc対象。今回CR-002の改修を正式再審査済みとしない。`active-review.json`がreport/raw_cli/execution/source-manifestのpath/SHA-256、対象commit、sessionを束縛。本文の対象commit行とexecution/activeを照合する。checksumは本人性・人間採否・独立性の証明ではない。

許可状態：codex_review_recordedはhuman pending/rejectedかつClaude未開始。codex_completeはhuman acceptedかつClaude未開始。claude_reviewingはhuman accepted・別session running・同baseline。claude_complete/readyはstarted=true・完了証拠とreport digest・同baseline、readyはremediation acceptedも必要。今回phase/承認flagは変更しない。

設計仕様G5-Dと実装後受入G5-RはPOST_IMPLEMENTATION_VALIDATION参照。実装が必要な試験は実装後に実施して設計へ戻すが、実装着手には別の明示許可が必要。Claude開始も今回指示していない。
