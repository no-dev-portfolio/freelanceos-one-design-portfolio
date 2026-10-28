# DOC-06 Obsidian Knowledge Model

## ナレッジとは
検証可能で適用条件が明示された再利用単位。会話履歴すべてではない。人による承認と、技術的検証は別概念。

### Vault構造の初期案
```text
FreelanceOS-Knowledge/
  00_Home/
  01_Inbox/Candidates/
  02_Profile/
  03_Technical/{SQL-Server,Oracle,VBA,AI,AWS}/
  04_Projects/
  05_Business/
  06_Experience/{Success,Failure,Lessons}/
  07_Playbooks/
  08_Research/
  09_Evaluations/
  90_Archive/
  99_Templates/
```
フォルダは見やすさを補助するだけで、ノートのID・権限・分類はパスの名前に依存しない。

### Frontmatterスキーマ例
```yaml
---
note_id: "00000000-0000-4000-8000-000000000001" # 架空UUID
assertion_type: "technical_fact" # technical_fact/procedure/preference
status: "candidate" # captured/candidate/reviewed/verified/superseded/quarantined
revision: 1
validation_id: null # DBの検証証拠参照。Frontmatterだけでは昇格しない
sensitivity: "confidential" # public/personal/confidential/restricted
scope:
  product: "SQL Server"
  version: "2022"
source_ids: ["SRC-DEMO-01"]
last_verified: null
supersedes: []
---
```
`source_ids` の元資料、証拠のハッシュ、承認記録はDB/Evidence Storeで参照。Frontmatterに機密本文やアクセストークンを入れない。

### ノート本文テンプレート
問題／結論／適用範囲／根拠／再現・テスト方法／例外／失敗事例／関連ノート／更新履歴。

### 知識状態機械
`Captured -> Candidate -> Reviewed -> Verified -> (Superseded | Quarantined)`。`Reviewed`は「人が内容を確認」、`Verified`は「適切な検証が証拠とともに完了」。assertion_type別の検証と状態遷移は末尾のv0.10節に定義する。本人の好みの確認を技術実証と呼ばない。

### 検索
1) caller ACL/sensitivity/失効を候補取得前に強制; 2) scope抽出; 3) 同一世代FTS/ベクトル検索; 4) リンク候補も同じ認可; 5) 本文/索引/検証hash照合; 6) 通常の回答根拠は有効verifiedだけ; 7) 引用位置と本文hashを検証; 8) jobへ依存note/hash/epochを保存; 9) 公開gateで再認可。candidateは候補審査画面の専用経路にのみ表示し、通常検索や回答へ混入させない。

### 更新
出典・重複・矛盾・機密チェック→元/提案本文snapshot保存→不変action生成→承認→writer能力とpolicy再認可→協調排他内で比較・適用→journal照合→索引更新。SYSTEM_DESIGNの安全条件を満たさなければBlocked。hash確認+renameだけではCASは成立しない。競合時は元/現在/提案の3-way diffを作り、mergeは新候補・新hash・新承認とする。

### 記憶汚染対策
ノート本文は非信頼データ。Markdownに指示らしき文章があってもプロンプトの上位権限にはしない。外部資料は隔離し、信頼済みルールの更新には使わない。候補の出典・事実性を確認する。

### 再評価/失効
対象技術のバージョン更新、テスト失敗、根拠削除、手作業での編集変更、期限超過で再検証対象とする。superseded/quarantinedは回答の根拠に使用しない。

### 同期のエッジケース
rename/move、同名ノート、添付移動、Obsidian Sync/iCloud競合、別端末編集、改行/エンコーディング差異、フロントマター破損、symlink、ディレクトリトラバーサル、index遅延、クラッシュをPoCで必須検証。

## v0.10 属性・分類・成長の確定条件

**改訂:** 2026-10-25 / CR-001 / 設計候補。重要ADRはProposed、実機未検証。審査基準・影響・比較案は [改修計画](../08-governance/DESIGN_REMEDIATION.md)。

`knowledge_id`は旧案の別名であり、標準識別子は`note_id`。既存ノートがある場合はdry-runで旧ID→UUIDのmappingを人間へ提示し、重複・欠落は隔離する。本文正本は変えない。case、改行、encodingを含むhashは保存bytesを対象にし、canonical化で人の本文差分を隠さない。

状態の保存値はlowercaseのcaptured/candidate/reviewed/verified/superseded/quarantined。captured→candidateは出典/分類検査、candidate→reviewedは人間確認、reviewed→verifiedは検証証拠とhash一致。確認だけでverifiedにはしない。verified本文変更は検証失効・candidateへ戻し、旧検証を履歴保持する。失効/矛盾/不明IDはquarantined、置換先が検証された場合にsuperseded。再有効化は新検証と人間処置を要求し、tombstoneを消さない。

assertion_type=technical_factは対象製品/版/再現試験、procedureは手順完遂証拠、preferenceは本人確認を証拠とし「技術実証」と表示しない。通常の技術回答はtechnical_fact/procedureのscopeと検証証拠を照合する。未知typeは隔離。失効したsourceを使う依存ノートも公開停止して再検証。

分類はpublic/personal/confidential/restrictedに統一。旧internal、未分類、混在で判定不能はdeny。未承認のFrontmatter変更で公開範囲を広げない。本文中の指示・出典中の指示は非信頼データで、許可toolでも引数/対象/送信条件を別gateで検査する。

削除・隔離・権限縮小はrevocation_epochを更新し、公開buffer・成果物・引用も再認可。外部変更検知gapと既送信回収の限界はSYSTEM_DESIGNを参照。TEST-KB-010/011/012とEVAL-002/004が未合格のため、安全な自動成長を実証済みとは扱わない。

## v0.11 候補からの検証・再利用

検証の主張/適用範囲とsuiteの適合はEXECUTION_CONTRACTSのregistryで定義。SCR-03/05からvalidation operationを依頼し、runner証拠と対象hashをSCR-08で確認、ownerがSCR-07で採用して初めて技術Verifiedへ進める設計。Passedだけ、承認だけ、旧hash・無関係suiteでは昇格不可。本文/証拠/source変化はEvidenceStale/検証無効、新validationで再審査する。

標準fieldはassertion_type、値はtechnical_fact/procedure/preference。旧type=technical-factは明示mappingとdry-runの対象で、未知値をそのまま採用しない。preferenceは本人確認human_attestedとして別表示し、技術実証と混同しない。

知識を利用した要約・prompt・出力・再添付にも分類/由来/taintを継承。publicへの自動分類引下げなし。本文は非信頼plain textとして表示し、埋込resourceを取得しない。技術成長や同期の成立は実装後の検証事項で、机上整合の確認と別管理する。
