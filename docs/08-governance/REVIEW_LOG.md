# 設計レビュー履歴

## 2026-10-25 Initial design package
- **実施:** これまでの要求からの整合性レビュー、設計文書化、主要な事故シナリオの棚卸し、AI引継ぎ規約の整備。
- **完了したこと:** PRD、要件ID、画面仕様、論理構成、ナレッジ仕様、API契約、初版テスト設計。
- **未実施:** 実機PoC、外部利用者によるUI試験、DB/API実装、アクセシビリティ検証、セキュリティ侵入試験。
- **状態:** Draft / Design review required。Go判定は未承認。

### 次回レビュー記録テンプレート
日付、担当（Codex/Claude Code/人間）、対象commit、レビュー対象、Critical/High/Medium件数、改善案、採否理由、変更した要件/画面/テスト、検査結果、残リスク、次の担当への引継ぎ。


## 2026-10-25 Codex正式一次設計審査

- 対象commit: `f4847f32be8da16445c41749b43aeaeb80657415` / review/codex-round-1。
- 担当: Codex CLI 0.163.0-alpha.11。session `01a17144-b1e4-73d0-a273-638fd2f11a18`、exit 0/turn.completed確認。
- 方法: 全34ファイルをGitHub connectorで固定取得しblob SHA照合。行番号付き全文をCLI標準入力で静的審査。初回起動と次の直接読取は環境制限で失敗、完了扱いにしていない。
- 成果: [REVIEW](../../reviews/codex/round-1/REVIEW.md)、Critical 3件/High 7件、全27要件追跡・全UX導線・3案比較・PoC計画。ISSUES統合/011〜016追加、ADR-008〜016提案、TRACEABILITY参照。仕様そのものの採用変更なし。
- 検査: python3 scripts/check_design.py と python3 scripts/check_review_gate.py は親Codexが実行し、どちらもexit 2（No such file or directory）。補助ID照合27/27は動作合格ではない。
- 未実施: UI試作操作（file欠落）、実機PoC、セキュリティ動作試験、記憶効果計測、Claude反証レビュー、アプリ実装。
- 判定: No-Go。人間採否・Critical解消・修正版再審査待ち。状態完了化・mainへのmergeはしていない。
- 証拠: reviews/codex/execution.json、baseline-manifest.json、supplemental-checks.json。


## 2026-10-25 CR-001 設計資料改修

- 利用者依頼：再実行した一次審査結果をもとに設計資料を改善しGitHubへ保存。実施担当はこのCodexセッション。追加の独立一次審査やClaude反証を実施したとの主張ではない。
- 改修元：3952a1cb5d950240374a641c4876fd37846f5a13（一次審査PR #2）。mainは元審査baselineのため、review/design-remediation-round-1をPR #2のブランチへ積み重ねる。採用/mergeは人間判断待ち。
- 変更前影響/ADR：DESIGN_REMEDIATIONへREQ/SCREEN/API/DB/Knowledge/Agent/TEST、3案、費用/新リスク/反証/移行を先行記録。ADR-008〜016はProposedのまま。
- 改修：writer能力gate、失効/公開直列化、復元、分類/egress、承認一回消費、attempt/fencing、属性権威、UX復旧、事前登録評価、認証/監査/予算、Stage依存と追跡を具体化。27要件を保持、37試験計画と11画面を追跡。
- 不足補修：検査2本、validator負例試験、変更/審査template、review-state、文書storyboardを追加。操作可能UI試作の完了主張を訂正。既存REVIEW/実行証拠は変更しない。
- 検証：check_design.py exit 0（27要件/37試験計画/11画面）、check_review_gate.py exit 0（codex_review_recorded/pending）、validator 12正負ケースOK。詳細はreviews/codex/VALIDATION.mdとvalidation-results.json。CIはPR Checksで別確認。
- 未実施/未解決：実機PoC、操作試作/試用、性能・費用・知識効果、独立反証、重要ADR採否。Critical 3/High 7は実証/処置/再審査待ち、No-Go継続。アプリ実装とClaude起動なし。


## 2026-10-25 正式一次設計審査 Round 2

- 対象commit: edcebcc650ec123913ac0407daa32aa2055349a5（改修PR #3）。全49blobのSHA一致を確認。
- 実行: Codex CLI 0.163.0-alpha.11、session 01a1716c-6fa8-74f3-b2e4-07032100a477、exit 0/turn.completed。ユーザーの全49file/OpenAI Codex CLI送信の明示承認後にstdin全文方式で実行。最初の送信処理は自動承認レビューに拒否され回避せず停止した。
- 判定: No-Go継続、新規Critical 0/High 4/Medium 1。前回10指摘を個別に仕様上解消/部分改善と評価。実証待ちは記述欠陥と分離し、既存Criticalを根拠なしに閉鎖しない。
- 所見: 分類継承/最終payload、再開計算の依存、Verified縦断契約、非信頼Markdown表示、review証拠/追跡の束縛。ISSUE-011/013/014/015/016へ統合、017とADR-017は未採用提案。
- 反証: CLI原文R2-05のclaude_complete/started=false疑義は親の2fixtureで拒否され撤回。別の2gate見逃しと2design見逃しを実測。原文・訂正・probe結果を保存し、validatorコードは修正しない。
- 検査: 対象commitで文書検査2本exit 0、12validatorケースOK。保存後の検査はreviews/codex/round-2/VALIDATION.md。これらは製品37TESTの実証ではない。
- 履歴: Round 1本文/実行証拠を元bytesのままarchive、最新REVIEW/execution/state対象をRound 2へ対応。phaseはcodex_review_recorded、人間/設計承認pendingを維持。
- 独立性/未実施: 同系列Codex再審査で盲検独立反証ではない。UI操作/実機PoC/性能/効果/Claude/アプリ実装は未実施。重要ADR採否と実証・独立反証は次の判断待ち。

## 2026-10-25 CR-002 実装前の仕様改善

- 依頼：実装なしで確認できる設計を改善し、実装依存事項は実装後に確認して設計を改良する。途中の「次のステップ」への回答はこの作業を継続する前提。
- 改修元：6977c21930b2541b27bfc9b47468c9423ef2a2c8（再審査PR #4）。全60 source blobをGitHub SHA照合。
- 変更前影響/3案/費用/反証/移行：DESIGN_REMEDIATION_2へ先行記録。重要方式は仕様候補、人間の個別採用や運用許可を捏造しない。ADR-018は検証時期の利用者指示を反映。
- 改善：job taint/最終送信、resume/fork/pure-effect/ledger、検証operation/証拠採用、plain text表示/exportをAPI/DB/Knowledge/Agent/画面/要件へ同時反映。実装後の37計画を全件not_runで担当/期待値/証拠/差戻し先付き登録。
- 段階：G5-D仕様審査→別のI許可→実装→G5-R実証/有効化→失敗から再設計。実装後試験を未実装設計の前提にする循環を除去、最終安全性検証を省略しない。
- 文書検査器：主試験交換/省略画面ID、API/entity、active本文/raw/execution/source digest/対象/session/phaseを照合。R2-05の実測見逃しを負例として固定。検査器は製品アプリではない。
- 確認：両文書検査と28 validatorケースを実行し合格。最終保存候補の実出力はreviews/codex/cr-002/VALIDATION.md。配色token24組は計算上候補4.5以上（最小4.863）。実render/a11y適合ではない。
- 未実施：正式な追加Codex CLI再審査、独立Claude反証、アプリ実装、37実機試験、interview/重要方針の個別人間採否。過去REVIEW/execution/全証拠は不変、review-state承認flag変更なし。

## 2026-10-28 CR-003 添付反証への修正

利用者依頼に基づきPR #5のローカル取得版を改修。DESIGN_REMEDIATION_3とADR-019/020に影響/比較/費用/反証/移行を先行記録。認証所有要件（28件目）、認証/一覧API/データ/画面契約、S/HとRの分離、slice追跡、効果標本設計、保持文を更新。検査器のM7見逃しを相互照合で修正し回帰試験を追加、現行source未審査を警告。

検証結果はreviews/cr-003/VALIDATION.mdへ実出力を保存。歴史的REVIEW/CLI証拠は不変、正式な新CLI審査/独立Claude/本体実装/37実機試験/S/H/人間採用は未実施。GitHubへの書込は実施していない。
