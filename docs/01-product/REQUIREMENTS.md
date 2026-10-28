# DOC-01b 要件カタログ

各要件は状態・優先度・受入条件を持つ。削除時はIDを再利用しない。P0は初期製品で必要な要件。最初の実装slice S1だけで全P0を提供するとはしない。各要件のS1/S2/後段はTRACEABILITYで追跡する。

| ID | 優先 | 要件・受入条件 | 主な検証 |
|---|---|---|---|
| REQ-UX-001 | P0 | 今日/仕事/知識の主要3ナビゲーション。5代表操作を到達可能 | TEST-UX-001 |
| REQ-UX-002 | P0 | AI作業の状態/履歴/成果物/停止を表示。不変resumeと訂正forkを区別 | TEST-UX-002 |
| REQ-UX-003 | P0 | 承認画面で現在版・変更版・証拠・適用範囲を提示 | TEST-UX-003 |
| REQ-UX-004 | P0 | 空状態/読取不可/通信断/競合/拒否を日本語で説明 | TEST-UX-004 |
| REQ-UX-005 | P0 | キーボード操作とWCAG 2.2 AAを設計目標とする | TEST-UX-005 |
| REQ-KB-001 | P0 | 指定されたVaultのMarkdownのみを読み込む（Vault外アクセス拒否） | TEST-KB-001 |
| REQ-KB-002 | P0 | note_id/revision/hashと検証状態を追跡 | TEST-KB-002 |
| REQ-KB-003 | P0 | 知識検索は権限・失効・適用範囲で絞り込む | TEST-KB-003 |
| REQ-KB-004 | P0 | 知識候補の人確認、runnerのPassed、証拠採用によるVerifiedを分離。対象hash/suite/scopeを照合 | TEST-KB-004 |
| REQ-KB-005 | P0 | 全writerの協調が証明された適用区間で変更前版と一致した時だけ更新。非協調/未検証なら適用せずBlocked | TEST-KB-005 |
| REQ-KB-006 | P0 | 同時編集、クラッシュ、索引遅延から復旧可能 | TEST-KB-006 |
| REQ-KB-007 | P0 | 削除/隔離/失効受付の確定後は検索・未公開回答/成果物から除外。外部変更検知gapと既送信限界を明示 | TEST-KB-007 |
| REQ-KB-008 | P0 | 質問に使用した根拠ID/版/引用箇所を保持 | TEST-KB-008 |
| REQ-KB-009 | P1 | ナレッジの重複・矛盾を提案し自動で上書きしない | TEST-KB-009 |
| REQ-AI-001 | P0 | LLMが利用できるツールはサーバー許可リストに限定 | TEST-AI-001 |
| REQ-AI-002 | P0 | 由来/単調job taint/最終payload同意・policyで全egressを強制。非public/未知deny、Cloud既定OFF | TEST-AI-002 |
| REQ-AI-003 | P0 | 実行計画のsteps/時間/最小費用上限、キャンセル要求/実停止の分離、新attempt再開、監査記録 | TEST-AI-003 |
| REQ-AI-004 | P0 | 宛先/環境/tool版を含む不変action hashと期限を固定、一回消費、対象/policy変更時に再承認 | TEST-AI-004 |
| REQ-AI-005 | P0 | 結果不確定の自動再送を禁止。forkでも副作用ledger継承、pure結果再利用は依存一致時だけ | TEST-AI-005 |
| REQ-AI-006 | P1 | SQL/Oracle読み取り専用接続、timeout/件数/対象スキーマ制限 | TEST-AI-006 |
| REQ-EVAL-001 | P0 | 同一問題・モデルで記憶有無／索引方式を比較 | TEST-EVAL-001 |
| REQ-EVAL-002 | P0 | 未見タスク、記憶汚染、失効、矛盾を評価データに含める | TEST-EVAL-002 |
| REQ-EVAL-003 | P0 | 人間確認工数、根拠誤り、タスク達成率を計測 | TEST-EVAL-003 |
| REQ-OPS-001 | P0 | Vaultバックアップ/復元と索引再構築を設計・検証 | TEST-OPS-001 |
| REQ-OPS-002 | P0 | 業務DBイベント、承認、操作結果を追跡 | TEST-OPS-002 |
| REQ-OPS-003 | P1 | 個別タスク/月額の費用設定・分析UI。発注前の最小並列予約/停止はP0のREQ-AI-003 | TEST-OPS-003 |
| REQ-SEC-001 | P0 | local pairing、session発行/更新/失効、CSRF・exact Origin/Host検証を所有。未認証・旧session・期限切れ・異Origin/Host・CSRF欠落を拒否しsecretを返却ログへ残さない | TEST-SEC-001 |
| REQ-BIZ-001 | P1 | 案件評価は必須条件とスキル推定を分離 | TEST-BIZ-001 |

**状態:** 全要件 Proposed。テストは計画IDであり合格実績ではない。

## v0.10 受入条件の補足

既存27 ID・優先度を保持。上記修正はCR-001設計候補であり人間受容/実機検証待ち。REQ-KB-007の「即時」はSYSTEM_DESIGNの失効受付commitと公開permitを直列化した順序で判定する。外部編集の未検知時間をゼロとする保証ではない。この保証境界の人間受容までISSUE-002を閉じない。

REQ-KB-002/004：note_idとvalidated_hashを正規化し、人確認と技術検証を区別。候補は審査専用経路だけ。REQ-OPS-001：Vault/DB/Evidence/tombstone/鍵の整合復元。REQ-AI-005：lease切れを外部処理停止の証拠とせずOutcomeUnknownは照合まで再送しない。REQ-EVAL-001〜003：条件manifest・系列holdout・固定採点・失敗を含む分母を必須とする。計画IDと検証結果を混同しない。

## v0.11 CR-002の確認時期

27要件と優先度を保持。仕様/状態/API/DB/画面/机上ケースは実装前に確認。実装挙動の受入はverification-registerの全37計画へ登録し、実装後に実施して設計を改良する。G5-DとG5-Rを分離、今回の実装許可はなし。非信頼表示/exportは初期plain text/JSON限定、検証昇格はregistry適合suiteだけ。

## v0.12 CR-003

既存27要件を保持し認証所有のREQ-SEC-001を追加、現行28要件。主試験37 IDは維持しSEC-001へ認証子ケースを追加。全件Proposed。古い27件との記述は過去版の記録。S1は価値閉ループの完了を主張できない。S2で安全書込・別問題での再利用・評価を完了する。