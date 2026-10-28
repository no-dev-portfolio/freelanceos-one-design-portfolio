# DOC-09 API契約 v0.10（未実装）

**改訂:** 2026-10-25 / CR-001 / 設計候補。重要ADRはProposed、実機未検証。審査基準・影響・比較案は [改修計画](../08-governance/DESIGN_REMEDIATION.md)。

## 共通契約
`/api/v1` / JSON UTF-8。単一利用者でも認証必須。初回のlocal pairingでsessionを確立し、secretをURL/ログへ載せない。cookieはHttpOnly/SameSite=Strict、TLS経路ではSecure。変更APIはsessionに束縛したCSRF token、exact Origin/Host allowlist、owner権限を検査する。CORS wildcard禁止。loopback HTTPはローカル限定候補であり、remote/mobileはTLSと追加認証の設計受容まで公開しない。session更新・失効、pairing秘密の保管・rotationはTEST-SEC-001対象。

原則、全変更APIは`Idempotency-Key`必須。認証bootstrapの例外とscopeは末尾の認証契約で限定する。scopeはactor+method+canonical path。正規化body hashが同じ再送は同じoperation/statusを返し、同keyで異なるbodyは409 IDEMPOTENCY_CONFLICT。キーは対応するoperationの監査保持期間が終了する前に削除しない。保持期間未決なら実運用不可。keyだけで外部副作用exactly-onceを主張しない。

成功受付は202とoperation_id/location、状態参照は200。401未認証、403禁止、404は存在秘匿が必要な対象、409版/状態競合、410既知失効、422schema不正、429rate/budget、503依存不達。403/404差で権限外データの存在を漏らさない。本文にcode/message/retryable/correlation_id/details（秘匿）/operation_idを持つ。OutcomeUnknownはretryable=false。ページcursorは不透明署名cursorとしlimit最大100、job本文64KiB、添付10MiB、timeout 30秒を**受入候補値**とする。超過は副作用前拒否。長時間処理は202で継続し、待受timeoutを取消と扱わない。

## エンドポイント
全行はowner/user/approverをサーバーで検査。agentは限定service identityを使い、権限昇格不可。

| Method | Path | request / result | 権限・競合 |
|---|---|---|---|
| GET | /health | 最小稼働状態だけ | 本文・path・接続secretは返さない |
| POST | /auth/pairing | challenge_id,one_time_code,client_nonce → session cookie,csrf_token,expires_at | nativeローカル承認済みchallenge、短時間一回消費、Origin/Host厳格照合 |
| GET | /auth/session | actor_id,expires_at,capabilities | owner session、secretやcookieをbodyへ複製しない |
| GET | /auth/csrf | csrf_token,session_version | owner session、no-store、exact Origin/Host |
| POST | /auth/session/refresh | csrf_token → rotated cookie,csrf_token,expires_at | owner、旧session/CSRFは同一transactionで失効 |
| DELETE | /auth/session | current session revoke → 204 | owner、CSRF必須、cookie消去、再実行は失効を緩和しない |
| GET | /auth/sessions | cursor,limit → active session summaries,next_cursor | owner、secretなし |
| DELETE | /auth/sessions/{id} | expected_version → 204 | owner、対象session即失効、他actorは秘匿404 |
| GET | /jobs | status?,cursor?,limit? → items,next_cursor | owner、固定updated_at/id順、本文なし、ACL前filterと返却再認可 |
| GET | /knowledge/candidates | status?,cursor?,limit? → candidate summaries,next_cursor | owner/reviewer、通常知識検索と別projection |
| GET | /knowledge/candidates/{id} | base/proposed hashes,text,evidence_refs,state,version | owner/reviewer、候補と証拠を再認可 |
| GET | /settings | policy_revision,capabilities,redacted_profiles | owner、credentialは参照IDだけ |
| GET | /consents | status?,cursor?,limit? → consent summaries,next_cursor | owner、期限/失効/宛先/対象hash、credentialなし |
| POST | /jobs | goal,input_refs,model_profile,max_steps,budget_jpy → job_id,operation_id | owner、model/分類/予算前検査 |
| GET | /jobs/{job_id} | state,attempt,sequence,steps,capabilities,blocked_reason | owner、全文の再認可 |
| GET | /jobs/{job_id}/events | after_sequence → event page,last_sequence | owner、欠番はsnapshot再取得 |
| POST | /jobs/{job_id}/cancel | expected_state_version → operation | owner、実停止点を返す |
| POST | /jobs/{job_id}/resume | expected_state_version,reconciliation_ref? | 不変execution_manifestのFailed/Blocked/Cancelledから新attempt。変更はfork、OutcomeUnknownは照合必須 |
| POST | /jobs/{job_id}/fork | corrected_input_refs,new_plan,reason,expected_state_version → new_job_id | owner、元job不変、taint/副作用ledger継承 |
| GET | /operations/{id} | status,reason,known_effects,next_actions | owner、同一key再送の照会先 |
| POST | /operations/{id}/reconcile | expected_version,evidence_refs,resolution | owner、人間判断、再送は別action/新承認 |
| POST | /attachments | bytes,classification → input_ref,hash | owner、型/長さ/隔離。未分類はdeny |
| GET | /knowledge/search | query,scope,limit,cursor → ids/citations,epoch | ACL前filter、返却時再認可 |
| GET | /knowledge/{note_id} | revision? → content,hash,status,validation | 現ACL/失効を確認、旧版で迂回不可 |
| POST | /knowledge/candidates | target_note_id?,base_hash?,content_ref,sources | agent/user、候補専用store |
| POST | /knowledge/candidates/{id}/resubmit | expected_version,new_content_ref | owner、旧承認失効、新action |
| POST | /knowledge/validations | target_ref,expected_content_hash,claim_id,assertion_type,scope,suite_id/version,dataset_ref/hash → validation_id,operation_id | owner/限定service、registry適合、任意試験不可 |
| GET | /knowledge/validations/{id} | status,target_hash,suite,evidence_refs,next_actions | owner、本文/証拠再認可 |
| POST | /knowledge/validations/{id}/adopt | expected_target_hash,expected_state_version,evidence_refs → operation_id | owner人間、Passed/適合証拠/現hashを確定的gateで再検査 |
| POST | /knowledge/{note_id}/revoke | expected_version,reason → epoch | owner、tombstone+audit同時確定 |
| POST | /actions | target,tool,input_refs,base/proposed hash,policy_revision | Policy service、不変envelope生成 |
| GET | /approvals | cursor,status → action summary | approver、一覧と文脈内は同一projection |
| POST | /approvals/{id}/decision | decision,action_hash,expected_version | approver、server時刻で期限判定 |
| POST | /approvals/{id}/cancel | expected_version | approver、claim前のみ取消。claim後409 TOO_LATE |
| POST | /vaults | local pickerのopaque capability,permission_profile → vault_id | owner、任意raw pathを受け付けずroot同一性/権限を確認 |
| GET | /vaults/{id}/status | sync_state,writer_mode,last_seen,index_generation | owner、不明をsuccessにしない |
| PATCH | /settings | expected_policy_revision,profile,budget,permissions | owner、機密縮小は即時、進行jobを再認可 |
| POST | /consents | final_envelope_hash,expiry,purpose,destination | owner、publicだけ、全外向き経路を対象 |
| DELETE | /consents/{id} | revoke | owner、未公開/未送信を停止、既送信回収不能 |
| POST | /backups | quiesce_request → operation/manifest | owner、鍵と失効台帳を検証 |
| POST | /restores | manifest_id,dry_run → isolated operation | owner、公開は別承認 |
| POST | /exports | job_id,time_range?,format=txt/json,redacted_preview_hash → operation | owner、保存成功とマスク結果を確認 |
| POST | /evaluation-runs | preregistered_manifest_id → run_id | owner、holdoutアクセス制限、予算予約 |
| GET | /evaluation-runs/{id} | manifest,metrics,failures,limitations | owner、採点用正解を通常agentへ返さない |

## 不変actionと承認
canonical JSONはキー順序・UTF-8・数値表現を固定し、schema_versionを含める。`action_id,actor_id,vault_id,target_id,target_environment,tool_id,tool_version,input_hashes,base_hash,proposed_hash,policy_revision,egress_preview_hash,budget_reservation_id,expires_at`をhash対象とする。サーバーがhashを再計算し、client hashを権威にしない。対象・宛先・版・本文・policyが変われば新action/再承認。

承認decisionは副作用そのものではない。Approved→Claimedへの一回消費をoperation作成・監査・lease取得と同一DB transactionにする。UNIQUE(action_id)と消費参照で二重claimを拒否する。cancel/expire/claimは同じ行lockで直列化。claim前取消は成功、claim後は取消不能点と既知副作用を返す。実行前のpolicy再検査で拒否なら不実行として確定し、新承認を要求。監査永続化不能なら高リスク実行を開始しない。

## エラーと再試行
REVISION_CONFLICT、KNOWLEDGE_STALE、REVOKED_EVIDENCE、MODEL_UNAVAILABLE、WRITER_UNSAFE、APPROVAL_EXPIRED、POLICY_CHANGED、BUDGET_EXCEEDED、AUDIT_UNAVAILABLE、TOOL_OUTCOME_UNKNOWNを画面の次操作へmappingする。通信断ならoperationを照会し、同じ副作用を新keyで再送しない。raw SQL・任意path・任意commandの入力は禁止。P1 DB接続はschema allowlist、読取専用credential、timeout/row limit、資格情報を参照IDで扱う別契約を審査するまで無効。

## v0.11 CR-002 契約の追加

[EXECUTION_CONTRACTS](EXECUTION_CONTRACTS.md) が派生分類・最終egress・不変resume/fork・validationの詳細仕様。全変更APIに既存Idempotency-Key/owner/expected versionを適用。入力/plan変更resumeは409 INPUT_CHANGED_USE_FORK、旧計算再利用不可は409 DEPENDENCY_STALE、検証不適合は422 VALIDATION_SCOPE_MISMATCH、旧hashは409 VALIDATION_STALE。envelope変化は409 CONSENT_STALE、taint/由来不明は403 CLASSIFICATION_DENIED。正解や権限外の原文をdetailsへ入れない。

forkは新jobでも副作用ledgerと非public由来を引き継ぐ。validation requestの202は試験合格ではなく受付。adoptは機械証拠の状態/対象/適合と人間権限の両方を検査しauditと同時確定する。P0 content/snippet/error/diff/exportは [CONTENT_PRESENTATION](../02-ux/CONTENT_PRESENTATION.md) の非実行text契約、raw HTMLと自動remote resourceを返すAPIとして使わない。

全通信body/添付の最終hashをconsentへ束縛し、同意後にadapter内容を追加しない。API auth secretはpreview/本文hash監査へ複製しない。canonical JSONはschemaで許可したUTF-8文字列/boolean/null/有限整数/配列/objectに限定、重複keyとNaN/Infinity/曖昧floatは拒否。body hashはcanonical envelopeと別に実送信bytesを照合する。価格小数は通貨最小単位の整数で扱う。実際のHTTPやtransactionの成立は実装後試験。

## v0.12 認証bootstrapと一覧契約（REQ-SEC-001）

challengeの発行はOSユーザーが操作するnative設定画面内だけで行う。未認証HTTP経由でchallenge/one-time-codeを取得するrouteは提供しない。native画面がない環境はpairing不可でBlocked。コードは暗号学的乱数、短時間TTL・試行回数制限・rate limitを実装前のsecurity設定として固定し、未設定では起動不可。challenge_idとcode hash、expiry、attempts、consumed_atをDBへ保存。codeをURL、監査本文、ブラウザ永続storageへ保存しない。

POST /auth/pairingだけはsession/CSRFの事前保有を不要とするが、許可済みexact Origin/Host、JSON content-type、nativeで表示したclient_nonce束縛とchallengeを検査する。HTTP変更の例外はこの一箇所。Idempotency-Key scopeはchallenge_id+client_nonce+method+path、消費済みコードの再送で新sessionやsecretを再発行しない。結果不明はnativeから旧発行sessionを失効して新challenge。以後の変更APIはsession/CSRF/Idempotency-Keyを必須とする。session失効DELETEの同一key再送はsecretを含まない204だけ返せるが、無効sessionで他操作はできない。

session cookieはHttpOnly/SameSite=Strict（TLSはSecure）、CSRFはsession_versionへ束縛しメモリだけに保持。refreshは成功応答に旧tokenを含めず、旧session/CSRFを無効化。logout/個別失効は各リクエストとjob公開/実行直前に検査し、進行中操作の未実行部分を停止する。消費済み外部作用を取消成功と表示しない。認証APIもCache-Control: no-store、GETは状態変更なし。agent service identityにはpairing/session管理権限を与えない。

一覧routeは同じopaque cursor/最大100件/安定したsnapshot順/ACL前filterと返却再認可、失効cursorは409 CURSOR_STALEで再取得。存在秘匿・empty/loading/offlineを区別し、candidate本文は専用detail経路でだけ表示。固定path /knowledge/candidates、/knowledge/search、/knowledge/validationsを可変 /knowledge/{note_id} より先に解決する。GET一覧追加は承認や実行の権限を増やさない。
