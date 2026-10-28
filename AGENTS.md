# Codex repository instructions — FreelanceOS ONE

**まず** `docs/08-governance/AI_WORKING_AGREEMENT.md` を読んで全規約を守る。次に `handoff/START_HERE.md` を読む。

- 現フェーズは **DESIGN ONLY**。明示的な実装許可がない限りプロダクションコード、DB migrations、AWSリソースは作成しない。
- 設計は日本語。図・表・技術識別子・APIフィールド名は英語でよい。
- 変更前に要件ID・画面ID・データ要素・テストIDへの影響を列挙する。
- 重要方針の変更はADRを起票し、代替案・反証・リスク・移行策を残す。
- 未検証の主張を検証済みと書かない。数値は仮説／受入目標と明示する。
- 機密データ・顧客情報を例示に使用しない。すべて架空または明示的に公開可能な値にする。
- 最後に `python3 scripts/check_design.py` を実行し、結果を報告する。
- 作業後は `docs/08-governance/REVIEW_LOG.md` と `docs/08-governance/ISSUES.md` を更新する。


**Primary-review stage:** Follow `reviews/CODEX_REVIEW_PROMPT.md`, produce an actual `reviews/codex/REVIEW.md`, and never produce Claude review on its behalf. Read `reviews/README.md`; run `python3 scripts/check_review_gate.py`.
