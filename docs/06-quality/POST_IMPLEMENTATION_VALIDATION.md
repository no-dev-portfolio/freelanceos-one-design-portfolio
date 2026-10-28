# 実装後の確認と設計改良 v0.11

2026-10-25の利用者指示により、実装が必要な実証は実装後に行い、結果を設計へ戻す。今回のアプリ実装開始許可ではない。実機合格や安全性受入を宣言しない。

## 3種類の確認

| 種別 | 今回できること | 未実施事項の扱い |
|---|---|---|
| D 文書/静的 | 不変条件、状態/権限表、API/DB/画面/試験対応、机上ケース、文書validator、配色tokenの計算 | 記述した規則が一貫するか確認。実装挙動を実証したとはしない |
| H 人間/利用者 | interview計画、紙/文書storyboardの導線確認、優先方針/許容値の採否 | 実装なしでも可能だが参加者/人間採否が未取得ならpending。実装依存と偽って先送りしない |
| R 実装後 | 実通信/renderer/transaction/FS/Obsidian/worker/model/性能/効果/a11y/復元 | verification-register.jsonの37試験をnot_runで登録、担当/前提/期待値/証拠/差戻し先を保持 |

## 設計仕様と実運用のゲート

- G5-D 設計仕様審査：Dの記述不足/矛盾を修正、未処置の仕様上Criticalを無くす。Rでしか確認できないリスクは、停止条件・対象環境・期待値・担当・実証予定を特定して未実証として残す。R未実施だけを理由に文書改修や仕様審査を無限に反復しない。重要方針の人間採否と必要な独立審査は別に記録する。
- I 実装着手：利用者が対象commit/scopeを明示して許可する別の判断。G5-DやPR保存は許可ではない。今回はI未許可、実装しない。
- G5-R 機能有効化/運用受入：I後に実装し、各capabilityに紐付くR試験を完了する。未検証capabilityは無効/隔離、結果不明はBlocked。Highを残すなら人間の明示リスク受容と隔離、Criticalの実証失敗は対象capability No-Go。試験なしで通常運用へ出さない。

過去のREVIEWのNo-Goはその対象commitと当時の基準の歴史記録として不変。CR-002で確認時期を分離しても、過去リスクをClosed/実証済みにしない。現時点は「設計改修案反映、仕様再審査/人間判断待ち、R試験not_run、実運用未承認」。

## 実装後の有効化条件

| capability | 初期状態 | 必須の代表試験 | 失敗時の停止と差戻し |
|---|---|---|---|
| Vault read/search | 未実装 | KB-001/002/003/007/008/012、SEC-001 | 読取/検索を停止、SYSTEM_DESIGN/KNOWLEDGE_MODELへ |
| Vault write | 未実装、未知writerは適用不可 | KB-005/006/010/011、AI-004/007/008、OPS-001 | write無効、候補保持、ADR-008と更新protocolへ |
| Cloud egress | OFF | AI-002/009、SEC-001、OPS-003/004 | 全Cloud停止、分類/最終payload/同意設計へ |
| workflow resume/fork | 未実装 | UX-002/004/006、AI-003/005/008、KB-011 | 自動resume停止、不明作用の再送なし、ADR-012へ |
| Verified memory | 未実装 | KB-004/012、EVAL-002 | 昇格/根拠使用停止、validation契約とADR-013へ |
| 表示/export | 未実装 | SEC-001、AI-009、UX-005/006、OPS-002 | 該当表示/export無効、plain text/CSP/ADR-017へ |
| 知識効果の主張 | 未測定 | EVAL-001〜004 | 成長効果を表示しない、対象仕事/評価設計へ |
| 通常運用/復元 | 未承認 | OPS-001〜004、SEC-001、保持/鍵/RPO/RTOの採否 | 隔離維持、復元公開不可、運用設計へ |
| P1 SQL/案件機能 | 未実装 | AI-006、BIZ-001と専用仕様 | 対象connector/機能無効、P1設計へ |

一覧は必要試験の代表集合。全受入IDの正本はregister。個々の試験合格だけで無関係capabilityを有効にしない。

## 必ず実施する改良ループ

1. 実装commit/環境/fixture hash/担当/期待値を凍結し、R試験を実行する。planned/not_runをpassedへ書換えるだけは禁止。
2. 結果、失敗/限界、実出力、秘匿済み証拠URI/hash、検証者、時刻をregisterへ記録。失敗はfailed、不確定はinconclusive。
3. Critical失敗は対象capabilityを停止。Issueに再現条件と設計仮説との差を記録し、対応ADR/API/DB/画面/Knowledge/TESTを修正する。期待値を実結果へ合わせて成功扱いしない。
4. 修正仕様の差分・移行/巻戻し・新リスクを審査し、新しい実装commitで再試験する。旧失敗結果を消さずattemptを追加する。
5. 必須ケース合格と人間の受入が揃ったcapabilityだけ有効化。知識効果は正答/根拠/人間工数/費用を実測してから表現する。

担当role：設計差戻しはdesign_owner、実装試験はimplementation_verifier、利用者試用はux_reviewer、security受入はsecurity_reviewer、最終有効化はhuman_owner。同じ人が兼ねる場合も役割・実施者を記録する。実施者名・日時・証拠は現在未取得でnull。自動scheduleや実装後の自動通知は今回設定しない。

## CR-003: S/HとRの境界・状態照合

アプリ非依存のFS競合/kill調査とlocalモデル能力はS（FEASIBILITY_SPIKES）でI前に見込みを調べる。統合後の実Vault/worker/model/通信の受入は引き続きR。S未了を「R待ち」とだけ表記しない。Hの参加者・採否もI前の判断材料にする。

両検査器は共通check_release_stateでreview-state、register、DESIGN_STATUSの実装許可をbooleanかつ一致と検査。現DESIGN ONLYでは全false固定。register/DESIGN_STATUSのruntime_acceptanceも一致し、acceptedは全計画passedと証拠記録が必要、さらに本段階では拒否。将来の実装許可は証拠と対象scopeを持つ別schemaの審査が必要で、flag操作で移行できない。照合は記録の整合であり、実行者/承認者の真正性や挙動は保証しない。
