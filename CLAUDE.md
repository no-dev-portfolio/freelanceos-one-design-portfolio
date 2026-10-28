# Claude Code instructions — FreelanceOS ONE

必ず最初に `docs/08-governance/AI_WORKING_AGREEMENT.md` と `handoff/START_HERE.md` を読む。`AGENTS.md` と矛盾したルールを新設しない。設計の変更は提案→影響分析→ADR/課題→テスト反映→レビューの順に行う。

- **現在は設計フェーズ**。利用者の明示的な許可なく本体実装を始めない。
- 要件ID、画面ID、状態ID、テストIDの追跡を崩さない。
- 質問・仮定・保留は `ISSUES.md` に記録し、裏付けのない事実を補完しない。
- セキュリティ、個人情報、不可逆操作を軽視して設計を簡略化しない。
- 審査で問題を見つけたら改善案・デメリット・検証法もセットで提案する。
- 作業後 `python3 scripts/check_design.py` とレビュー記録の更新を行う。


**Counter-review gate:** Do not proceed until phase is `codex_complete` with real evidence. Follow `reviews/CLAUDE_COUNTER_REVIEW_PROMPT.md`; independently assess the baseline before challenging Codex findings. Run `python3 scripts/check_review_gate.py`.
