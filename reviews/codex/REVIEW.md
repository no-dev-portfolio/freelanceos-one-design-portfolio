# FreelanceOS ONE 4.0 正式一次設計審査 Round 2

**判定：No-Go継続。新規の記述欠陥はCritical 0件／High 4件／Medium 1件。前回Critical 3件／High 7件は、下記の仕様上の改善評価とは別に、必要な実証・人間処置が未完了である。**

## 1. スコープと証拠の限界

| 項目 | 内容 |
|---|---|
| 対象commit | `edcebcc650ec123913ac0407daa32aa2055349a5` |
| 対象 | 改修PR #3のheadとして提供された全49ファイル |
| 審査日 | 2026-10-25 |
| 審査主体 | Codex。同系列Codexによる一次設計再審査 |
| 方法 | 提供された行番号付き全文に対する静的審査 |
| 取得・一致確認 | 親CodexがGitHub connectorで固定取得し、全49blob SHA一致を確認したとの提供情報に依存 |
| 実行主体の識別 | 本回答からCLI version・session ID・終了状態を独立確認していない。親側の実行証拠で補完が必要 |
| 保存予定 | `reviews/codex/REVIEW.md`。前回REVIEWとexecutionは履歴としてarchive予定 |
| 独立性 | 独立Claude反証ではない。既存所見と改修対応表を読んだ再審査であり、盲検レビューでもない |

共通協定、START_HERE、審査指示、テンプレート、全設計、既存審査記録、検査コード、文書ストーリーボードを提供本文で確認した。GitHub直接読取、ローカルファイル読取、コマンド実行、画面操作、実機PoCは行っていない。アプリ実装、DB migration、AWS操作、仕様・検査コードの修正も行っていない。

親実測の文書検査結果を末尾に転載する。これは本審査者自身の実行結果ではない。37 TESTは受入試験の**計画**であり、動作合格実績は提供資料上0件である。検査器の12ケースとは別集計とする。

本書のIssue・ADR・REVIEW_LOGへの記載は追記提案であり、台帳更新を実行したとは主張しない。保存と履歴参照の修正後には、親側で検査を再実行する必要がある。状態の自動昇格、Issue閉鎖、人間採否の代行はしない。

## 2. 前回F-01〜F-10の処置評価

「仕様上解消」は前回の記述欠陥が補修されたという意味であり、実機安全性やIssue閉鎖を意味しない。旧commitの引用行番号を現commitの欠陥根拠として流用しない。

| 前回 | 今回評価 | 現commitの根拠と評価 | 残る退出証拠 |
|---|---|---|---|
| F-01 Critical：Vault CAS | **部分改善** | `docs/03-architecture/SYSTEM_DESIGN.md:20–28`はrenameをCAS扱いせず、非協調・未検証writerで適用を拒否する。旧事故経路を提供条件から外した点は改善。全writer協調をどう確立するかは未選定 | ADR-008の方式・環境選択、TEST-KB-010。ISSUE-001/008継続 |
| F-02 Critical：失効・公開・復元 | **仕様上解消** | `SYSTEM_DESIGN.md:30–38`で受付commit、公開permitとの直列化、非公開buffer、復元時の最新台帳合成を定義。外部変更gap・既送信限界も明記 | TEST-KB-011、保証境界の人間受容、保持・復元訓練。ISSUE-002等継続 |
| F-03 Critical：分類・推論経路 | **部分改善** | `docs/04-knowledge/KNOWLEDGE_MODEL.md:74`で分類統一・未知deny、`SYSTEM_DESIGN.md:18`でP0最小local経路と未成立時Blockedを明記。P0/P1矛盾は補修。モデル成立性は未確認 | local能力PoC、TEST-AI-009。派生データの分類契約はR2-01として追加 |
| F-04 High：承認消費・取消 | **仕様上解消** | `docs/03-architecture/API_CONTRACT.md:46–49`で不変envelope、一回claim、operation・監査との同一transaction、取消との行lockを定義 | TEST-AI-007/UX-006、正規化仕様の詳細化と競合実証 |
| F-05 High：永続復旧 | **部分改善** | `docs/05-agent/AGENT_AND_TOOLS.md:36–49`と`DATA_MODEL.md:18–20`でattempt・lease・fencing・OutcomeUnknownを補修。成功step再利用時の有効性判定は不足 | TEST-AI-008、R2-02の依存関係再検査 |
| F-06 High：知識権威 | **仕様上解消** | `DATA_MODEL.md:31–35`、`KNOWLEDGE_MODEL.md:68–74`でID、保存状態、検証hash、属性権威、候補隔離を統一 | TEST-KB-012、移行dry-run。Verifiedへ至る実用導線はR2-03 |
| F-07 High：UX導線 | **部分改善** | `docs/02-ux/SCREEN_SPEC.md:43–63`に全画面の復帰・通信断・mobile・a11y条件を追加。IAの画面IDと評価入口も補修 | 操作可能試作、利用者試験、コントラスト・読み上げ・keyboard実測 |
| F-08 High：評価契約 | **仕様上解消** | `docs/04-knowledge/GROWTH_EVALUATION.md:23–29`で同corpus、paired比較、系列split、盲検採点、固定閾値、失敗込み分母を定義 | TEST-EVAL-004、事前登録値、価値・確認工数の実測 |
| F-09 High：local運用境界 | **部分改善** | `API_CONTRACT.md:6–10`、`SYSTEM_DESIGN.md:16/38–40`、`AGENT_AND_TOOLS.md:49–51`で認証、最小権限、予算予約等を具体化。保持・鍵・RPO/RTOは明示的blocker | TEST-SEC-001/OPS-004、運用値・責任者決定。表示境界はR2-04 |
| F-10 High：検査・成果物・段階 | **部分改善** | 検査2本、12正負ケース、template、state、追跡表が存在し、試作未作成とStage依存を正確化。旧「欠落・実行不能」は解消 | R2-05の状態・証拠束縛、Round 2保存後検査、操作試作と人間処置 |

前回10件をそのまま新規10件として再計上しない。改修は設計記述として実質的に前進している。一方、必要PoCや人間受容がないため、既存Criticalを閉鎖できる状態ではない。

## 3. 上位10課題

今回の新規課題は**5件**とする。費用は設計・検証・保守負担の相対仮説であり、実測工数ではない。以下の受入値は試験条件内の目標である。

### R2-01 High：派生データの分類継承と、同意対象となる実送信payloadの対応が未定義

**根拠**

- `docs/03-architecture/DATA_MODEL.md:24`はconsentをpreview hashに束縛する。
- 同`:31–32`はノートの最終権限をDB・policy・本文分類の厳格側とする。
- `docs/05-agent/AGENT_AND_TOOLS.md:49`は全egressとpublic限定を要求する。
- `docs/03-architecture/API_CONTRACT.md:38/47`はegress preview hashを持つが、複数入力から生成したprompt・要約・tool結果・添付変換物の分類と、実送信bytesをpreviewへ束縛する規則がない。

**事故例・反証可能な主張**

publicの依頼とconfidentialノートからlocal生成した要約を、新規のpublic成果物としてCloudへ送る。全通信がegress gateを通っても、派生物の分類が入力の制約を失えば漏洩する。またpreview後にadapterが追加した会話・添付・provider固有項目が同意対象から外れ得る。

これはgateの存在不足ではなく、**gateが判定する分類とpayloadの生成契約不足**である。実装が入力制約を伝播し、最終送信内容を同意へ完全対応付けできれば反証できる。

| 比較案 | 費用仮説 | 効果・新リスク・旧案が優れる条件 |
|---|---|---|
| A：派生物に入力依存・分類・policy版を継承し、最終egress envelopeへ同意を束縛 | 中〜高 | 判定を追跡できる。依存漏れと過剰分類で停止が増える |
| B：非public入力に触れたjob全体をCloud不可に固定 | 低〜中 | 単純で初期PoC向き。無害な派生物まで送れず利便性が下がる |
| C：現契約を維持しCloudを提供しない | 低 | local限定なら送信事故面を縮小できる。Cloud機能の成立証拠にはならない |

推奨は初期B、必要性を確認してA。現案は全入力が事前確定したpublicだけの隔離実験なら簡潔である。分類引下げは別の明示的な人間判断とし、LLMによる「秘密を除去した」という自己申告だけでpublic化しない。

**検証・受入条件**

TEST-AI-009の子ケースとして、混在入力→要約→export→再添付→Cloud、過去会話の自動付加、adapterによるpayload追加、同意後の入力差替えを試す。架空canaryの未許可送信0件、最終payloadと同意対象の対応記録、取消後の未送信停止を保存する。未実施。

**影響・処置**

- REQ：AI-002/004、KB-003、OPS-002。
- SCREEN：SCR-00/03/07/08/09。実送信対象と分類由来を説明。
- API：`/consents`、`/actions`、`/attachments`、`/exports`。
- DB：consents、actions、publication dependencies、派生物の分類・由来。
- Knowledge：sourceから派生物までの制約継承。
- Agent：prompt構築・adapter変換後の最終gate。
- TEST：AI-002/009、OPS-002。
- Issue/ADR：ISSUE-011/015へ統合、ADR-010/015を補足。
- 人間採否：Cloud提供範囲、分類引下げ権限、同意previewの粒度。採否pending。
- 移行：分類由来不明の既存派生物はdeny。旧同意を新envelopeへ自動転用しない。

### R2-02 High：再開時に成功stepを無条件保持すると、訂正済み入力や失効依存を使った計算が残る

**根拠**

- `docs/03-architecture/DATA_MODEL.md:18`は成功済みstepを再実行しない。
- `docs/05-agent/AGENT_AND_TOOLS.md:44/47`も新attemptで成功stepを保持する。
- `docs/03-architecture/API_CONTRACT.md:22`のresumeはstate versionと照合参照が中心。
- `docs/02-ux/SCREEN_SPEC.md:15/50`は計画変更要求と成功step保持を提供する。
- 公開時の失効再検査は`SYSTEM_DESIGN.md:33`にあるが、計画・入力・モデル・tool変更時のstep成果物再利用判定は定義されない。

**事故例・反証可能な主張**

架空SQLケースの入力訂正後、失敗した後段だけ再開する。前段の集計結果は旧入力に基づくが、成功扱いで再利用され、誤った差分を回答する。失効時には公開gateが止められても、古い依存を捨てて再計算する経路がないと復旧不能になる。

成功した**副作用の再送防止**と、純粋計算結果の**キャッシュ有効性**を同じ規則で扱っている点が問題である。

| 比較案 | 費用仮説 | 効果・新リスク・旧案が優れる条件 |
|---|---|---|
| A：stepごとに入力・plan・tool・model・policy・知識依存を記録し、有効な結果だけ再利用 | 中〜高 | 訂正後の再計算が可能。依存グラフと無効化が複雑 |
| B：resumeは不変入力の継続だけ。変更は新jobへ分岐 | 低〜中 | 契約が明快。履歴と成果物の引継ぎ操作が増える |
| C：初期は自動resumeを制限し、人が再利用可能stepを照合 | 中 | 実装面を縮小できる。確認負担と判断ミスが増える |

推奨はBを初期契約とし、副作用operationは引き続き一回性を守る。現案は入力・plan・実行条件が完全不変の障害再開なら適する。

**検証・受入条件**

TEST-AI-008に、成功step後の入力訂正、tool版変更、知識失効、同一入力の単純worker再起動を追加。古い計算結果の無条件採用0件、完了済み副作用の自動重複0件、失効依存を除いた再計画または説明付きBlockedを確認する。未実施。

**影響・処置**

- REQ：UX-002/004、AI-003/005、KB-006/007/008。
- SCREEN：SCR-02/03/08。継続と新job作成を区別。
- API：resume、job/plan変更、operation照会。
- DB：job_stepsの依存fingerprint、plan版、成果物有効状態。
- Knowledge：失効依存を持つ中間成果物の無効化。
- Agent：純粋計算の再計算と副作用再送の分離。
- TEST：AI-008、UX-002/004、KB-011。
- Issue/ADR：ISSUE-013へ統合、ADR-012を補足。
- 人間採否：resumeで許す変更範囲。採否pending。
- 移行：依存が不明な成功結果は自動再利用不可。監査履歴は保持する。

### R2-03 High：候補を技術検証しVerifiedへ進める縦断契約が不足する

**根拠**

- `docs/04-knowledge/KNOWLEDGE_MODEL.md:70–72`はReviewed→Verifiedに証拠・hash一致を要求する。
- `docs/03-architecture/DATA_MODEL.md:12`はknowledge_validationsを持つ。
- `docs/05-agent/AGENT_AND_TOOLS.md:15/53`は固定のapproved_test_idと架空datasetだけを許可する。
- `docs/03-architecture/API_CONTRACT.md:28–34`には候補・再提出・action・承認があるが、検証要求、試験結果採用、validation失効・更新の契約がない。
- `docs/02-ux/SCREEN_SPEC.md:27`は「再検証」を操作として挙げるが、対象hash・試験適合性・結果採用者・復帰先を定義していない。

**事故例・反証可能な主張**

候補の文言を編集した後、旧hashに対する成功試験を添付する、または無関係な固定試験の成功を使ってVerifiedにする。反対に、安全に昇格できる操作がなければ候補は通常検索へ戻らず、仕事→知識→再利用の価値ループが停止する。

承認と検証の概念分離は正しく補修された。残る問題は、その状態遷移を実行する製品契約である。

| 比較案 | 費用仮説 | 効果・新リスク・旧案が優れる条件 |
|---|---|---|
| A：検証専用operationを定義し、対象hash・scope・試験版・結果・採用者を束縛 | 中〜高 | 閉ループが成立しやすい。試験と主張の適合性管理が必要 |
| B：初期は人間による証拠審査・登録に限定 | 中 | 自動検証範囲を抑えられる。登録負担と誤認証リスクが残る |
| C：既存の検証済みcorpusのみ再利用し、新候補のVerified昇格を停止 | 低 | 検索比較を先行できる。自動成長のP0達成とは呼べない |

推奨はSQL件数不一致の一系列でA/Bを具体化する。現案は検証状態を参照するだけのread-only評価には適する。

**検証・受入条件**

TEST-KB-004/012に、承認のみ、旧hashの証拠、無関係な試験、失敗・timeout、scope違い、証拠失効、検証中の本文変更を追加。無効証拠によるVerified化0件。有効証拠なら正しいhashだけが検索可能になり、SCR-05で根拠を追えること。未実施。

**影響・処置**

- REQ：KB-002/004/008、EVAL-002。
- SCREEN：SCR-03/05/07/08。
- API：検証要求・状態・証拠採用の契約追加候補。既存APIへの暗黙実装は避ける。
- DB：knowledge_validations、evidence、候補hashと検証operationの対応。
- Knowledge：assertion_type別の証拠適合性と再検証。
- Agent：試験実行とVerified採用権限の分離。
- TEST：KB-004/012、EVAL-002。
- Issue/ADR：ISSUE-014へ統合、ADR-013を補足。
- 人間採否：誰がどの証拠を採用できるか、初期に対応する主張の種類。採否pending。
- 移行：既存Verifiedの証拠適合性不明なら再審査し、自動昇格しない。

### R2-04 High：非信頼MarkdownをUI・exportへ表示する際の実行可能コンテンツ境界がない

**根拠**

- `docs/04-knowledge/KNOWLEDGE_MODEL.md:55–56/74`は本文を非信頼データとするが、主にLLMへの命令とtool引数を扱う。
- `docs/02-ux/SCREEN_SPEC.md:18/21/27/30`はヒット箇所、本文、差分、ログを表示する。
- `docs/03-architecture/API_CONTRACT.md:6`はsession・CSRF・Originを定義するが、Markdown/HTML描画、外部画像、リンクscheme、export描画の制約がない。

**事故例・反証可能な主張**

取得ノートに埋め込まれたHTMLや外部画像を表示して、画面表示だけで外向き通信が発生する。危険なリンクschemeや描画器のHTML許可により、所有者sessionのあるUIで意図しない操作を誘発する可能性もある。

実際のXSS成立を確認したわけではない。**非信頼本文の表示方式が未指定で、全egress gateと認証境界を描画経路へ適用できるか判断できない**という設計欠陥である。

| 比較案 | 費用仮説 | 効果・新リスク・旧案が優れる条件 |
|---|---|---|
| A：許可Markdown subset、HTML禁止・sanitize、危険scheme拒否、外部resource既定遮断 | 中 | 文書の読みやすさを保てる。parser更新・許可属性管理が必要 |
| B：初期は本文・差分をplain textで表示 | 低 | 実行可能描画を大幅に減らせる。表・コードの可読性が下がる |
| C：隔離sandbox viewerを使い、resource取得もpolicy経由 | 中〜高 | 表現力を残せる。frame・通信・exportの境界管理が増える |

推奨は初期B、必要な範囲でA。現仕様のままでも、実装が既に完全なplain text描画に限定されるなら追加機構は小さくてよいが、その制約を明記する必要がある。

**検証・受入条件**

TEST-SEC-001/AI-009の子ケースとして、raw HTML、event属性、危険scheme、外部画像、SVG、差分・引用・エラーメッセージ内の同内容、exportを試す。script実行・未許可通信・secret露出0件を受入目標とする。未実施。

**影響・処置**

- REQ：AI-002、KB-001、UX-003/005、OPS-002。
- SCREEN：SCR-03/04/05/07/08。
- API：content・snippet・error・exportの安全な表現契約。
- DB：本文正本は維持。描画済み派生物の版管理を検討。
- Knowledge：Markdown本文を権限や実行コードにしない。
- Agent：LLM出力も同じ描画境界へ。
- TEST：SEC-001、AI-009、UX-005、OPS-002。
- Issue/ADR：新規Issue案として登録。ADR-015補足または表示境界の新ADR候補。
- 人間採否：許可する表現と外部resource取得範囲。採否pending。
- 移行：過去本文は書換えず、安全なrendererで再表示する。

### R2-05 Medium：検査基盤は状態・レビュー証拠・要件別追跡を十分に束縛しない

**根拠**

- `scripts/check_review_gate.py:47–61`はcommit文字列が本文のどこかにあること、見出し、executionのcommit・session・exit・terminal typeを検査する。
- 同`:77–86`はfalse側の参照禁止とphase側の参照必須を組み合わせている。このため`claude_complete`かつ`claude_started=false`は拒否される。CLI原文の見逃し疑義は、親側のfixture検証で反証され、欠陥根拠から除外した。
- `claude_started=True`でも、phaseが`codex_complete`以降であることを明示検査しない。
- `reviews/review-state.json:4–6`は旧commit・旧REVIEW・旧executionを指す。これは現時点では歴史資料として正しいが、Round 2本文へ置換すると参照の再構成が必要。
- `scripts/test_design_checks.py:45–60`には上記組合せや本文差替えの負例がない。

**事故例・反証可能な主張**

親側の検証では、`claude_complete`かつ`claude_started=false`はnull参照でも非null参照でも拒否された。CLI原文の当該疑義は誤指摘として撤回する。未検証の他の組合せで通ると推定してはならない。

一方、`phase=codex_review_recorded`のままhuman_acceptance=acceptedと存在する参照を置き`claude_started=true`にする矛盾状態は通過した。また、今回本文に旧commitを歴史説明として含めると旧state/旧executionとの組合せが通過し、active対象の取り違えを検出できなかった。これは本人性の保証問題ではなく機械的に確認できる対応関係の不足である。

補助検証ではcheck_designについても、UX-001/002の主試験を追跡表で交換する、`SCR-00/99`と未定義IDを省略表記へ混ぜる、の両fixtureがエラー0件だった。`check_design.py:50–72`は主試験の要件ごとの一致を見ず、`:65–81`のregexは省略後半IDを展開していない。Medium所見R2-05の検査基盤の範囲に統合する。

検査器が本人性を証明しない限界は明記済みであり、それ自体を欠陥とはしない。問題は機械的に確認可能な状態整合と成果物対応である。

| 比較案 | 費用仮説 | 効果・新リスク・旧案が優れる条件 |
|---|---|---|
| A：状態真理値表と構造化review metadata、本文digest・対象commitを対応付ける | 中 | 取り違えを検出しやすい。schema移行とdigest更新運用が必要 |
| B：Round別の不変ディレクトリとmanifestを作り、active参照だけ切替 | 低〜中 | 履歴を保ちやすい。active参照とリンクの更新漏れが残る |
| C：現検査を維持し、PRで人がmanifest・本文・executionを照合 | 低 | 単発・少人数なら軽い。反復時の取り違えを自動検出しない |

推奨はBと最小限のA。現案は単一Roundの構造検査としては有用であり、廃棄する必要はない。

**検証・受入条件**

状態の許可・禁止組合せ、異なるRoundの本文差替え、履歴中だけに対象commitがある本文、executionのdigest不一致、Claude baseline不一致を負例化する。許可状態は通過し、禁止状態・成果物取り違えは失敗すること。CLI自身は未実行。親側が実行した限定fixtureの結果は下記第8節とprobesに記録し、それ以外の負例は未実施。

**影響・処置**

- REQ：全27要件の審査証拠管理。製品要件の変更は不要。
- SCREEN/API/DB：製品仕様への直接変更なし。
- Knowledge/Agent：製品機能への直接変更なし。審査役割・独立性の記録を補強。
- TEST：検査器の追加負例。37製品TESTとは別管理。
- Issue/ADR：ISSUE-016へ統合、ADR-016を補足。
- 人間採否：Round履歴形式、active reviewの受理。採否pending。
- 移行：旧REVIEW・executionを対でarchiveし、旧ADR・IssueのF-01〜10参照が旧審査を指し続けるようにする。状態は自動昇格しない。

## 4. 全27要件の追跡審査

全要件はProposed。下表の「仕様あり」は動作合格を意味しない。API・DBの対応は`docs/08-governance/TRACEABILITY.md:7–33`も確認した。

略記：APIは`docs/03-architecture/API_CONTRACT.md`、DBは同`DATA_MODEL.md`、Knowledgeは`docs/04-knowledge/KNOWLEDGE_MODEL.md`、Agentは`docs/05-agent/AGENT_AND_TOOLS.md`。TESTは全て`TEST-`接頭辞を省略する。

| REQ | 設計・SCREEN | API／DB・強制点 | TEST計画／審査結果 |
|---|---|---|---|
| UX-001 | SCREEN_SPEC:47–57、00/01/02/04/06/10 | jobs/search/approvals、各projection | UX-001。5代表操作明記済み、試用待ち |
| UX-002 | SCREEN_SPEC:43/49–50、02/03/08 | events/operations、attempt・sequence | UX-002、AI-008。R2-02、動的操作待ち |
| UX-003 | SCREEN_SPEC:53–54、06/07 | decision、actions・approval消費 | UX-003/006、AI-007。対象固定改善、R2-04 |
| UX-004 | SCREEN_SPEC:47–57、00/03/07/09 | operation reason、jobs | UX-004/006。復帰表あり、理解・完遂試験待ち |
| UX-005 | SCREEN_SPEC:61、全11画面 | event通知、UI状態 | UX-005/006。a11y目標、実測なし |
| KB-001 | SYSTEM_DESIGN:16、00/04/05/09 | vault capability、root_identity | KB-001/010、SEC-001。実ファイル境界待ち |
| KB-002 | Knowledge:68–72、04/05/07 | knowledge、refs・validations | KB-002/012。属性権威改善、R2-03 |
| KB-003 | Knowledge:50、04/05 | search/get、ACL・epoch・hash | KB-003/011、AI-009。再認可仕様あり、R2-01 |
| KB-004 | Knowledge:70–72、03/05/07 | candidates、validations | KB-004/012。承認分離あり、R2-03 |
| KB-005 | SYSTEM_DESIGN:20–28、05/07 | actions/operations、write journal | KB-005/010、AI-007。未検証writer拒否、方式未選定 |
| KB-006 | SYSTEM_DESIGN:25–26/38–40、03/05/07/09 | reconcile、journal・attempt | KB-006/010、AI-008。障害注入待ち、R2-02 |
| KB-007 | SYSTEM_DESIGN:30–38、03/04/05/09 | revoke、revocations・publication | KB-007/011。線形化仕様あり、実証・境界受容待ち |
| KB-008 | Knowledge:50、03/05/08 | knowledge/get、sources・dependencies | KB-008/011。引用位置保持の計画、実一致待ち |
| KB-009 | Knowledge:53/59/72、05/07 | candidates、edges | KB-009/012。P1、矛盾比較UI・関係列挙詳細待ち |
| AI-001 | Agent:24/49/53、03/08/09 | actions、policy・tool gate | AI-001、SEC-001。注入・引数越権の実証待ち |
| AI-002 | Agent:49、00/03/07/09 | consents/settings、policy | AI-002/009。R2-01/04、local能力待ち |
| AI-003 | Agent:36–51、02/03/08/09 | cancel/resume、attempt・budget予約 | AI-003/008、OPS-004。R2-02、上限実証待ち |
| AI-004 | API:46–49、03/06/07 | decision、action envelope | AI-004/007。仕様上補修、競合実証待ち |
| AI-005 | Agent:43/47、02/03/08 | reconcile、tool_executions | AI-005/008。不明再送禁止、実証待ち |
| AI-006 | API:52、03/08/09 | P1 connector契約未承認 | AI-006。無効化を明記、P0完了と混同しない |
| EVAL-001 | GROWTH_EVALUATION:23–29、10 | evaluation-runs、frozen manifest | EVAL-001/004。比較契約改善、閾値・実測待ち |
| EVAL-002 | 同:25–29、05/10 | holdout隔離、validation証拠 | EVAL-002/004。系列漏洩破壊試験待ち |
| EVAL-003 | 同:27、08/10 | metrics・failures、evaluation_runs | EVAL-003/004。分母・計時定義あり、測定待ち |
| OPS-001 | SYSTEM_DESIGN:37–40、09 | backups/restores、manifest・tombstone | OPS-001/004、KB-011。鍵・値・復元訓練待ち |
| OPS-002 | DB:25、03/08/09 | exports、audit・evidence | OPS-002/004、SEC-001。R2-04、anchor運用待ち |
| OPS-003 | Agent:51、03/09/10 | settings、budget_reservations | OPS-003/004。P0最小制御とP1分析を分離、実測待ち |
| BIZ-001 | PRD:24、PHASES:13、03想定 | P1専用API・必須条件schema未決 | BIZ-001。P1保留は明記済み、専用設計が必要 |

価値・機能面では、`PRD.md:47`の架空SQL件数不一致に絞る方針は妥当な検証単位である。単一Planner、P1 connectorの無効化、Cloud OFFも範囲抑制に寄与する。

ただし、local推論、PostgreSQL、Evidence Store、協調writer、独自workflow、検証証拠管理を同時に成立させる負担は大きい。安全制御を削るのではなく、**一つの仕事で必要な最小経路を測り、不要な接続・モデル選択・検索方式の拡大を止める**べきである。手作業、既存Obsidian検索、提案ファイル方式と確認時間・復旧時間・費用を比較する。G0の利用頻度とG4の効果が不明なら、機能追加より対象仕事の再選定を優先する。

## 5. UX全導線・a11y・mobileの審査

文書ストーリーボードは存在する。操作可能UI試作ではなく、以下は机上確認である。

| 導線 | 今回の改善 | 残る確認 |
|---|---|---|
| 初回設定：00→09→00→01 | Cloud OFF、modelなしは閲覧、架空demoを区別 | 能力testの成功基準、失敗説明、keyboardで中断・再開 |
| 依頼：01→03 | 分類・model・費用・Plan、Draft保持 | R2-01の分類由来、長文・添付失敗時の入力保持 |
| 一覧・再開：02→03 | OutcomeUnknownと新attemptを区別 | R2-02の変更時分岐、archiveと取消の理解 |
| 実行・停止：03→08 | 停止要求と停止完了、sequence再取得 | 停止待ち中の操作、読上げ頻度、進捗停止の説明 |
| 検索：04→05 | 該当なしと索引不明を分離、存在秘匿 | 権限変更中・stale時の表示更新、R2-04 |
| 根拠：03/05→08 | 使用版・現在版・検証hash、失効時本文非表示 | 引用箇所への移動、証拠非表示時の説明 |
| 訂正・検証：05→07→08 | 元/現在/提案、再提出を定義 | R2-03の検証完遂、差戻し後の編集・保存 |
| 文脈内承認・承認一覧 | 同一projection、一括は閲覧だけ | 複数入口・複数tab・期限境界の同期 |
| 承認中通信断 | 同operation照会、新key再送禁止 | ブラウザ再起動後のoperation復元、照会不能の理解 |
| 同期競合・merge | 人の編集保持、新候補・新hash・新承認 | 競合再発、3-way diffの読解、全writer条件の説明 |
| 障害照合：02/03→08 | 既知効果と人間の証拠入力 | 「照合済み」を誤って確定しない入力・確認設計 |
| 設定往復：09→元作業 | return_to・Draft保持、policy縮小再認可 | 他tabの旧設定、未送信・送信済みの区別 |
| 復元：09 | manifest・鍵・台帳、隔離と別公開承認 | RPO/RTO値、公開承認の対象集合と操作契約の詳細 |
| 評価：10 | 未実施、分母、条件、CI、旧run不変 | 盲検採点・失敗例への到達、比較不能条件の表示 |
| 監査export：08 | マスクpreview・保存結果 | APIのjob単位指定と画面の対象期間指定の整合、R2-04 |
| mobile承認 | 確認不能なら停止、remoteは未提供 | 320pxだけでなくzoom・横スクロール・PC引継ぎの実操作 |
| P1 SQL・案件評価 | 別契約まで無効 | 未提供機能を利用可能に見せない表示 |

WCAG 2.2 AAは目標のままであり、適合判定はできない。少なくともフォーカス順、dialog復帰、エラー関連付け、読み上げ、文字拡大、差分の意味構造、状態通知、色以外の識別を操作試作で確認する必要がある。

`SCREEN_SPEC.md:61`の「確認できなければ承認button無効」は安全側だが、判定方法が未定である。画面幅のみやスクロール完了だけで理解を推定せず、必要情報へアクセスできる構成と利用者試験を組み合わせる。秘密をlive通知で読み上げない条件は維持する。

## 6. 検査基盤・評価・動作実績

親提供の対象commitに対する実測では、両検査と検査器12ケースは成功している。前回のscript欠落・exit 2は旧commitの事実であり、現commitの検査不能として扱わない。

| 区分 | 確認できること | 確認できないこと |
|---|---|---|
| check_design | 必須成果物、27要件、37計画、11画面、追跡・リンクの一部 | 設計内容の正しさ、API/DBの完全な意味整合 |
| check_review_gate | 許可phase、参照、一定のexecution書式、人間受容欄 | 本人性・独立性・承認真正性、R2-05の取り違え全般 |
| 12 validator tests | 提供した正負fixtureで検査器が期待どおり応答 | 製品の37 TEST、安全性、UX、性能 |
| 37 TEST計画 | 受入シナリオの存在 | 実行・合格。提供資料上は合格0件 |
| 評価設計 | 系列split、固定条件、分母、採点契約 | 知識成長、時間削減、費用対効果 |
| 文書storyboard | 状態遷移・文言の机上確認 | 実操作、a11y適合、初回成功率 |

コード静読上、`check_design.py:65–81`はSCREEN列の参照を検査するが、API列・DB列の識別子を各定義へ意味照合しない。`:84–94`のMarkdownリンク検査はhidden directoryを除外し、anchorの存在も検査しない。これは直ちに安全欠陥ではないが、「追跡確認済み」の範囲を限定すべきである。

評価計画は大きく改善された。なお、閾値・許容劣化・停止基準・計時点は値を決めるまで探索段階である。20〜100例や5名は仮案であり、効果や90%成功率の達成根拠ではない。local推論の能力不足、承認工数、復旧負担を失敗として評価に含める必要がある。

## 7. 未解決事項・人間判断・引継ぎ

**No-Goを維持する。** 新規Criticalを検出しなかったことは、既存Criticalの解消実証を意味しない。ISSUE-001/002/011は必要な方式選定・実機証拠・保証境界の受容が未完了であり、根拠なく閉鎖しない。

親側への記録提案は次のとおり。

| 記録先 | 追記内容 |
|---|---|
| ISSUES | R2-01を011/015、R2-02を013、R2-03を014、R2-05を016へ統合。R2-04は新規Issueとして衝突確認後に採番 |
| DECISIONS | ADR-010/012/013/015/016へ本書の比較案・反証・移行を補足。重要判断はProposedを維持 |
| REVIEW_LOG | 対象commit、全文静的審査、前回処置表、新規High 4/Medium 1、親検査と審査者未実行の区別、No-Goを記録 |
| 履歴・state | 前回REVIEW/executionを対でarchive。旧F番号参照を保持し、今回本文・execution・manifestを対応付ける。phaseは自動昇格しない |

人間の採否が必要なのは、writer方式・対応環境、local推論の提供条件、失効保証境界、分類引下げ権限、resumeで許す変更、検証証拠の採用権限、表示可能なMarkdown範囲、保持・鍵・RPO/RTO、実験閾値である。Highを残すなら明示的リスク受容と範囲隔離が必要である。

次の作業は、記述欠陥の補修提案を採否し、架空データ・対象環境・期限・停止条件を固定した隔離PoC計画を作ること。PoC開始、G5設計承認、アプリ実装は別々の許可とする。Claude反証は、一次審査受理と前提充足後、人間の指示に従う別セッションで行う。本書はその代行ではない。

### 末尾添付：親Codexが実行した検査結果

以下はユーザー提供の親実測記録を転載したもの。本審査者自身は実行していない。対象はRound 2本文保存前のcommitであり、保存・archive・参照更新後の検査結果ではない。

```json
{
  "platform": "macOS-27.0.1-arm64-arm-64bit",
  "base_commit": "edcebcc650ec123913ac0407daa32aa2055349a5",
  "checks": [
    {
      "command": "python3 scripts/check_design.py",
      "exit_code": 0,
      "stdout": "PASS: design structure {'requirements': 27, 'test_plans': 37, 'screens': 11}\nLIMIT: no runtime, UX, safety, reviewer identity or human acceptance verified\n",
      "stderr": ""
    },
    {
      "command": "python3 scripts/check_review_gate.py",
      "exit_code": 0,
      "stdout": "PASS: review metadata {'phase': 'codex_review_recorded', 'human_acceptance': 'pending', 'design_approval': 'pending'}\nLIMIT: artifact shape only; identity, independence, PoC and approval authenticity not verified\n",
      "stderr": ""
    },
    {
      "command": "python3 -m unittest discover -s scripts -p test_design_checks.py",
      "exit_code": 0,
      "stdout": "",
      "stderr": "............\n----------------------------------------------------------------------\nRan 12 tests in 0.595s\n\nOK\n"
    }
  ]
}
```

## 8. 親Codexによる実行確認・訂正・保存記録

### 実行主体と送信承認

Codex CLI `0.163.0-alpha.11` / session `01a1716c-6fa8-74f3-b2e4-07032100a477` / exit 0、turn.completedを親Codexが確認。対象commitの全49blobをGitHub connectorで固定取得したmanifestとSHA一致させ、行番号付き本文をstdinへ入力した。stdin送信は一度自動承認レビューで拒否され、回避せずに停止。ユーザーが「全49ファイルをOpenAI Codex CLIへ送信して再審査」を明示承認した後に実行した。

CLIは直接file読取や実機操作をしていない。今回の審査は改修を行った同系列Codexによる再審査であり、独立/盲検/Claude反証とは主張しない。原文は [CLI_REVIEW_RAW](round-2/CLI_REVIEW_RAW.md)、入力対象は [source-manifest](round-2/source-manifest.json)、実行情報は [execution](execution.json)。

### 原文R2-05への反証と訂正

CLI原文はclaude_complete/claude_started=falseの矛盾状態を見逃す疑義を挙げたが、親側fixtureではnull/non-null両方とも拒否された。この部分を誤指摘として本本文から除外し、原文は不変保存した。残る証拠束縛の欠陥と、実測した検査の見逃しはR2-05へ統合した。製品/validatorコードの修正は今回行っていない。

| 親側限定fixture | 結果 |
|---|---|
| claude_complete + started=false + null refs | 拒否。原文の疑義を反証 |
| claude_complete + started=false + 非null refs | 拒否。原文の疑義を反証 |
| codex_review_recorded + human accepted + started=true + 存在ref | エラー0件で通過。状態組合せの見逃し |
| Round 2本文+旧commitの歴史記述、旧state/execution | エラー0件で通過。active成果物の取り違えを見逃し |
| UX-001/002主試験を追跡表で交換 | エラー0件で通過。要件別主試験不一致の見逃し |
| SCR-00/99を追跡表へ挿入 | エラー0件で通過。省略表記内の未定義画面を見逃し |

すべて一時コピー上のvalidator試験であり、Claudeを実際に起動したものでも、製品の実機PoCでもない。生の結果は [gate-probes](round-2/gate-probes.json) と [design-probes](round-2/design-probes.json)。通常の12ケースOKと追加probeの見逃しを相殺せず別記する。

### 保存と状態

前回審査と実行証拠は [Round 1](round-1/REVIEW.md) に対でarchiveし、元bytesを保持した。現在のREVIEW/execution/state対象は本commitへ揃えるがphaseはcodex_review_recorded、人間受容/設計承認pending、Claude/実装falseを維持する。旧F-01〜10とCR-001の参照はRound 1へ固定する。ISSUES/ADR/REVIEW_LOGへ処置を追記し、仕様/実装や検査コードは変更しない。

保存後の検査結果は [ROUND2_VALIDATION](round-2/VALIDATION.md) を参照。通常検査合格と37計画の動作未実施を分離し、既存Criticalの閉鎖・設計承認・実装許可は行わない。
