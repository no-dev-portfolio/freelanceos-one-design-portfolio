# UIデザインシステム v0.9

## 視覚方針
Calm Workspace：静かな業務画面を基本とし、SQL/コード詳細は開発ツール型、知識詳細は文書閲覧型。ブランド表現は控えめにし、可読性・根拠の見つけやすさ・誤操作防止を優先。

| Token | Light案 | Dark案 | 用途 |
|---|---|---|---|
| background | #F6F8FB | #111827 | 全体背景 |
| surface | #FFFFFF | #1F2937 | 作業面 |
| text | #182235 | #F3F4F6 | 主本文 |
| muted | #526176 | #CBD5E1 | 補助本文 |
| primary | #225EA8 | #7AB4F5 | 主操作 |
| positive | #16724D | #5BD3A0 | 成功＋文字ラベル |
| warning | #9A6016 | #F4C16F | 確認＋文字ラベル |
| critical | #B13535 | #FF8585 | 危険＋文字ラベル |

本文16px基準、line-height 1.5以上、補助テキストは原則12px未満にしない。日本語UIでは重要情報を切り捨てない。8pxスペーシング基準、角丸8〜12px、モーション最小化。色の組合せはWCAGコントラストで実測。ダークモード、OSの文字倍率、Reduced Motionに対応。

### コンポーネント
AppShell, PrimaryNavigation, StatusLabel, TaskTimeline, EvidenceCitation, KnowledgeCard, RevisionDiff, ApprovalAction, SyncHealth, EmptyState, ErrorRecovery, PermissionPreview, CostBudget, Toast/InlineError。

### UI原則
- インライン承認と承認センターに同じ状態を表示。
- 「完了」と「提案」「未検証」を異なる語で表示。
- 削除/外部送信時はUndo不能なら明示。
- 重要承認はダイアログより差分専用ビューを優先。
- 履歴は残すが通常のユーザーには専門ログを押し付けない。

## v0.10 復旧・状態コンポーネント

OperationStatusは「受付/実行中/停止要求済み/結果不明/照合済み」を語句で区別。ApprovalActionはaction hash/versionとoperation_idを保持し、状態照会中の再送を抑止。ConflictViewは元/現在/提案を同等に示し、mergeの新承認を必須化。ErrorRecoveryはreason code→次の一手→復帰先を表示する。全状態はSCREEN_SPECの表と同じ語彙を使う。

CR-002で候補tokenの24組を計算し、受入候補4.5以上（最小4.863）を確認した。実renderの配色測定、screen reader、zoom、keyboard試験は未実施。token計算だけで適合判定しない。リスク操作を色だけで区別しない。

## v0.11 表示・確認語彙

ContentTextはHTML/Markdownを実行せず、Diff/EvidenceCitation/InlineErrorも同じtext境界を使う。ValidationStatusはRequested/Running/Passed/Failed/TimedOut/EvidenceStaleと「Verified採用」を別ラベルにする。ResumeActionは不変入力の継続、ForkActionは訂正後の新job。TaintLabelはpublic/非public/由来不明と送信不可理由を表示する。詳細はCONTENT_PRESENTATIONとSCREEN_SPEC。コンポーネントの実装・適合試験は未実施。
