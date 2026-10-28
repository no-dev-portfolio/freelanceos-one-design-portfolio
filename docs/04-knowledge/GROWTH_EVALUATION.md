# DOC-07 知識成長ループの設計

## 成長の定義
モデル重みの自己更新はしない。検証済みの知識とPlaybookを再利用することで、**未知の類似タスクに対する成果の品質が測定可能に改善すること**を成長と定義する。

## ループ
Work event -> Experience extraction -> Candidate scoring -> Source validation -> Contradiction check -> Human review -> Versioned memory -> Retrieval -> Independent task evaluation -> Feedback.

### ナレッジ候補採用基準
新規性、再利用性、出典品質、機密リスク、既存知識との整合、修正コスト。低品質な候補は生成量を増やさず保留/破棄する。

### A/B評価方法
同一モデル、同一質問、同一温度/パラメータ、固定ツールを用いて `No-memory` / `FTS` / `Validated-hybrid` を比較。評価セットは作成時系列でtrain/dev/holdoutに分離。holdoutの答えを記憶へ投入しない。複数反復の分散も記録。

### KPI
Task success rate、根拠の正確率、無効知識誤使用数、記憶が逆効果になった数、手作業確認時間、コスト/タスク、応答時間。スコアの分母と対象難易度、サンプル数、信頼区間を必須表示。

### 失敗時
記憶あり条件で劣化が生じた場合は対象知識/検索版を隔離し、再発ケースを評価データに追加する。AIが自身の判断だけで過去の正しい記憶を大量削除しない。

## v0.10 実験契約（未実測）

run manifestをholdout実行前に凍結：dataset/問題系列split/hash、corpus snapshot/hash、index生成設定/版、modelの固定識別子、prompt/tool/parameter版、seed（非対応なら非対応を記録）、条件順序、予算、採点rubric、採点者、主要指標、許容劣化、最小効果幅、停止基準、実行環境を保持する。値が未確定なら探索実験であって価値合格としない。

No-memory/FTS/Validated-hybridは同一問題のpaired比較。方式差は同じ検証済みcorpusを使い、知識の検証品質差は別実験に分ける。各条件でjob/cache/過去回答/会話を初期化し、実行順を無作為化する。問題系列単位でtrain/dev/holdoutを分け、言い換え・同じ元資料の派生問題が跨がないようhash/由来を審査。holdout正解は通常agentと採点対象memoryから隔離する。

正答・根拠整合・scope適合は固定rubricと盲検人手評価で確認し、LLM自己採点だけで合格にしない。全割当問題を分母にしtimeout/拒否/失敗/棄権を別集計する。CIの単位は独立問題系列、同問題の反復を独立例として水増ししない。人間確認時間は計画確認・差分承認・訂正・失敗復旧を含む開始/終了点を事前定義する。

20〜100架空例は探索用仮案。holdoutを見てから閾値を変更しない。再測定は新run/新holdoutへ。劣化は対象知識/索引版を隔離し、原因例はdevへ移してから新holdoutを用意する。改善不明なら機能追加で埋めず、対象仕事とコスト/確認時間をG0へ戻す。TEST-EVAL-004で系列漏洩と条件間汚染を破壊試験する。

## v0.11 評価時期と設計差戻し

実装前はmanifest項目、split/採点/分母/CI/計時の定義、漏洩しないデータ管理を仕様として確認する。効果・悪化・費用・確認時間の実測は実装後にEVAL-001〜004で行う。結果が悪ければ対象job/知識/検索条件をIssue化してPRD/Knowledge/評価設計を改良し、新runと新holdoutで再試験する。閾値を後付けで下げて成功扱いしない。担当/証拠/差戻し先はverification-registerで保持する。

## v0.12 効果幅と独立系列数の固定（CR-007）

20〜100例は探索であり、区間の重なりだけでpaired効果の有無を判定しない。確証比較は独立問題系列ごとに1つの事前定義したbinary成功を採点し、主要比較はNo-memory対Validated-hybridの1比較。他比較は探索又は多重性を事前調整する。

未承認の計画例: 最小差delta=0.15、条件間の不一致確率q=0.40、両側alpha=0.05、検出力0.80。独立paired差の正規近似で n ≈ (z(1-alpha/2)*sqrt(q)+z(power)*sqrt(q-delta²))²/delta² ≈138系列（切上げ、安全側の概算）となる。これは既知母数での近似で、qの見積り・小標本・層化/クラスタに依存する。採用値でも実測結果でもない。

手順: dev pilotの独立系列でqと基礎成功率を見積り、delta/alpha/power/層別/主要比較/人間確認時間の許容劣化を人間が採用する。exact paired検定のpower又は事前seed固定simulationで必要nを再計算し、脱落見込みを加えてfreeze。計算方法/コード版/出力hash/採用者/日時をrun manifestへ格納。未確定ならholdout未開始。必要nを用意できない場合は探索/不確定と報告し「改善なし」や価値合格にしない。

CIは系列単位のpaired差を対象にし、反復や言い換えをnへ足さない。欠測/timeoutも割当分母に残し成功率0として主要解析、理由別内訳を併記。holdout閲覧後のn/閾値変更は新manifest/新holdout。S-LOCALの40系列は実用性spikeであり、この効果検証nを満たしたとはしない。
