# CR-003 検証結果（2026-10-28）

実行対象は本ZIPのlatest。文書/検査コードの検証で、製品の37試験ではありません。

## python3 scripts/check_design.py

Exit: 0

```text
PASS: design structure {'requirements': 28, 'test_plans': 37, 'screens': 11}
LIMIT: no runtime, UX, safety, reviewer identity or human acceptance verified
```

## python3 scripts/check_review_gate.py

Exit: 0

```text
WARN: REVIEW_SOURCE_DRIFT: historical reviewed commit edcebcc650ec123913ac0407daa32aa2055349a5; 32 reviewed files differ/missing; 12 new source files. Current source is not covered by this review; fresh review required before approval.
PASS: review metadata and artifact binding {'phase': 'codex_review_recorded', 'human_acceptance': 'pending', 'design_approval': 'pending'}
LIMIT: no identity, independence, approval authenticity or runtime safety verified
```

## python3 scripts/test_design_checks.py

Exit: 0

```text
...................................................
----------------------------------------------------------------------
Ran 51 tests in 4.980s

OK
```

M7、許可flagの片側変更/全側偽装、受入accepted+not_run、証拠風の体裁だけの全件passed、GETを消してPOSTだけ残す、認証要件/画面対応の欠落、P0後回し、審査source差分の警告を回帰確認。全51ケースOK。新たな正式CLI審査/承認真正性の検証ではありません。
