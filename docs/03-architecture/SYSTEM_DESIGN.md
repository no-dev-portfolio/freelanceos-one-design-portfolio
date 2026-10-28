# DOC-04 システム基本設計 v0.10

**改訂:** 2026-10-25 / CR-001 / 設計候補。重要ADRはProposed、実機未検証。審査基準・影響・比較案は [改修計画](../08-governance/DESIGN_REMEDIATION.md)。

## 責任分界と構成
UI → 認証API → Policy/Approval → 永続Workflow → 許可Tool/LLM Adapter。Retrieval → PostgreSQL FTS/pgvector（派生索引）→ Vault Sync（本文照合）。全外向き通信はegress gateを通す。

| 正本 | 内容 | 禁止事項 |
|---|---|---|
| Obsidian Markdown | 本文と可搬属性。移動でもnote_id維持 | PostgreSQL本文を別の更新正本にしない |
| PostgreSQL | job/attempt/action/承認/監査、検証証拠、ACL/失効、版mapping | Frontmatterのverifiedや公開指定だけで権限昇格しない |
| Evidence Store | 元版・提案版の不変snapshot、検証結果・hash | 復旧用snapshotを通常検索へ混ぜない |
| LLM | 候補・説明・計画 | 認可、確定、検証済み昇格、無制限実行をしない |

## 対象環境と能力確認
Macローカルを初期候補としAPI/UI/DB/workerを分離する。APIはloopbackだけへbindし、DBはhostへ公開しない。UI/workerはVault read-only、Syncだけ許可Vaultへの書込資格を持つ。実際のマウント設定はTEST-SEC-001で確認する。symlink/別mount/パス差替えはディレクトリ境界で拒否し、検査した対象と開いた対象の同一性を確認する。

Cloud LLM・外部Embedding・telemetryはdefault OFF。P0の機密タスク向け最小local推論経路の成立を能力PoCで確認する提案。P1ローカルLLMはモデル選択・高速化・配布最適化を指す。利用可能な推論経路がなければMODEL_UNAVAILABLEでBlockedとし、秘密をクラウドへfallbackしない。これはP0提供完了ではない。publicデータ向けCloudの明示有効化は分類・同意・上限・egress試験を通した場合のみ。AWS・remote/mobile公開は初期運用対象として未承認。

## Vault更新プロトコル（REQ-KB-005/006）
1. 不変actionにtarget note_id、vault_id、元本文snapshot、base_hash、proposed_hash、policy版、writer能力を保存し承認へ束縛。
2. Syncが書込開始前に現在の対象・hash・失効・権限・承認を再確認。writer_modeが未検証、非協調Obsidian/同期writerが存在、Vault不達なら副作用前にBlocked。
3. **hash確認後のrenameだけをCASと呼ばない。** 全writerが協調する排他区間内で比較から確定まで保護できる場合だけ適用可能とする設計候補。排他を守らないeditor/別端末が存在するとき適用を許可しない。OSのファイルlockだけでObsidianも従うと仮定しない。
4. 隔離PoCでは同一directoryへのtemp生成→内容fsync→rename→parent directory永続化→再読取照合を検証。権限・属性・改行・symlinkを含む。これは耐久性候補で、条件付き更新の証明とは別。
5. operation journalをPrepared→Applying→Committedに進め、索引更新をoutboxへ登録。DBとFSの単一transactionを仮定しない。異常時OutcomeUnknownに隔離して自動再適用しない。
6. 再起動は保存snapshot/元hash/提案hash/実ファイルを照合。現在hashが元なら未反映候補、提案hashなら反映候補、それ以外はConflict。hashだけで履歴を断定せずjournal・外部writer状況を照合して手動確定。不確定では承認を再利用しない。

非協調環境の提案file方式、全writer協調方式、適用停止でのPoCをADR-008で比較中。P0安全更新を削除せず、成立証拠が揃うまで提供不可とする。APFS・iCloud・Obsidian Sync・network Vaultは環境ごとにTEST-KB-010を通す。未合格環境はread-only/候補確認まで。

## 失効と公開の整合性（REQ-KB-007）
失効API受付はDB内でtombstone/ACL版/単調revocation_epoch更新とauditを同時確定する。失効受付のcommitを線形化点とする。検索結果だけでなく、jobの派生要約・引用・生成buffer・成果物に依存note/hash/epochを保持する。

回答・成果物の公開gateは現在のACL/失効/本文hash/索引hash/検証hashを照合し、失効受付と公開permitの順序を同一DB排他で直列化する。公開済みの定義はpermitと公開記録の確定であり、端末への到着時刻ではない。受付より前に許可済みの送信bufferは回収不能と表示し、未公開bufferは破棄する。secret由来のtoken streamingはgate通過前にUIへ出さず、必要なら全文bufferする。外部LLMへ既送信の本文も回収を保証しない。

ファイル外部削除の発生からwatcher検知までの絶対即時性は保証しない。公開直前の現物確認、watcher gap/同期不明時fail-closed、手動失効APIを組み合わせる。参照先が変化・不達なら回答を保留し再取得する。外部ファイル確認とその後の外部変更の競合限界はTEST-KB-011で記録し、保証範囲を人間が受容するまでISSUE-002は閉じない。

## 障害・復元
Vault、DB、Evidence、索引版、policy、tombstoneを一つのbackup manifestへ記録。DB/Vaultの相互snapshotが確定できなければ書込を静止しbackup未完扱い。復元は隔離→最新失効台帳の合成（古いsnapshotで復活させない）→権限/分類確認→索引再構築→整合照合→人間の公開許可。最新台帳が失われた場合は全復元知識をdenyとして再審査する。鍵がないbackupを復元可能と表示しない。

RPO/RTO、保持日数、鍵保管・rotationは値と責任者を実運用前に決定するrelease blocker。TEST-OPS-001/004で復元訓練する。索引は派生物として再構築可能、再構築中は混在世代を使わずINDEX_STALE/Blocked。性能P95・検知SLOはVault規模別PoCで決め、未実測値を表示しない。

## v0.11 実装前後の分離と追加契約

CR-002では机上で定義できる分類/最終egress、resume/fork、validation operationを [EXECUTION_CONTRACTS](EXECUTION_CONTRACTS.md) に具体化。非実行表示はCONTENT_PRESENTATION。実装後にしか確認できないFS/DB競合、通信遮断、model実用性、復元、a11y/性能/知識効果はPOST_IMPLEMENTATION_VALIDATIONと37件の台帳へ登録した。

文書仕様を改善しても当該capabilityを実証済みとはしない。一方、未実装ゆえの未実証だけを理由に仕様改良を終えられない循環は作らない。設計仕様審査G5-D、別の実装許可I、実装後の機能有効化G5-Rを分離する。保持日数/鍵責任者/RPO/RTO等の人間判断は実装なしでも可能なH-pendingとして扱い、運用前の決定条件を残す。
