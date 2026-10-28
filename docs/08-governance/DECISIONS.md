# 設計決定（ADR台帳）

| ID | 状態 | 決定 | 根拠 / 代替案 |
|---|---|---|---|
| ADR-001 | Proposed | Obsidian Markdownを知識本文正本に | データ可搬性。代替: DB本文正本、Obsidianプラグインのみ |
| ADR-002 | Proposed | PostgreSQLを業務状態正本に | 同時更新/監査。代替: Markdownのみ、SQLite |
| ADR-003 | Proposed | AI単一Planner＋allowlist tool群から始める | 複雑性削減。代替: multi-agent |
| ADR-004 | Proposed | Cloudへの情報送信default deny | 秘密保護。代替: allow-by-default（不採用） |
| ADR-005 | Proposed | 3主画面（今日/仕事/知識） | 日常操作優先。代替: 8カテゴリのメニュー |
| ADR-006 | Proposed | Knowledge版/hashとindex版の不一致は安全側へ | 古い知識誤利用防止。代替: eventual consistency無警告 |
| ADR-007 | Proposed | 人の承認と技術検証を分離 | 人の好みと真偽の違い。代替: 承認即verified |

## 新ADRの書式
`ADR-008: title / Context / Decision / Options / Why / Consequences / Security impact / UX impact / Verification / Approver / Date / Status`。採用前はProposed。旧ADRは消さずSuperseded。


## 2026-10-25 一次審査からのADR提案（未採用）

全て **Proposed / Approver: pending / Date: 2026-10-25**。Decisionは未決。採用・正本変更・P0変更・実装許可を意味しない。Context、3比較案、費用、新リスク、失敗条件、Security/UX impact、Verificationは下記参照先に記録。重要判断は人間処置待ち。

| ID | 判断対象・Context | Options / Why / Consequences / Verification |
|---|---|---|
| ADR-008 | 非協調編集下のVault書込方式、対応環境（ADR-001/006関連） | REVIEW F-01：提案file/協調ゲート/自動反映停止。競合PoC後に選定 |
| ADR-009 | 失効の起点・回答公開・復元tombstone（ADR-006関連） | F-02：失効世代/関連job停止/保証縮小。漏洩と停止範囲を比較 |
| ADR-010 | 分類・同意・P0モデル経路（ADR-004関連） | F-03：local必須/公開データ同意Cloud/AI縮小。egress観測 |
| ADR-011 | 承認対象固定・消費・取消不能点 | F-04：一回承認/直前対話/単一操作限定。競合試験 |
| ADR-012 | attempt・fencing・不確定復旧（ADR-002/003関連） | F-05：DB制御/durable基盤/手動照合。障害注入 |
| ADR-013 | 知識属性の権威・検証hash（ADR-001/007関連） | F-06：共通schema/属性DB管理/対象知識限定。破損・複製試験 |
| ADR-014 | 記憶比較・holdout・劣化停止 | F-08：事前登録比較/少数リスク検出/実務観察。条件固定と採点 |
| ADR-015 | local境界・保持・鍵・監査・費用 | F-09：厳格local profile/bridge/隔離PoC。認証・復元・上限試験 |
| ADR-016 | PoC・設計承認・実装着手の分離 | F-10：成果物修復/手動未完チェック/固定commit再審査。検査実体と負例 |

移行・巻戻し：仕様採用前なので現設計は維持。将来のID/分類/状態移行はプレビュー、未知値隔離、旧版保持、索引再構築を必須設計とする提案。現在のレビュー追記を戻す場合も審査証拠を履歴に保持し、修正版で指摘の解消を判定する。

詳細：[Codex正式一次審査](../../reviews/codex/round-1/REVIEW.md)。他レビュアーとの合意・反証結果はまだ存在しない。

## CR-001によるADR具体化

2026-10-25、利用者から一次審査をもとに設計資料の改修・GitHub保存を依頼。ADR-008〜016のContext/3案/費用/反証/移行/検証を [DESIGN_REMEDIATION](DESIGN_REMEDIATION.md) に具体化し、要件/画面/API/DB/Knowledge/Agent/評価を同時改訂した。状態は全てProposed、人間の個別採否はpending。本文正本・Cloud default OFF・既存27要件とP0を維持する。旧snapshotへ戻す場合も失効台帳を巻き戻す設計は採らない。変更前REVIEWは旧commitの記録として保持する。


## Round 2の追加検討（2026-10-25、採用未決）

ADR-010/015にR2-01（分類由来/最終egress）、ADR-012にR2-02（resume入力不変/成功step再利用）、ADR-013にR2-03（検証operationと証拠採用）、ADR-016にR2-05（state/本文/実行/追跡の束縛）を補足。3案・費用・新リスク・反証・移行は [Round 2](../../reviews/codex/REVIEW.md) を参照。既存仕様を変更・採用していない。

ADR-017: 非信頼Markdownの表示境界 / Status: Proposed / Approver: pending / Date: 2026-10-25。Context: R2-04、LLMへの命令境界だけでは描画時のscript/外向きresourceを制御しない。Options: A許可Markdown subset/sanitize（中）、Bplain text（低、初期推奨）、C隔離viewer+通信gate（中高）。新リスク: 可読性低下、parser保守、隔離設定漏れ。旧案は完全plain text実装を制約として確定できれば追加機構が小さい。Security/UX impact: 本文・差分・引用・ログ・exportの安全表現。Verification: SEC-001/AI-009/UX-005/OPS-002の子ケース。移行: 元本文を改変せず安全rendererで再表示、描画済み派生物を再生成。Decisionは人間判断待ち、実装なし。

## CR-002（2026-10-25）

変更前の影響/3比較案/費用仮説/反証/移行を [DESIGN_REMEDIATION_2](DESIGN_REMEDIATION_2.md) に記録。ADR-010/015へjob taintと最終egress、ADR-012へ不変resume/訂正fork/作用ledger、ADR-013へvalidation採用gate、ADR-017へ初期plain text、ADR-016へactiveレビューdigestとphase真理値表を具体化。各重要方式の個別採用はProposed、仕様改修PRで判断する。本文正本・Cloud既定OFF・既存P0を維持。

ADR-018: 設計仕様と実装後実証の分離 / Date: 2026-10-25 / Status: 利用者指示を設計に反映（実装/運用許可なし）。Context: 未実装の実証を仕様改善の前提にすると循環する。Decision: G5-D（仕様）→別のI許可→実装→G5-R（実証/有効化）→失敗から再設計。Options: 実機を全設計の前提、段階分離、実証省略（不採用）。Risk: 実装後の手戻り、安全性受入の省略と誤読されること。対策: 台帳/停止条件/役割/証拠と明示許可を分離。移行: 過去No-Go/失敗を保持し、対象capabilityを実証なしで有効化しない。Verification: 文書整合と37件台帳は今、動作と効果は実装後。

## CR-003（2026-10-28、採用候補）

ADR-019: 認証契約/画面API・許可記録の相互照合 / Status: Proposed / Approver: pending。
Context: CR-03/04/05で所有要件・APIと許可照合が欠落。Options: 注記のみ、共通照合+台帳、製品実装。今回の文書/validator修正は中央照合と台帳を選ぶ。費用・新リスク・反証・移行はDESIGN_REMEDIATION_3参照。真正性を暗号学的に証明する機構ではない。

ADR-020: 事前調査と初回slice / Status: Proposed / Approver: pending。
S（隔離spike）/H（利用者調査）をI前の判断材料に追加。S用の範囲許可と製品I許可は別。候補はread-only安全基盤S1→協調書込/独立再利用/評価S2、P1は後段。代替は全面P0同時実装、read-only限定製品への転換。コスト/反証はDESIGN_REMEDIATION_3、数値はFEASIBILITY_SPIKES。ADR-018のR分離を保持し、S合格をG5-R合格へ流用しない。
