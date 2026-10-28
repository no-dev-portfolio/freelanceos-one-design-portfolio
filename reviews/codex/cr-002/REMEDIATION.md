# CR-002 実装なしで確認する設計の改善結果

改修元commit: `6977c21930b2541b27bfc9b47468c9423ef2a2c8`。正式Round 2は旧対象commitの歴史記録として不変。今回の追加CLI審査/独立反証/人間採否を実施したとしない。

| 所見 | 改修 | 今確認した範囲 | 実装後に残す確認 |
|---|---|---|---|
| R2-01 | job taint/由来継承、最終egress/body/添付同意、claim/取消境界 | 机上D-01〜06とAPI/DB/Agent/画面の対応 | AI-009.a〜gの実通信 |
| R2-02 | 不変resume、訂正fork、pureの依存判定、系譜跨ぎeffect ledger | 机上D-07〜10、成功と再利用の区別 | AI-008/KB-011の故障/失効/並列動作 |
| R2-03 | registry適合/runner Passed/owner採用/Verifiedの分離、対象hash/証拠失効 | 机上D-11〜15、API/DB/画面/型の対応 | KB-004/012、EVAL-002の昇格/失効 |
| R2-04 | 初期plain text、外部resource/危険scheme遮断、text/JSON export | 表示規則と事故例、token配色24組の計算 | renderer/CSP/通信/a11y/exportの実効性 |
| R2-05 | 主試験/省略画面/API/entity/証拠digest/対象/session/phaseの検査 | 両validator、元の4見逃しを含む28ケース | 本人性/独立性/人間採否は自動検査で証明しない |

実装依存の未検証を理由に同じ文書審査を無限反復せず、[実装後台帳](../../../docs/06-quality/POST_IMPLEMENTATION_VALIDATION.md) に従い実施・差戻し・再試験する。設計の採用/実装許可/実運用受入は別記。現在は仕様候補更新済み・再審査/人間採否待ち、runtime37件not_run。

比較3案・費用/新リスク/反証/移行は [CR-002](../../../docs/08-governance/DESIGN_REMEDIATION_2.md)、実検査出力は [VALIDATION](VALIDATION.md)。
