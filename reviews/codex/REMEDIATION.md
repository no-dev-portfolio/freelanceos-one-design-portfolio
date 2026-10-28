# CR-001 一次審査に基づく設計改修対応表

対象審査: f4847f32be8da16445c41749b43aeaeb80657415 / 改修元: 3952a1cb5d950240374a641c4876fd37846f5a13 / 日付: 2026-10-25。

**設計候補の保存。実機・独立反証・人間受容は未完了、No-Go継続。** 一次REVIEW本文と実行証拠は不変。Claude Code/アプリ実装は開始していない。

| 指摘 | 反映先 | 文書での処置 | 未解決・閉鎖証拠 |
|---|---|---|---|
| F-01 | SYSTEM_DESIGN/REQUIREMENTS/KNOWLEDGE_MODEL | renameをCAS扱いしない。writer能力gate、元版保存、journal/競合復旧 | ISSUE-001/008、ADR-008の人間選択、KB-010実機 |
| F-02 | SYSTEM_DESIGN/DATA_MODEL/API | tombstone/epoch、失効と公開直列化、stream buffer、復元隔離 | ISSUE-002/007/009、未検知gap/既送信の保証受容、KB-011 |
| F-03 | PRD/REQUIREMENTS/KNOWLEDGE_MODEL/AGENT | 単一分類、未知deny、全egress、Cloud OFF、最小local能力条件 | ISSUE-005/011、モデル実用性/性能とAI-009 |
| F-04 | API/DATA_MODEL/SCREEN_SPEC | action環境/宛先固定、一回消費、取消不能点、通信断照会 | ISSUE-012、AI-007/UX-006 |
| F-05 | AGENT/DATA_MODEL/API/SCREEN | attempt/lease/fencing、CancelRequested/OutcomeUnknown、照合 | ISSUE-013、AI-008障害注入 |
| F-06 | KNOWLEDGE_MODEL/DATA_MODEL | note_id、status統一、validated_hash、属性権威、候補隔離 | ISSUE-014、KB-012、移行dry-run |
| F-07 | SCREEN_SPEC/DESIGN_SYSTEM/IA/STORYBOARD | 画面別復帰、mobile承認条件、focus/読上げ、5代表操作 | ISSUE-004/006、操作試作/利用者/適合試験は未実施 |
| F-08 | GROWTH_EVALUATION/VERIFICATION_PLAN | 同corpus/paired条件、系列holdout、固定採点/分母/CI | ISSUE-003/010、EVAL-004、効果と確認時間の実測 |
| F-09 | SYSTEM/API/DATA/THREAT/AGENT | local認証/最小権限、保持/鍵のblocker、監査と予算予約 | ISSUE-015/007/009、SEC-001/OPS-004、保持/RPO/RTO値決定 |
| F-10 | README/PHASES/TRACEABILITY/reviews/scripts/templates | 虚偽完了を訂正、37試験追跡、実検査基盤と状態recorded | ISSUE-016は文書/検査補修、操作試作と採否/再審査は別途必要 |

file略記はdocs配下の同名文書。完全な対応は [TRACEABILITY](../../docs/08-governance/TRACEABILITY.md)。比較3案・費用・新リスク・反証・移行は [CR-001](../../docs/08-governance/DESIGN_REMEDIATION.md)。検査実結果は [VALIDATION](VALIDATION.md)。文書記述の追加は事故が防げた証拠ではなく、全Critical/Highは検証・再審査待ち。


## 審査履歴の固定

本表はCR-001とRound 1への対応。元の一次審査/実行証拠は [Round 1](round-1/REVIEW.md) に不変保存。改修後の再審査は [Round 2](REVIEW.md)、対象はedcebcc650ec123913ac0407daa32aa2055349a5。新規High 4/Medium 1、既存Criticalの実証待ちを継続。
