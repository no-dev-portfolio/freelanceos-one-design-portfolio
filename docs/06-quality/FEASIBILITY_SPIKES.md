# 実装前の成立性調査 S と人間確認 H（CR-003）

状態: plan_only / 実験0件 / 人間採否pending。製品I許可と別の限定spike許可を取り、S/Hの結果をI前に確認する提案。調査スクリプト自体が製品の実装や受入を代替することはない。実Vault/顧客資料/Cloudを使わず、使い捨てfixtureに限定。未決の閾値を実験後に埋めない。

## S-WRITER: 書込競合と復旧（ISSUE-001、ADR-008）

アプリ非依存でAPFSの一時ディレクトリに架空ノートを作り、①hash取得直後の別writer保存、②rename前後の別writer保存、③書込直後/記録前kill、④再実行・重複、⑤symlink差替えを調べる。非協調writerでは本来CASを保証できないため、黙った適用成功を目標にせず適用拒否/提案fileだけを期待する。協調方式候補は全writerが同じgateに従う条件を明示し、各注入点100反復を受入候補とする。無言消失0、重複適用0、不明はBlocked、双方本文/journal保持。未達/非協調はwriter有効化不可。

保存証拠: fixture/script/hash、OS/FS/Obsidian/sync版、注入点、seed、両本文hash、実出力、再現手順、失敗も含む全反復。Obsidian/syncを使わないFSだけの調査で対応認定しない。Sは方式の見込みを比較するもの、製品統合のTEST-KB-010/AI-008はI後に別実施。

## S-LOCAL: 機密仕事をlocalだけで処理（ISSUE-005/011、REQ-AI-002）

P-01の主要仕事は非public由来となる前提で、Cloudを可用性の救済にしない。job taintは単調、要約/匿名化でpublic化しない。localが不成立ならP0未達として対象仕事/モデル/機能を見直す。

実験前の採用候補値（未承認）: 独立40系列の架空SQL件数不一致、NULL/JOIN/重複/集計各10系列。正解と採点rubricを担当人間が先に固定し、通常agentと分離。期待結果・根拠・適用制約を満たす系列32/40以上、timeout/拒否も分母。誤った更新SQLを実行0、許可外通信0。対象Macのcold startを別報告し、warm end-to-end p95 120秒以下、1系列最大180秒、peakメモリは人間が対象Macに応じて固定（未設定なら実験開始不可）。これらは実測値でも統計的な価値立証でもない。

固定項目: hardware/メモリ/OS、model完全ID・hash・量子化・runtime版、prompt/tool、fixture/正解hash、温度/seed、出力採点、時間の起終点/timeout、最大メモリ、上記閾値への採否、採用者/日時。いずれも未記入。model導入/downloadや他者送信は今回実行しない。S合格後もTEST-AI-002.localを実装環境で再試験し、統合経路の漏洩・性能を確認する。

## H-VALUE: 5名の形成的聞き取り（ISSUE-010）

VALUE_VALIDATIONの質問で実装なしに頻度、手作業時間、候補だけの価値、書込/再利用が必須か、local待時間/確認負担を調べる。5名は募集計画で参加者0名、代替手段が優れる所見も保存する。統計的な90%成功の立証には使わない。参加者確保・連絡・聞き取りは今回行っていない。

## Iへ渡す条件と停止

S/H実施者はdesign_owner/human_owner/security_reviewer。対象scope、スクリプト/環境、合否閾値を人間が実験前に採用して凍結する。writer/localが不成立又は結果不明なら拡大実装を止めADRへ戻す。read-only S1だけを先行する例外は、その範囲・残リスク・価値未実証を人間が記録してIを別判断する。S/H未了を黙ってG5-DやI合格にしない。S/Hと製品Rの結果欄・証拠を分離する。
