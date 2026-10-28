# CR-002 実装前に確認できる設計の改善

日付: 2026-10-25 / 改修元commit: `6977c21930b2541b27bfc9b47468c9423ef2a2c8` / 対象審査: Round 2（審査対象 `edcebcc650ec123913ac0407daa32aa2055349a5`）。

## スコープと利用者指示

実装なしで確認できる仕様・整合性・手順・評価基準を改良する。実装が必要なものは、実装後に試験し、その結果で設計を再改良する。これは今回の実装開始許可・実運用承認ではない。アプリ、migration、AWS、Claude反証には着手しない。文書検査器はアプリではなく設計資料の保守用として修復する。

## 変更前影響分析

| 所見 | REQ | SCREEN | API / DB / Knowledge / Agent | TEST |
|---|---|---|---|---|
| R2-01 | AI-002/004,KB-003,OPS-002 | 00/03/07/08/09 | 派生分類・job taint、最終egress envelope/同意、不明由来deny | AI-002/009,OPS-002 |
| R2-02 | UX-002/004,AI-003/005,KB-006/007/008 | 02/03/08 | 不変jobのresume、訂正はfork、純粋計算と副作用ledgerを分離 | AI-008,UX-002/004,KB-011 |
| R2-03 | KB-002/004/008,EVAL-002 | 03/05/07/08 | validation operation、主張/試験適合/対象hash、技術証拠と人確認を分離 | KB-004/012,EVAL-002 |
| R2-04 | AI-002,KB-001,UX-003/005,OPS-002 | 03/04/05/07/08 | 初期plain text、HTML/外部resourceなし、text export、安全URI操作 | SEC-001,AI-009,UX-005,OPS-002 |
| R2-05 | 全27要件の証拠 | 製品画面変更なし | 本文digest/対象commit/実行証拠/phase/要件別主試験/画面IDの検査 | 文書validator負例、37製品TESTと別 |
| 実証時期の分離 | 全要件 | 全画面 | 設計仕様の審査と実装後の実機・運用受入を分離。失敗から設計に戻る台帳 | 全37計画ID、not_runを保持 |

## ADR比較・反証・移行（変更前記録）

| ADR | 今回の仕様候補 / 3案 | 費用仮説・新リスク・旧案が優れる条件 | 移行・検証 |
|---|---|---|---|
| 010/015 | B非publicに触れたjobはCloud不可を初期規則。A精密lineage/分類引下げ（高）・Bjob taint（低中）・CCloudなし（低） | Bは公開部分の送信も止める。完全publicだけなら旧案は単純。由来不明を許すと破綻 | 不明由来はdeny、旧同意再利用なし。混在→要約→再添付を机上追跡、通信実証は後 |
| 012 | B入力不変resume/訂正はfork。A依存DAG再計算（中高）・B新job（低中）・C人手再利用（中） | job増と説明負担。完全不変の障害復旧は旧案が適する。forkで副作用ledgerを失えば破綻 | 不明な旧成果は再利用不可、副作用IDを引継ぎ再送禁止。状態表/ケース机上確認、kill試験は後 |
| 013 | A限定suiteのvalidation operation。A機械証拠と採用gate（中高）・B人の証拠確認（中）・C既存corpusのみ（低） | Aはsuite誤適合で過大なVerifiedが生じる。read-only比較だけならCが速い | assertion_typeと対象hash統一、未知suiteは昇格不可。旧証拠適合性不明は再審査。実動作は後 |
| 017 | B初期plain text。A安全Markdown subset（中）・B非実行text（低）・C隔離viewer（中高） | Bは見た目の表現力低下。旧実装が既にtextなら追加は小さい | 本文bytes不変、安全な表示/再export。悪意fixtureは計画、UI/通信実証は後 |
| 016 | A状態真理値表とdigest束縛+B不変Round記録。A構造化検査（中）・B履歴manifest（低中）・C手動照合のみ（低） | metadata更新負担、digestは真正性の証明ではない。単発ならCが簡単 | 最新証拠を改変せずactive metadataを新設。検査器の実負例で確認 |
| 018（新規） | 設計仕様D/実装後Rに分離。A実機を設計承認の前提（循環し得る）・B仕様後に実装/実証/再設計（今回指示）・C実証省略（不採用） | Bは実装後の手戻りが増える。read-only文書用途だけならAの限定PoCは有益 | 過去No-Goは履歴保持。今回は規則更新だけ、許可/合格を捏造しない。実証台帳とrelease gateを対応 |

重要方針の個別採用はProposedのまま。本利用者指示により検証時期の分離方針を設計に反映するが、実装開始/本番利用の許可にはしない。Markdown本文正本・Cloud default OFF・既存27要件を保持する。

## 確認すること・先送りすること

今回: 契約の一意性、API/DB/画面/状態/主試験の対応、机上ケース、証拠digest、検査器負例を確認。人間判断・インタビュー結果は未取得なら未取得と記録する。

実装後: 同時編集、kill/復旧、失効/公開競合、通信観測、renderer/a11y、実機model性能、backup復元、費用、知識効果。実施担当・開始条件・期待値・証拠・設計差戻し先は `docs/06-quality/POST_IMPLEMENTATION_VALIDATION.md` と `verification-register.json` へ登録。動作未確認を理由に同じ文書審査を繰り返さず、実装後に実施して設計を改良する。
