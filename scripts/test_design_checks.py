"""Destructive fixtures for the document validators, never application tests."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import check_design
import check_review_gate

class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'repo'
        shutil.copytree(check_design.ROOT, self.root)
    def tearDown(self):
        self.tmp.cleanup()
    def change_state(self, **values):
        p = self.root / 'reviews/review-state.json'
        data = json.loads(p.read_text()); data.update(values)
        p.write_text(json.dumps(data))
    def test_valid_documents(self):
        self.assertEqual(check_design.validate(self.root)[0], [])
        self.assertEqual(check_review_gate.validate(self.root)[0], [])
    def test_missing_required_file(self):
        (self.root/'templates/CHANGE_REQUEST.md').unlink()
        self.assertTrue(check_design.validate(self.root)[0])
    def test_broken_link(self):
        with (self.root/'README.md').open('a') as f:
            f.write('\n[missing](docs/does-not-exist.md)\n')
        self.assertTrue(check_design.validate(self.root)[0])
    def test_undefined_and_missing_test(self):
        p=self.root/'docs/08-governance/TRACEABILITY.md'
        p.write_text(p.read_text().replace('TEST-UX-001','TEST-UX-999'))
        self.assertTrue(check_design.validate(self.root)[0])
    def test_malformed_commit_type(self):
        self.change_state(reviewed_commit=[])
        self.assertTrue(check_review_gate.validate(self.root)[0])
    def test_malformed_json(self):
        (self.root/'reviews/review-state.json').write_text('{broken')
        self.assertTrue(check_review_gate.validate(self.root)[0])
    def test_duplicate_requirement(self):
        p=self.root/'docs/01-product/REQUIREMENTS.md'
        p.write_text(p.read_text().replace('REQ-UX-002 |','REQ-UX-001 |'))
        self.assertTrue(check_design.validate(self.root)[0])
    def test_unknown_phase(self):
        self.change_state(phase='everything_done')
        self.assertTrue(check_review_gate.validate(self.root)[0])
    def test_completion_without_human_acceptance(self):
        self.change_state(phase='codex_complete')
        self.assertTrue(check_review_gate.validate(self.root)[0])
    def test_forged_execution_status(self):
        p=self.root/'reviews/codex/execution.json';d=json.loads(p.read_text())
        d['exit_code']=1;p.write_text(json.dumps(d))
        self.assertTrue(check_review_gate.validate(self.root)[0])
    def test_premature_claude(self):
        self.change_state(claude_started=True)
        self.assertTrue(check_review_gate.validate(self.root)[0])
    def test_implementation_flag(self):
        self.change_state(implementation_authorized=True)
        self.assertTrue(check_review_gate.validate(self.root)[0])

    def trace_cell(self, req, column, transform):
        p = self.root/'docs/08-governance/TRACEABILITY.md'
        lines = p.read_text().splitlines()
        for i, line in enumerate(lines):
            if line.startswith('| '+req+' |'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                cells[column] = transform(cells[column])
                lines[i] = '| '+' | '.join(cells)+' |'
        p.write_text('\n'.join(lines)+'\n')
    def accepted_primary(self):
        (self.root/'fixture-acceptance.txt').write_text('Synthetic acceptance fixture; not real approval')
        self.change_state(phase='codex_complete', human_acceptance='accepted',
                          human_acceptance_ref='fixture-acceptance.txt')
    def test_primary_tests_swapped(self):
        self.trace_cell('REQ-UX-001',5,lambda s:s.replace('TEST-UX-001','TEST-UX-002'))
        self.trace_cell('REQ-UX-002',5,lambda s:s.replace('TEST-UX-002','TEST-UX-001'))
        self.assertTrue(any('primary test mismatch' in e for e in check_design.validate(self.root)[0]))
    def test_undefined_screen_in_shorthand(self):
        self.trace_cell('REQ-UX-001',2,lambda s:'SCR-00/99')
        self.assertIn('undefined screen: SCR-99',check_design.validate(self.root)[0])
    def test_valid_shorthand_remains_supported(self):
        self.trace_cell('REQ-UX-001',2,lambda s:'SCR-00/01/02/04/06/10')
        self.assertEqual(check_design.validate(self.root)[0],[])
    def test_undefined_api_route(self):
        self.trace_cell('REQ-UX-001',3,lambda s:s+',/unknown-route')
        self.assertIn('undefined API route: /unknown-route',check_design.validate(self.root)[0])
    def test_undefined_entity(self):
        self.trace_cell('REQ-UX-001',4,lambda s:s+',unknown_entity')
        self.assertIn('undefined entity: unknown_entity',check_design.validate(self.root)[0])
    def test_report_commit_only_in_history(self):
        p=self.root/'reviews/codex/REVIEW.md';d=json.loads((self.root/'reviews/review-state.json').read_text())
        p.write_text(p.read_text().replace('| 対象commit | `'+d['reviewed_commit']+'` |','| 対象commit | `'+('0'*40)+'` |')+'\nHistorical commit '+d['reviewed_commit'])
        self.assertIn('active report target commit missing/mismatched',check_review_gate.validate(self.root)[0])
    def test_report_tampered_with_same_commit(self):
        p=self.root/'reviews/codex/REVIEW.md';p.write_text(p.read_text()+'\nChanged finding\n')
        self.assertIn('active artifact digest mismatch: report',check_review_gate.validate(self.root)[0])
    def test_source_manifest_tampered(self):
        active=json.loads((self.root/'reviews/active-review.json').read_text())
        p=self.root/active['artifacts']['source_manifest']['path'];p.write_text(p.read_text()+'\n ')
        self.assertIn('active artifact digest mismatch: source_manifest',check_review_gate.validate(self.root)[0])
    def test_started_under_recorded_phase(self):
        self.accepted_primary()
        self.change_state(phase='codex_review_recorded',claude_started=True,
                          claude_artifact='README.md',claude_execution_ref='README.md',
                          claude_reviewed_commit='edcebcc650ec123913ac0407daa32aa2055349a5')
        self.assertIn('recorded phase conflicts with acceptance/Claude start',check_review_gate.validate(self.root)[0])
    def test_valid_primary_accepted_state(self):
        self.accepted_primary()
        self.assertEqual(check_review_gate.validate(self.root)[0],[])
    def test_claude_complete_requires_started(self):
        self.accepted_primary();self.change_state(phase='claude_complete')
        self.assertIn('Claude phase requires started=true',check_review_gate.validate(self.root)[0])
    def test_claude_baseline_mismatch(self):
        self.accepted_primary()
        self.change_state(phase='claude_reviewing',claude_started=True,
                          claude_reviewed_commit='0'*40,claude_execution_ref='README.md')
        self.assertIn('Claude baseline mismatch',check_review_gate.validate(self.root)[0])
    def test_active_session_mismatch(self):
        p=self.root/'reviews/active-review.json';a=json.loads(p.read_text());a['cli_session_id']='other-session';p.write_text(json.dumps(a))
        self.assertIn('active review commit/session mismatch',check_review_gate.validate(self.root)[0])
    def test_runtime_cannot_be_marked_passed_without_implementation(self):
        p=self.root/'docs/06-quality/verification-register.json';d=json.loads(p.read_text());d['items'][0]['status']='passed';p.write_text(json.dumps(d))
        self.assertIn('runtime execution without implementation authorization',check_design.validate(self.root)[0])
    def test_runtime_register_missing_test(self):
        p=self.root/'docs/06-quality/verification-register.json';d=json.loads(p.read_text());d['items'].pop();p.write_text(json.dumps(d))
        self.assertIn('runtime register/test plan mismatch',check_design.validate(self.root)[0])
    def test_runtime_return_design_path_missing(self):
        p=self.root/'docs/06-quality/verification-register.json';d=json.loads(p.read_text());d['items'][0]['design_return_paths']=['missing.md'];p.write_text(json.dumps(d))
        self.assertIn('invalid design return path: missing.md',check_design.validate(self.root)[0])

    def update_json(self, name, **changes):
        p = self.root / name
        data = json.loads(p.read_text())
        data.update(changes)
        p.write_text(json.dumps(data))

    def assert_release_rejected(self, expected):
        for validator in (check_design.validate, check_review_gate.validate):
            errors, _ = validator(self.root)
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_m7_register_authorization_and_acceptance_forgery(self):
        self.update_json('docs/06-quality/verification-register.json',
                         application_implementation_authorized=True,
                         runtime_acceptance='accepted')
        self.assert_release_rejected('implementation authorization mismatch')
        self.assert_release_rejected('every plan passed with evidence')

    def test_register_authorization_only(self):
        self.update_json('docs/06-quality/verification-register.json',
                         application_implementation_authorized=True)
        self.assert_release_rejected('implementation authorization mismatch')

    def test_design_status_authorization_only(self):
        self.update_json('docs/08-governance/DESIGN_STATUS.json',
                         application_implementation_authorized=True)
        self.assert_release_rejected('implementation authorization mismatch')

    def test_string_authorization_rejected(self):
        self.update_json('docs/06-quality/verification-register.json',
                         application_implementation_authorized='false')
        self.assert_release_rejected('flags must be boolean')

    def test_all_authorizations_enabled_still_design_only(self):
        self.change_state(implementation_authorized=True)
        for name in ('docs/06-quality/verification-register.json',
                     'docs/08-governance/DESIGN_STATUS.json'):
            self.update_json(name, application_implementation_authorized=True)
        self.assert_release_rejected('all implementation authorizations must be false')

    def test_acceptance_mismatch(self):
        self.update_json('docs/08-governance/DESIGN_STATUS.json', runtime_acceptance='accepted')
        self.assert_release_rejected('runtime acceptance mismatch')

    def test_unknown_acceptance_rejected(self):
        for name in ('docs/06-quality/verification-register.json',
                     'docs/08-governance/DESIGN_STATUS.json'):
            self.update_json(name, runtime_acceptance='done')
        self.assert_release_rejected('invalid runtime acceptance')

    def test_acceptance_with_not_run_rejected(self):
        for name in ('docs/06-quality/verification-register.json',
                     'docs/08-governance/DESIGN_STATUS.json'):
            self.update_json(name, runtime_acceptance='accepted')
        self.assert_release_rejected('every plan passed with evidence')

    def test_fabricated_complete_results_cannot_enable_design_package(self):
        p = self.root / 'docs/06-quality/verification-register.json'
        data = json.loads(p.read_text())
        for item in data['items']:
            item.update(status='passed', actual_result='fabricated fixture',
                        executed_by='fixture', executed_at='2026-10-28',
                        evidence_refs=['README.md'], attempts=[{'fixture': True}])
        data.update(application_implementation_authorized=True, runtime_acceptance='accepted')
        p.write_text(json.dumps(data))
        self.change_state(implementation_authorized=True)
        self.update_json('docs/08-governance/DESIGN_STATUS.json',
                         application_implementation_authorized=True, runtime_acceptance='accepted')
        self.assert_release_rejected('runtime acceptance cannot be enabled here')

    def test_missing_design_state(self):
        (self.root / 'docs/08-governance/DESIGN_STATUS.json').unlink()
        self.assert_release_rejected('invalid release state')

    def test_missing_register_rejected_by_both(self):
        (self.root / 'docs/06-quality/verification-register.json').unlink()
        self.assertTrue(check_design.validate(self.root)[0])
        self.assertTrue(check_review_gate.validate(self.root)[0])

    def test_register_non_object_item(self):
        p = self.root / 'docs/06-quality/verification-register.json'
        data = json.loads(p.read_text()); data['items'][0] = None
        p.write_text(json.dumps(data))
        self.assert_release_rejected('invalid runtime acceptance test items')

    def remove_route(self, method, route):
        p = self.root / 'docs/03-architecture/API_CONTRACT.md'
        p.write_text('\n'.join(line for line in p.read_text().splitlines()
                               if not line.startswith('| '+method+' | '+route+' |'))+'\n')

    def test_missing_jobs_get_not_masked_by_post(self):
        self.remove_route('GET', '/jobs')
        self.assertIn('undefined screen API: SCR-02: GET /jobs', check_design.validate(self.root)[0])

    def test_missing_auth_pairing_route(self):
        self.remove_route('POST', '/auth/pairing')
        self.assertIn('undefined screen API: SCR-00: POST /auth/pairing', check_design.validate(self.root)[0])

    def test_missing_auth_requirement(self):
        p = self.root / 'docs/01-product/REQUIREMENTS.md'
        p.write_text('\n'.join(line for line in p.read_text().splitlines()
                               if not line.startswith('| REQ-SEC-001 |'))+'\n')
        self.assertIn('authentication requirement/acceptance missing', check_design.validate(self.root)[0])

    def test_missing_required_screen_mapping(self):
        p = self.root / 'docs/02-ux/screen-api-contracts.json'
        data = json.loads(p.read_text()); data['screens']['SCR-02'] = [{'method':'GET','path':'/health'}]
        p.write_text(json.dumps(data))
        self.assertIn('missing mandatory screen API: SCR-02', check_design.validate(self.root)[0])

    def test_missing_settings_read(self):
        self.remove_route('GET', '/settings')
        self.assertIn('undefined screen API: SCR-09: GET /settings', check_design.validate(self.root)[0])

    def test_missing_candidate_list(self):
        self.remove_route('GET', '/knowledge/candidates')
        self.assertIn('undefined screen API: SCR-05: GET /knowledge/candidates', check_design.validate(self.root)[0])

    def test_invalid_slice(self):
        self.trace_cell('REQ-UX-001', 7, lambda _: 'unknown')
        self.assertIn('invalid implementation slice: REQ-UX-001', check_design.validate(self.root)[0])

    def test_p0_deferred_without_design_revision(self):
        self.trace_cell('REQ-UX-001', 7, lambda _: 'deferred')
        self.assertIn('P0 cannot be deferred without explicit design revision: REQ-UX-001',
                      check_design.validate(self.root)[0])

    def test_source_drift_warns_without_changing_historical_evidence(self):
        self.assertTrue(any('REVIEW_SOURCE_DRIFT' in warning
                            for warning in check_review_gate.review_warnings(self.root)))
        self.assertEqual(check_review_gate.validate(self.root)[0], [])

    def test_unreadable_source_manifest_warning(self):
        p = self.root / 'reviews/codex/round-2/source-manifest.json'
        p.write_text('{}')
        self.assertTrue(any('REVIEW_SOURCE_UNVERIFIED' in warning
                            for warning in check_review_gate.review_warnings(self.root)))

    def test_source_matching_manifest_has_no_drift_warning(self):
        import hashlib
        data = b'synthetic source'
        source = self.root / 'isolated-source.txt'; source.write_bytes(data)
        digest = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        tree = [{'type':'blob', 'path':'isolated-source.txt', 'sha':digest}]
        # Use a minimal isolated tree to test the warning function, not approval.
        for folder in ('docs','scripts','handoff','wireframes','.github'):
            shutil.rmtree(self.root / folder, ignore_errors=True)
        manifest = self.root / 'reviews/codex/round-2/source-manifest.json'
        manifest.write_text(json.dumps({'tree':tree}))
        self.assertEqual(check_review_gate.review_warnings(self.root), [])
        (self.root / 'docs').mkdir()
        (self.root / 'docs/new.md').write_text('new unreviewed source')
        self.assertTrue(any('REVIEW_SOURCE_DRIFT' in warning
                            for warning in check_review_gate.review_warnings(self.root)))

if __name__ == '__main__':
    unittest.main()
