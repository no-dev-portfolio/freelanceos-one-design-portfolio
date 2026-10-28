# FreelanceOS ONE 4.0 — 設計・反証レビュー対応ポートフォリオ

仕事→検証→知識→再利用の閉ループを目指す、自主制作の設計資料と文書検査コードです。アプリ本体は未実装です。

- 公開先: https://github.com/no-dev-portfolio/freelanceos-one-design-portfolio
- 公開版: CR-003 / 2026-10-28、Private作業ブランチcommit `9d5785f1a7c4b84299bebff2b394f32a5aa2c785` からのコピー。
- 28要件、37試験計画、11画面。文書検査2本とvalidator回帰テスト51件を確認済み。
- 認証・CSRF・一覧API、機密由来の分類継承、承認と一回実行、知識の検証・失効、設計追跡を扱います。
- 製品の動作・安全性・知識効果は未実証。37件の製品試験、spike、聞き取り、重要方針の人間採否は未実施です。

## 検査の実行

Python 3.9以上（外部パッケージ不要）。リポジトリのルートで実行します。

```sh
python3 scripts/check_design.py
python3 scripts/check_review_gate.py
python3 scripts/test_design_checks.py
```

審査ゲートのWARNは、過去の正式レビュー対象と現行設計が異なることを示す意図した警告です。PASSは歴史記録の整合性であり、現行設計の承認ではありません。

## 読む資料

- [反証への対応表](reviews/cr-003/REMEDIATION.md)
- [検証実出力](reviews/cr-003/VALIDATION.md)
- [製品要求](docs/01-product/PRD.md)
- [API契約](docs/03-architecture/API_CONTRACT.md)
- [要件から画面・API・試験・実装段階への追跡](docs/08-governance/TRACEABILITY.md)
- [実装前の成立性調査計画](docs/06-quality/FEASIBILITY_SPIKES.md)

元のPrivateリポジトリと履歴は公開せず、本リポジトリへ公開用コピーだけを登録しています。下記の元資料で「ローカル修正版」「GitHub未反映」とある箇所は、CR-003作成時点の履歴です。公開は設計承認・アプリ実装許可・本番運用許可ではありません。機密情報と実顧客データは含めません。

---

# FreelanceOS ONE 4.0 — 設計改修候補 v0.11

ITフリーランスの仕事→検証→Obsidian知識→再利用を支援し、未知タスクへの効果と人間の確認工数を測る設計資料。

**状態：DESIGN ONLY / CR-002仕様改修、再審査・人間判断待ち。** 最新の正式Round 2のNo-Goは旧対象commitの歴史記録。今回、実装なしで確認できる記述不足を改善し、実装依存試験は実装後に実施して設計を改良する計画へ分離した。実装・実運用の許可や実証合格ではない。Claude/アプリ実装は開始していない。

## 読む順序
1. [今回CR-002の影響・ADR比較](docs/08-governance/DESIGN_REMEDIATION_2.md) / [前回CR-001](docs/08-governance/DESIGN_REMEDIATION.md)
2. [PRD](docs/01-product/PRD.md) / [27要件](docs/01-product/REQUIREMENTS.md)
3. [画面仕様](docs/02-ux/SCREEN_SPEC.md) / [文書ストーリーボード](wireframes/STORYBOARD.md)
4. [基本設計](docs/03-architecture/SYSTEM_DESIGN.md) / [API](docs/03-architecture/API_CONTRACT.md) / [データ](docs/03-architecture/DATA_MODEL.md)
5. [知識](docs/04-knowledge/KNOWLEDGE_MODEL.md) / [成長評価](docs/04-knowledge/GROWTH_EVALUATION.md) / [Agent](docs/05-agent/AGENT_AND_TOOLS.md)
6. [検証計画](docs/06-quality/VERIFICATION_PLAN.md) / [要求追跡](docs/08-governance/TRACEABILITY.md)
7. [一次審査](reviews/codex/REVIEW.md) / [改修対応表](reviews/codex/REMEDIATION.md) / [ISSUES](docs/08-governance/ISSUES.md) / [ADR](docs/08-governance/DECISIONS.md)
8. [START HERE](handoff/START_HERE.md) / [レビュー手順](reviews/README.md)

## 設計候補の原則と未決
本文正本はMarkdown、業務/権限/失効/検証証拠はDB。Cloud default OFF、分類不明はdeny、未検証writerは適用不可。hash読取+renameだけでCAS成立とはしない。承認対象・公開判定・復旧・予算を確定的gateで強制する設計。

重要方式ADR-008〜017は個別採否待ち。ADR-018は利用者指示による検証時期の分離を反映（実装/運用許可ではない）。P0安全更新は削除しない。writer方式、最小local推論の実用性、失効境界、保持/鍵/RPO/RTO、評価閾値の人間採否と実機証拠が必要。変更前の一次REVIEWと実行証拠はRound 1 archiveへ元bytesのまま保持。最新REVIEWはRound 2を示す。

## 検査と限界
```
python3 scripts/check_design.py
python3 scripts/check_review_gate.py
python3 -m unittest discover -s scripts -p 'test_design_checks.py'
```
リンク・必須成果物・27要件と37試験計画・追跡・審査状態の構造を検査する。内容の正しさ、reviewer本人性、実機安全性、UI適合、知識成長、人間承認は証明しない。

文書storyboardはあるが動的UI/実機/性能/効果は未実施。[実装後確認・設計改良計画](docs/06-quality/POST_IMPLEMENTATION_VALIDATION.md) と37件のverification-registerへnot_runで登録した。G5-Dは仕様審査、Iは別の実装許可、G5-Rは実装後の機能有効化/運用受入。R未実施だけで文書改良を循環させず、結果から設計へ戻す。人間採否とinterviewも未取得を明示する。

[変更管理](docs/08-governance/CHANGE_CONTROL.md)、[レビュー履歴](docs/08-governance/REVIEW_LOG.md)、[状態記録](reviews/review-state.json)を参照。


詳細契約：[分類/再開/検証](docs/03-architecture/EXECUTION_CONTRACTS.md)、[非実行表示](docs/02-ux/CONTENT_PRESENTATION.md)。文書検査合格は、これらの実装が安全に動いた証拠ではない。

[次の手順](docs/07-delivery/NEXT_STEPS.md) に、仕様確認→範囲を決めた実装許可→実装→検証→設計改良を記載。

## CR-003 反証レビュー反映（2026-10-28 ローカル修正版 v0.12）

現行28要件（認証REQ-SEC-001を追加）・37試験計画・11画面。以前の27件は元版の数。修正内容は [CR-003](docs/08-governance/DESIGN_REMEDIATION_3.md) と [対応報告](reviews/cr-003/REMEDIATION.md)。検査コードの状態相互照合・画面method/path照合を追加。認証/一覧API、S/H調査、S1/S2追跡、標本設計を補完。

check_review_gateのPASSは歴史的Round 2記録の整合だけ。現行sourceと旧審査対象の差はWARNとして表示し、現行の正式審査合格とは扱わない。元PRはopen、今回GitHub未反映。実装許可false、運用受入pending、37試験not_run、数値候補/人間採否/S/H調査は未完了。
