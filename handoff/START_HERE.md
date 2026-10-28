# Codex / Claude Code 引継ぎ: START HERE

## 最初のタスク
**実装せず設計レビューする。** まず共通作業協定・基本設計・要件・画面・ナレッジ・テストを読み、最大のリスク上位10件を批判的に洗い出す。既存Issueと重複は統合する。修正提案と反証案を記述する。

## 依頼用プロンプト（そのまま貼り付けてよい）
> あなたはFreelanceOS ONE 4.0の設計審査担当です。AGENTS.md / CLAUDE.md と `docs/08-governance/AI_WORKING_AGREEMENT.md` に従ってください。今は実装しないでください。全設計の矛盾、要件不足、UX誤操作、Vault同期、記憶汚染、安全性、運用コスト、検証可能性を厳格に審査し、反証付き改善案を優先度順に作成してください。要件・UI・データ/API・テストの影響関係を更新し、ADR/ISSUES/REVIEW_LOGを記録してください。検査スクリプトを実行し、最後にユーザーの承認が必要な設計決定だけを簡潔にまとめてください。

## Codexで開始
GitHubリポジトリのルートにZIPを展開しCodexを開く。`AGENTS.md`はリポジトリのルール。初回の依頼では上記プロンプトを使用。

## Claude Codeで開始
同じディレクトリをClaude Codeで開く。`CLAUDE.md`から共通協定を参照。初回は同じプロンプトを使用。

## 設計と実装を混同しない
実装の提案は可能だが、ユーザーが「Stage 1の実装開始」を明示するまではファイル・API・DBの実装を作らない。静的UI試作はレビュー用途のみ。

## 毎セッションの成果
1. issueの優先度と重大度、2.修正設計と代替案、3.反証と未検証仮説、4.影響された要件・テスト、5.レビュー記録、6.次回担当への引継ぎ。

## CR-001後の再開位置

まず `docs/08-governance/DESIGN_REMEDIATION.md` と `reviews/codex/REMEDIATION.md` を読む。一次審査済み、改修は設計候補、実機/独立反証/人間採否待ち。既存REVIEWのfile:lineは旧対象commitの根拠なので現行行番号へ書換えない。Claude Codeとアプリ実装を開始しない。両検査は復旧済みだが構造検査のみである。

## CR-002後の次の手順

`docs/08-governance/DESIGN_REMEDIATION_2.md`、EXECUTION_CONTRACTS、CONTENT_PRESENTATION、POST_IMPLEMENTATION_VALIDATIONを読む。今回は仕様改善と文書validatorのみ。最新正式審査は旧対象edcebccのRound 2、CR-002の仕様再審査/重要方針採否は未済。

次は仕様差分/残る人間判断を確認して対象範囲を固定し、利用者が別途実装を明示許可した後に実装する。実装後はverification-registerの担当/期待値/証拠/差戻し先で検証し、失敗から設計を改良。未実装の実証だけを理由に文書審査を無限反復しない。Claudeとアプリ実装は今回開始しない。

## CR-003 ローカル修正版の再開位置

CR-003対応報告、FEASIBILITY_SPIKES、TRACEABILITYのsliceを読む。文書検査コードを修正したが本体アプリなし。S/H調査/数値候補採用/最新source正式審査が必要。旧CLI証拠は保持し新審査へ付替えない。GitHubへは未反映。