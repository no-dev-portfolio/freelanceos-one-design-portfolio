# 要求‐画面‐API/データ‐試験の対応 v0.10

全27要件を個別化。TESTは37計画ID、全て実機未実施。API/DBは設計候補。P1未定義は未実装と明示し隠さない。Knowledge/Agentの強制点は設計参照とCR-001影響表で追跡する。

| REQ | 設計 | SCREEN | API | DB/データ | TEST | 審査  初回slice |
|---|---|---|---|---|---|---|---|
| REQ-UX-001 | [02-ux/SCREEN_SPEC.md](../02-ux/SCREEN_SPEC.md) | SCR-00, SCR-01, SCR-02, SCR-04, SCR-06, SCR-10 | /jobs,/knowledge/search,/approvals | jobs,knowledge_refs,approval_requests | TEST-UX-001 | F-07/10 | S1 |
| REQ-UX-002 | [05-agent/AGENT_AND_TOOLS.md](../05-agent/AGENT_AND_TOOLS.md) | SCR-02, SCR-03, SCR-08 | /jobs/{job_id}/events,/operations/{id},/jobs/{job_id}/fork | job_attempts,job_steps,operations,execution_manifests,effect_ledger | TEST-UX-002, TEST-AI-008 | F-05/07 | S1 |
| REQ-UX-003 | [02-ux/CONTENT_PRESENTATION.md](../02-ux/CONTENT_PRESENTATION.md) | SCR-06, SCR-07 | /approvals/{id}/decision | actions,approval_requests | TEST-UX-003, TEST-UX-006, TEST-AI-007 | F-04/07 | S1 |
| REQ-UX-004 | [02-ux/SCREEN_SPEC.md](../02-ux/SCREEN_SPEC.md) | SCR-00, SCR-03, SCR-07, SCR-09 | /operations/{id},/settings | operations,jobs | TEST-UX-004, TEST-UX-006 | F-05/07 | S1 |
| REQ-UX-005 | [02-ux/CONTENT_PRESENTATION.md](../02-ux/CONTENT_PRESENTATION.md) | SCR-00, SCR-01, SCR-02, SCR-03, SCR-04, SCR-05, SCR-06, SCR-07, SCR-08, SCR-09, SCR-10 | /jobs/{job_id}/events | jobs | TEST-UX-005, TEST-UX-006 | F-07 | S1 |
| REQ-KB-001 | [03-architecture/SYSTEM_DESIGN.md](../03-architecture/SYSTEM_DESIGN.md) | SCR-00, SCR-04, SCR-05, SCR-09 | /vaults/{id}/status | vaults | TEST-KB-001, TEST-KB-010, TEST-SEC-001 | F-01/09 | S1 |
| REQ-KB-002 | [04-knowledge/KNOWLEDGE_MODEL.md](../04-knowledge/KNOWLEDGE_MODEL.md) | SCR-04, SCR-05, SCR-07 | /knowledge/{note_id},/knowledge/validations,/knowledge/validations/{id}/adopt | knowledge_refs,knowledge_validations,validation_suites | TEST-KB-002, TEST-KB-012 | F-06 | S1 |
| REQ-KB-003 | [04-knowledge/KNOWLEDGE_MODEL.md](../04-knowledge/KNOWLEDGE_MODEL.md) | SCR-04, SCR-05 | /knowledge/search | revocations,knowledge_refs | TEST-KB-003, TEST-KB-011, TEST-AI-009 | F-02/03/06 | S1 |
| REQ-KB-004 | [04-knowledge/KNOWLEDGE_MODEL.md](../04-knowledge/KNOWLEDGE_MODEL.md) | SCR-03, SCR-05, SCR-07 | /knowledge/candidates,/knowledge/validations,/knowledge/validations/{id}/adopt | memory_candidates,knowledge_validations,validation_suites | TEST-KB-004, TEST-KB-012 | F-06 | S1 |
| REQ-KB-005 | [03-architecture/SYSTEM_DESIGN.md](../03-architecture/SYSTEM_DESIGN.md) | SCR-05, SCR-07 | /actions,/operations/{id} | write_operations,actions | TEST-KB-005, TEST-KB-010, TEST-AI-007 | F-01/04 | S2 |
| REQ-KB-006 | [03-architecture/SYSTEM_DESIGN.md](../03-architecture/SYSTEM_DESIGN.md) | SCR-03, SCR-05, SCR-07, SCR-09 | /operations/{id}/reconcile | write_operations,job_attempts | TEST-KB-006, TEST-KB-010, TEST-AI-008 | F-01/05 | S2 |
| REQ-KB-007 | [03-architecture/SYSTEM_DESIGN.md](../03-architecture/SYSTEM_DESIGN.md) | SCR-03, SCR-04, SCR-05, SCR-09 | /knowledge/{note_id}/revoke | revocations,publication_records | TEST-KB-007, TEST-KB-011 | F-02 | S1 |
| REQ-KB-008 | [04-knowledge/KNOWLEDGE_MODEL.md](../04-knowledge/KNOWLEDGE_MODEL.md) | SCR-03, SCR-05, SCR-08 | /knowledge/{note_id} | dependencies,knowledge_sources | TEST-KB-008, TEST-KB-011 | F-02/06 | S1 |
| REQ-KB-009 | [04-knowledge/KNOWLEDGE_MODEL.md](../04-knowledge/KNOWLEDGE_MODEL.md) | SCR-05, SCR-07 | /knowledge/candidates | knowledge_edges,memory_candidates | TEST-KB-009, TEST-KB-012 | F-06 | deferred |
| REQ-AI-001 | [05-agent/AGENT_AND_TOOLS.md](../05-agent/AGENT_AND_TOOLS.md) | SCR-03, SCR-08, SCR-09 | /actions | actions,settings_policies | TEST-AI-001, TEST-SEC-001 | F-03/09 | S1 |
| REQ-AI-002 | [03-architecture/EXECUTION_CONTRACTS.md](../03-architecture/EXECUTION_CONTRACTS.md) | SCR-00, SCR-03, SCR-07, SCR-09 | /consents,/settings | consents,settings_policies,derived_artifacts,egress_envelopes | TEST-AI-002, TEST-AI-009 | F-03 | S1 |
| REQ-AI-003 | [05-agent/AGENT_AND_TOOLS.md](../05-agent/AGENT_AND_TOOLS.md) | SCR-02, SCR-03, SCR-08, SCR-09 | /jobs/{job_id}/cancel,/jobs/{job_id}/resume,/jobs/{job_id}/fork | job_attempts,budget_reservations,execution_manifests,effect_ledger | TEST-AI-003, TEST-AI-008, TEST-OPS-004 | F-05/09 | S1 |
| REQ-AI-004 | [03-architecture/EXECUTION_CONTRACTS.md](../03-architecture/EXECUTION_CONTRACTS.md) | SCR-03, SCR-06, SCR-07 | /approvals/{id}/decision | actions,approval_requests,derived_artifacts,egress_envelopes | TEST-AI-004, TEST-AI-007 | F-04 | S1 |
| REQ-AI-005 | [05-agent/AGENT_AND_TOOLS.md](../05-agent/AGENT_AND_TOOLS.md) | SCR-02, SCR-03, SCR-08 | /operations/{id}/reconcile,/jobs/{job_id}/fork | operations,tool_executions,execution_manifests,effect_ledger | TEST-AI-005, TEST-AI-008 | F-05 | S1 |
| REQ-AI-006 | [06-quality/THREAT_MODEL.md](../06-quality/THREAT_MODEL.md) | SCR-03, SCR-08, SCR-09 | P1 connector契約未承認 | settings_policies,tool_executions | TEST-AI-006 | F-09 | deferred |
| REQ-EVAL-001 | [04-knowledge/GROWTH_EVALUATION.md](../04-knowledge/GROWTH_EVALUATION.md) | SCR-10 | /evaluation-runs | evaluation_runs | TEST-EVAL-001, TEST-EVAL-004 | F-08 | S2 |
| REQ-EVAL-002 | [04-knowledge/GROWTH_EVALUATION.md](../04-knowledge/GROWTH_EVALUATION.md) | SCR-05, SCR-10 | /evaluation-runs | evaluation_runs,knowledge_validations | TEST-EVAL-002, TEST-EVAL-004 | F-06/08 | S2 |
| REQ-EVAL-003 | [04-knowledge/GROWTH_EVALUATION.md](../04-knowledge/GROWTH_EVALUATION.md) | SCR-08, SCR-10 | /evaluation-runs/{id} | evaluation_runs | TEST-EVAL-003, TEST-EVAL-004 | F-08 | S2 |
| REQ-OPS-001 | [03-architecture/SYSTEM_DESIGN.md](../03-architecture/SYSTEM_DESIGN.md) | SCR-09 | /backups,/restores | backup_manifests,revocations | TEST-OPS-001, TEST-KB-011, TEST-OPS-004 | F-02/09 | S2 |
| REQ-OPS-002 | [02-ux/CONTENT_PRESENTATION.md](../02-ux/CONTENT_PRESENTATION.md) | SCR-03, SCR-08, SCR-09 | /exports | audit_events,evidence | TEST-OPS-002, TEST-SEC-001, TEST-OPS-004 | F-04/05/09 | S1 |
| REQ-OPS-003 | [05-agent/AGENT_AND_TOOLS.md](../05-agent/AGENT_AND_TOOLS.md) | SCR-03, SCR-09, SCR-10 | /settings | budget_reservations | TEST-OPS-003, TEST-OPS-004 | F-09 | deferred |
| REQ-BIZ-001 | [01-product/PRD.md](../01-product/PRD.md) | SCR-03 | P1専用契約未承認 | P1必須条件schema未決 | TEST-BIZ-001 | F-10 | deferred |

全指摘の処置・採否・実証待ちは [改修対応表](../../reviews/codex/REMEDIATION.md)、変更前影響は [改修計画](DESIGN_REMEDIATION.md) を参照。

CR-002の実装前後の分離と子ケースは [実装後確認計画](../06-quality/POST_IMPLEMENTATION_VALIDATION.md)。全37計画はverification-registerへnot_runで登録。主試験の要件ごとの一致、API/entity/画面参照は文書validatorで検査する。
| REQ-SEC-001 | [03-architecture/API_CONTRACT.md](../03-architecture/API_CONTRACT.md) | SCR-00, SCR-09 | /auth/pairing,/auth/session,/auth/csrf,/auth/session/refresh,/auth/sessions,/auth/sessions/{id} | users,sessions,pairing_challenges | TEST-SEC-001 | CR-03/ISSUE-015 | S1 |

## sliceの意味（CR-003）

S1=最初の安全基盤/読取・候補審査、S2=安全書込・復旧・独立再利用・評価・通常運用、deferred=P1の後段。S1列は要件全体合格を意味しない。S1のAI-003/005はローカル候補作用でも上限/不明作用停止とledgerが必要。CloudはS1/S2ともOFF、未提供操作は拒否。KB-004はS1で隔離runner証拠の採用まで、Vaultへの適用はS2。OPS-001未完のS1は架空データの使い捨てVault限定、既存の実Vaultを変更/通常運用しない。EVAL未完S1は知識成長の価値合格を主張しない。

S1→S2でP0要件を削除せず、S2着手前にwriter/復旧の判断と対象scope許可を追加する。各sliceでも全不変条件は適用し、無効機能をUI/API両方で閉じる。37試験は統合受入の正本で、部分sliceの合格を全37合格へ転記しない。
