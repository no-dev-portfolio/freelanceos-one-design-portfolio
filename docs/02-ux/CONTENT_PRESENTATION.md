# 非信頼コンテンツの表示・export契約 v0.11

R2-04/ADR-017の初期設計候補。アプリ実装なし。Markdown本文を正本として保存し、表示だけを非実行のplain textへ制限する。

## 初期ルール

本文、LLM回答、検索snippet、差分、引用、metadata、エラー、監査摘要、ファイル名は全て非信頼text。DOMへtextとして挿入する契約とし、HTMLとして解釈/挿入しない。raw HTML、SVG、iframe、event属性、style、script、Markdown埋込画像は実行/描画しない。rich Markdown/HTML viewerは初期対象外。scriptや外向きresourceは文字列で見えるだけ。markdown parserやlinkifyによる自動URL変換も行わない。

外部画像、link preview、favicon、埋込動画、remote font等を本文から自動取得しない。CSPの候補はdefault-src 'none'を基準に、ビルド済みlocal assets、必要な同一origin API、nonce/hash付きアプリscript/styleだけを限定許可する。object/frame/base-uriはnone。unsafe-inline/unsafe-eval、任意remote originは禁止。これは実装設定を証明した記述ではなくTEST-SEC-001の確認対象。

リンク文字列はクリックで実行しない。明示「リンク先を確認」操作で正規化済みhttps URLをpreviewし、egress/同意を再検査する。javascript/data/file/任意custom schemeは拒否。Obsidianは専用buttonだけ、note_idをサーバーで許可Vault内の現pathへ解決し、制御文字/引数混入を拒否し、同じnoteを開く明示確認後にlocal操作する。本文内のobsidian URIを直接実行しない。

P0 exportはUTF-8 .txtか構造化JSONに限定。Content-Typeはtext/plain又はapplication/json、Content-Dispositionはattachment、X-Content-Type-Optionsはnosniffを要求。保存名はアプリ生成の固定形式でpath/制御文字を受け付けない。HTML/SVG/実行可能formatとrich exportは別ADR/試験まで未提供。exportしても分類/由来は失わず、再取込はEXECUTION_CONTRACTSの規則に従う。

## UX/a11yと表示量

コード/差分は空白・改行・行番号を保持し、元/現在/提案を見出しで区別する。長文は折返し/横scrollを選択可能、keyboardで全情報へ到達できる設計。bidi/不可視制御文字は表示層で可視化できるようにし、元bytesを黙って変えない。コピー時は原文/可視化表示のどちらかを明示する。

差分を全部scrollしただけで理解を確認したとしない。SCR-07は作用先/変更範囲/証拠/不可逆性にアクセスできない場合に承認を止める。読み上げへ秘密を自動流出させず、利用者操作で内容を読む。表示量/出力token/処理時間の上限はjobの予算・model profileに持たせ、上限不明では無制限生成しない。巨大本文は全文hashと省略状態を示し、未表示差分を承認済みにしない。

## 机上確認と実装後受入

| ケース | 仕様上の帰結 | 実装後の証拠 |
|---|---|---|
| 本文/LLM出力のscript・event属性 | textとして表示、実行不可を要求 | SEC-001.a：実行0件 |
| 外部画像/SVG/iframe/preview | textだけ、自動通信不可を要求 | AI-009.g：未許可通信0件 |
| 危険schemeを本文・差分・errorへ埋込 | 自動linkなし、専用操作でも拒否 | SEC-001.b：遷移/操作0件 |
| HTML風のexport・path名 | text/JSON attachment、固定保存名 | OPS-002.a：実行/漏洩0件 |
| 長文差分・320px/拡大・読み上げ | 隠れた差分の承認停止、focus/文脈を維持 | UX-005/006：実操作/a11y記録 |

机上規則は確認できるが、browser/renderer/CSP/exportの実効性は実装後に確認する。失敗時はADR-017、API表現契約、画面仕様を改良し、再試験までは対象表示/exportを有効にしない。
