# DOC-10 セキュリティ・プライバシー脅威分析

| 脅威 | 侵入口 | 影響 | 軽減策 | 検証 |
|---|---|---|---|---|
| プロンプト注入 | Markdown/メール/ログ | 禁止ツール実行 | 信頼境界、allowlist、schema、policy | TEST-AI-001 |
| メモリ汚染 | 外部ノート | 誤った回答を継続 | source quarantine、検証、失効、版管理 | TEST-EVAL-002 |
| 機密漏洩 | Cloud LLM egress | 顧客秘密の送信 | default-deny分類、送信前diff、local選択 | TEST-AI-002 |
| Vault外参照 | パストラバーサル/symlink | 任意ファイル取得 | canonical path、root enforcement | TEST-KB-001 |
| 誤承認 | base hash変化 | 意図しない更新 | 承認hash固定、期限、再照合 | TEST-AI-004 |
| 競合上書き | AI/人の同時編集 | 知識消失 | CAS, backup, conflict UI | TEST-KB-005 |
| 削除済み知識残存 | cache/index | 意図しない再露出 | 即時denylist、索引無効化 | TEST-KB-007 |
| SQL暴走 | DB読み取り接続 | ロック/負荷/コスト | least-privilege、timeout、row limit、allowlist | TEST-AI-006 |
| 二重外部処理 | timeout/retry | 重複送信 | idempotency and outcome reconciliation | TEST-AI-005 |
| ログ漏洩 | traces/audit export | 秘密の二次漏洩 | redact、least retention、encrypted backup | TEST-OPS-002 |

### 信頼境界
外部文書/LLM出力は非信頼、ローカル設定もUIで勝手に昇格しない。ファイル、ネットワーク、DB、外部サービスそれぞれの接続に別のPolicy Gateを置く。

### 限界と残る決定
秘密情報検出の誤検知/見逃し、データ保存期限、削除済みバックアップの扱い、暗号鍵管理、脅威モデルの第三者レビューはPoC/設計審査で決定。

## v0.10 脅威境界の具体化

| 追加攻撃/障害 | 強制点 | 受入証拠 |
|---|---|---|
| hash確認後に非協調editorが保存 | writer能力判定、未検証なら適用不可。renameをCAS扱いしない | TEST-KB-010 |
| 検索後の失効・生成tokenの先出し | 依存epoch、公開permitと失効の直列化、公開前buffer | TEST-KB-011 |
| Frontmatterをverified/publicへ改変 | DB検証hash/ACL、分類の厳格側合成、未知値deny | TEST-KB-012 |
| 同じ承認で宛先/環境を変更、取消とclaimを競合 | 不変envelope、一回消費、同一lockによる直列化 | TEST-AI-007 |
| 古いworkerの復帰 | lease/fencing、外部結果照合、不明なら再送禁止 | TEST-AI-008 |
| 付随Embedding・ログ・fallbackから漏洩 | 全egress経路、public同意、Cloud既定OFF | TEST-AI-009 |
| 悪意Webからlocal API、再送、Host書換 | session/CSRF/exact Origin/Host、loopback、入力境界 | TEST-SEC-001 |
| 監査障害・予算並列発注・古い復元 | audit永続前に高リスク停止、予約直列化、最新失効合成 | TEST-OPS-004 |

ログは原文でなくhash/最小摘要を原則にし、redaction前bufferにも保存先・保持制限を設ける。append-only DB権限、hash連鎖と別保全anchorを組み合わせ、管理者/鍵侵害時の完全性保証の限界を明示する。保持日数/鍵rotation/RPO/RTO/送信後の回収不能は未決運用blocker。これらの決定と実機試験なしに安全性検証済みとしない。

## CR-002の仕様改善と実証時期

R2-01の派生物/再添付は単調job taintと最終envelope同意、R2-02の訂正再開は不変manifest/fork/作用ledger、R2-03の不正証拠はsuite適合/runner証拠/owner採用、R2-04の描画注入はplain text/外部resource遮断で仕様化。全てEXECUTION_CONTRACTS/CONTENT_PRESENTATIONへ統合した。

規則と机上事故例の対応は実装前に確認し、DB/HTTP/FS/rendererへの強制の実効性は実装後の37計画で確認する。失敗すれば該当capabilityを停止し、該当Issue/ADR/設計を改良して再試験。動作未検証を安全性確認済みにしない。
