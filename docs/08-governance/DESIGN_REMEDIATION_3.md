# CR-003 反証レビューへの改修計画（2026-10-28）

対象はGitHub PR #5の515fbc5921e5170f060a2dc157f278d7f8e1bfecからのローカル修正版。添付報告書は所見の出典であり、承認・実験実行の指示とは扱わない。今回の依頼に基づき文書検査コードと対応仕様を修正する。製品アプリの新規実装、モデル実験、聞き取り、GitHub書込は今回の対象外。

## 変更前の影響

| 所見 | 要件/画面 | API/データ | 試験/強制点 |
|---|---|---|---|
| CR-01/02 | AI-002、KB-005/006、EVAL-001〜003、SCR-00/07/10 | model profile、writer mode、事前調査記録 | AI-002、KB-010、AI-008、S/H調査とIの分離 |
| CR-03 | 新規REQ-SEC-001、UX-001/002、KB-004、SCR-00/02/05/07/09 | 認証7route、jobs/candidates/settings/consentsのGET、pairing_challenges/sessions | SEC-001子ケース、HTTP method付き画面API台帳 |
| CR-04 | 全R計画、運用表示 | register/state/DESIGN_STATUSの許可・受入 | 共通validator、M7と受入偽装の負例 |
| CR-05 | 審査状態の表示 | reviewed commitとローカルファイルhash | 警告、歴史的CLI証拠は不変 |
| CR-06 | 全28要件・全11画面 | 初回sliceの含有/後回しと条件 | TRACEABILITY第8列と全件検査 |
| CR-07/08 | EVAL-001/003、SCR-10 | 事前登録manifest、保持契約 | 標本数の前提/固定手続、曖昧文の訂正 |

## 比較・費用・反証・移行

A: 文書注記のみ（低費用、M7再発と即興APIのリスク）。B: 共通照合器とmethod付き画面台帳、事前調査・slice追跡を追加（採用候補、保守費用中、台帳自体の漏れと閾値の誤採用が新リスク）。C: アプリ全体を実装し実機検証（高費用、調査前の手戻り、今回の範囲外）。Bを今回の文書・検査修正に使用し、重要な数値/方式の採用はpendingにする。

旧案が優れる条件は、read-only検索だけで価値があると利用者が明示採用し、書込/成長効果を提供範囲から除く場合。その場合もP0を黙って削除せず別ADRで製品仮説を変更する。単調taintを弱めてCloud可用性を得る案は今回採用しない。

移行は原本ZIPとsnapshotsを保持しlatestだけ改修。旧レビュー本文/digest/sessionを新commitへ付替えない。取消は修正前のZIPへ戻せるが、M7の穴も戻る。原本manifestと修正版manifestを分ける。
