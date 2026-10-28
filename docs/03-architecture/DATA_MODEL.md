# DOC-05 論理データ設計 v0.10（migrationなし）

**改訂:** 2026-10-25 / CR-001 / 設計候補。重要ADRはProposed、実機未検証。審査基準・影響・比較案は [改修計画](../08-governance/DESIGN_REMEDIATION.md)。

UUIDは不変、UTC保存、表示Asia/Tokyo。本文の更新正本はMarkdown。snapshotは証拠/復旧用で通常検索の別正本ではない。

| Entity | key / 主な要素 | 制約 |
|---|---|---|
| users / sessions | user_id / session_id,actor_id,expires_at,revoked_at | local単一利用者でも認証、secret hash保管 |
| vaults | vault_id,root_identity,writer_mode,sync_state,last_seen,index_generation | canonical rootと開いたobjectの一致、unknown writerは適用不可 |
| knowledge_refs | note_id,vault_id,relative_path,content_hash,revision,sensitivity,acl_revision,status | note_id globally unique、revision DB単調、同ID複製は隔離 |
| knowledge_validations | validation_id,target_ref,validated_hash,claim_id,assertion_type,scope,suite_id,suite_version,dataset_hash,runner_id,status,evidence_ids,adopted_by,verified_at,expires_at | PassedとVerified採用は別。対象hash/適合suite/証拠/ownerを同時確認 |
| knowledge_sources / knowledge_edges | source_id,hash,scope / edge_id,from_note_id,to_note_id,relation | relation列挙、削除・失効は依存先へ伝播 |
| memory_candidates | candidate_id,target_note_id,base_snapshot_ref,base_hash,proposed_snapshot_ref,proposed_hash,state,version | 未承認は通常検索対象外、元本文なしで3-way mergeしない |
| actions | action_id,envelope,schema_version,action_hash,policy_revision,expires_at | 不変。修正は新ID。canonical hash、宛先/環境/tool版まで固定 |
| approval_requests | approval_id,action_id,actor_id,status,version,decided_at,consumed_by_operation_id | action当たり一つの実行消費。expiryはserver UTC |
| operations / write_operations | operation_id,action_id,status,version,known_effects,journal_ref,base/proposed/current_hash | UNIQUE(action_id)、FS/DB跨ぎはOutcomeUnknownを許容 |
| jobs / job_steps | job_id,owner_id,state,state_version,policy_revision,execution_manifest_hash,parent_job_id,job_taint / step_id,job_id,kind,order,input_hash,dependency_fingerprint,output_ref | 実行manifest不変。成功effect再送禁止、pure再利用は依存一致時だけ |
| job_attempts | attempt_id,job_id,attempt_no,lease_owner,lease_until,fencing_token,status | job+attempt_no unique。token単調、旧token結果採用拒否 |
| tool_executions | exec_id,step_id,attempt_id,operation_id,idempotency_key,external_ref,outcome | logical operationの重複禁止、外部照合不能なら保留 |
| idempotency_records | actor_id,method,path,key,request_hash,operation_id,response_ref,retain_until | 複合unique、異なるbodyは409 |
| revocations | revocation_id,note_id,epoch,reason,at,actor_id | append-only tombstone、権限縮小も世代更新、復元で巻戻さない |
| publication_records / dependencies | publication_id,job_id,permit_epoch,output_hash,state / note_id,hash,acl_revision | 公開と失効受付を直列化、全派生物の依存記録必須 |
| consents | consent_id,final_envelope_hash,destination,purpose,classification,expires_at,revoked_at,send_claim_id | publicかつjob_taint=publicだけ。claim前取消は停止、後は照合 |
| evidence / audit_events | evidence_id,storage_ref,hash,sensitivity / event_id,correlation_id,actor,action,target,at,payload_hash | 原文secretをauditへ載せない。append-only権限、連鎖hashと保全anchorを検証 |
| budget_reservations | reservation_id,job_id,amount,currency,pricing_version,status,actual_cost | 同時予約をDB直列化、job/月の上限両方検査 |
| evaluation_runs | run_id,manifest_ref,manifest_hash,dataset_version,corpus_hash,metrics_ref,status | frozen後変更禁止、訂正は新run、失敗も保持 |
| settings_policies | policy_id,revision,classification_rules,egress_rules,limits,retention_profile | immutable revision、変更者監査、未知分類deny |
| backup_manifests | backup_id,db_lsn,vault_snapshot,evidence_manifest,revocation_epoch,policy_revision,key_id,hash,verified_at | 世代対応、restore隔離、最新失効台帳の合成必須 |

## 知識属性の権威
本文・可搬属性はMarkdown、ACL/送信同意/失効/技術検証証拠はDB/Policy。`status`や`sensitivity`のFrontmatterは観測入力であり昇格権限ではない。最終有効権限はDBとpolicyと本文分類の最も厳しいもの。非比較分類や未知値はdeny。検証はvalidated_hash=content_hash、証拠有効、scope一致の場合だけ有効。本文変更時はrevisionをDB側で進め、検証を失効させる。手動revisionをDBへ強制上書きしない。

## 派生索引と保持
FTS/embeddingはnote_id,indexed_hash,permission_scope,acl_revision,revocation_epoch,index_generationを必須化。候補取得前ACL filter、返却/公開直前も現在版で照合。旧世代と新世代を混在させない。削除は論理denyを先に確定し、cache/索引/派生要約/生成buffer/成果物を無効化する。

保持・消去・backup鍵の保存期間はrelease前決定事項。監査に残す最小hash/イベント、本文snapshot、復元tombstoneを分離する。消去要求時は対象と期限、バックアップ残存と回収不能な既送信先を表示し、物理消去完了を論理失効完了と混同しない。鍵削除だけを物理消去検証と同一視しない。

## v0.11 由来・実行・検証の追加entity

| Entity | 主な要素 | 不変条件 |
|---|---|---|
| derived_artifacts | artifact_id,content_hash,source_ids/source_hashes,effective_classification,policy_revision,job_taint | 要約/export/再添付でも由来保持。不明はdeny、job taint低下なし |
| egress_envelopes | envelope_id,hash,body_hash,attachment_hashes,destination,provider,model,adapter_version,source_hashes,policy_revision,budget_reservation_id,expires_at | adapter構築後不変。consent/actionとhash一致、秘密credentialは参照だけ |
| execution_manifests | manifest_id,job_id,input_hashes,plan_hash,model/prompt/tool_versions,scope,policy_revision,knowledge_dependencies | Running後変更禁止。変更は新jobへfork |
| effect_ledger | logical_effect_key,origin_operation_id,lineage_root_id,target,owner,status,external_ref | 系譜を跨ぐ同一副作用を照合。forkで不明/完了を再送しない |
| validation_suites | suite_id,version,allowed_claim_kinds,scope_rules,dataset_hashes,runner_policy,status | registry適合のない主張は技術Verified不可、撤回は依存証拠を失効 |

snapshot、rendered/export派生物は本文の別正本にしない。source chainとtaintはDBで強制し、FrontmatterやLLM出力を信用してpublic化しない。validation採用のtransaction/画面/APIはEXECUTION_CONTRACTS参照。実装前のschema整合は確認できるが、制約の実効性と性能は実装後の試験対象。

## v0.12 認証の所有データ

| Entity | 主な要素 | 不変条件 |
|---|---|---|
| pairing_challenges | challenge_id,code_hash,client_nonce_hash,expires_at,attempts,consumed_at,native_approval_ref | native発行限定、一回消費、秘密codeは保管/監査しない |

sessionsへsession_version,csrf_token_hash,rotated_from,created_at,last_seenを追加。session/CSRFは同時rotation/失効。認証bootstrapと失効を監査し生secretを含めない。TEST-SEC-001で旧session/CSRF再使用を拒否。