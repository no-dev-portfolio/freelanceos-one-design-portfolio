# GitHub設計審査・改修手順 v0.10

Private repository: NaokiOosawa/freelanceos-one-design。一次審査PR #2（review/codex-round-1）は実施記録。CR-001改修はreview/design-remediation-round-1から積み重ねPRとして保存し、一次審査とは別に差分確認する。mainへのmerge/設計承認は未実施。

1. 対象commit固定、AGENTS→共通協定→START_HERE→全設計を読む。
2. 一次審査の実行・保存を確認し、元REVIEWは不変にする。改修元・対象審査・変更ファイルを記録する。
3. DESIGN_REMEDIATIONに変更前影響とADR比較、ISSUESに実証待ち、仕様/追跡/TESTを同時に更新する。
4. 両検査とvalidator負例試験を実行。構造検査で実機/UX/独立性が証明されたとは書かない。
5. 改修PRで人間の重要ADR採否、Critical/High処置、許可されたPoCの証拠を確認する。状態はcodex_review_recordedのまま自動昇格しない。
6. 一次審査受理と前提充足後、人間の指示がある場合だけClaudeを新sessionで開始する。baselineを先に盲検審査し、その後Codexと比較。制約があれば独立性の限界を記す。本作業で起動しない。
7. 設計承認G5とアプリ実装許可は別々に記録する。Draft PRや検査greenは許可ではない。

main保護とowner approvalは推奨設定であって設定済みとは主張しない。認証情報をcommitしない。
