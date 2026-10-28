"""Validate design artifact structure; never a behavioral or safety certification."""
import re
import json
import sys
from pathlib import Path
from urllib.parse import unquote
from check_release_state import validate as validate_release_state

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'AGENTS.md', 'README.md', 'docs/01-product/PRD.md',
    'docs/01-product/REQUIREMENTS.md', 'docs/02-ux/SCREEN_SPEC.md',
    'docs/02-ux/INFORMATION_ARCHITECTURE.md', 'docs/02-ux/DESIGN_SYSTEM.md',
    'docs/03-architecture/SYSTEM_DESIGN.md', 'docs/03-architecture/API_CONTRACT.md',
    'docs/03-architecture/DATA_MODEL.md', 'docs/04-knowledge/KNOWLEDGE_MODEL.md',
    'docs/04-knowledge/GROWTH_EVALUATION.md', 'docs/05-agent/AGENT_AND_TOOLS.md',
    'docs/06-quality/THREAT_MODEL.md', 'docs/06-quality/VERIFICATION_PLAN.md',
    'docs/07-delivery/PHASES.md', 'docs/08-governance/TRACEABILITY.md',
    'docs/08-governance/DESIGN_REMEDIATION.md', 'docs/08-governance/ISSUES.md',
    'docs/08-governance/DECISIONS.md', 'docs/08-governance/REVIEW_LOG.md',
    'templates/CHANGE_REQUEST.md', 'wireframes/STORYBOARD.md',
    'reviews/CODEX_REVIEW_TEMPLATE.md', 'reviews/codex/REVIEW.md',
    'reviews/codex/REMEDIATION.md', 'reviews/codex/VALIDATION.md',
    'reviews/review-state.json', 'scripts/check_review_gate.py',
    'scripts/test_design_checks.py', 'reviews/active-review.json',
    'docs/03-architecture/EXECUTION_CONTRACTS.md',
    'docs/02-ux/CONTENT_PRESENTATION.md',
    'docs/06-quality/POST_IMPLEMENTATION_VALIDATION.md',
    'docs/06-quality/verification-register.json',
    'docs/08-governance/DESIGN_REMEDIATION_2.md',
    'scripts/check_release_state.py',
    'docs/02-ux/screen-api-contracts.json',
    'docs/06-quality/FEASIBILITY_SPIKES.md',
    'docs/08-governance/DESIGN_REMEDIATION_3.md',
)

def table_rows(text):
    return [[c.strip() for c in line.strip().strip('|').split('|')]
            for line in text.splitlines() if line.startswith('|')]

def screen_ids(cell):
    result = []
    for group in re.split(r'\s*,\s*', cell):
        if not re.fullmatch(r'SCR-\d{2}(?:/\d{2})*', group):
            raise ValueError('invalid screen syntax: ' + cell)
        result.extend('SCR-' + number for number in group[4:].split('/'))
    return result

def validate(root):
    root = Path(root).resolve()
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append('missing artifact: ' + name)
    if errors:
        return errors, {}
    req_text = (root / 'docs/01-product/REQUIREMENTS.md').read_text()
    req_rows = [row for row in table_rows(req_text)
                if re.fullmatch(r'REQ-[A-Z]+-\d{3}', row[0])]
    reqs = [row[0] for row in req_rows]
    if len(reqs) != 28 or len(set(reqs)) != 28:
        errors.append('expected 28 unique requirement definitions')
    plan = (root / 'docs/06-quality/VERIFICATION_PLAN.md').read_text()
    test_rows = [row for row in table_rows(plan)
                 if re.fullmatch(r'TEST-[A-Z]+-\d{3}', row[0])]
    tests = [row[0] for row in test_rows]
    if len(tests) != 37 or len(set(tests)) != 37:
        errors.append('expected 37 unique test plan definitions')
    for row in req_rows:
        for test in re.findall(r'TEST-[A-Z]+-\d{3}', row[-1]):
            if test not in tests:
                errors.append('requirement references undefined test: ' + test)
    trace_text = (root / 'docs/08-governance/TRACEABILITY.md').read_text()
    trace = [row for row in table_rows(trace_text)
             if re.fullmatch(r'REQ-[A-Z]+-\d{3}', row[0])]
    traced = [row[0] for row in trace]
    if set(reqs) != set(traced) or len(traced) != len(set(traced)):
        errors.append('requirement/trace definitions mismatch or duplicate')
    primary_tests = {row[0]: set(re.findall(r"TEST-[A-Z]+-\d{3}", row[-1])) for row in req_rows}
    traced_tests = set()
    for row in trace:
        if len(row) == 8 and row[7] not in ('S1', 'S2', 'deferred'):
            errors.append('invalid implementation slice: ' + row[0])
        if len(row) == 8 and row[7] == 'deferred' and any(
                req[0] == row[0] and req[1] == 'P0' for req in req_rows):
            errors.append('P0 cannot be deferred without explicit design revision: ' + row[0])
    for row in trace:
        if len(row) != 8 or any(not cell for cell in row):
            errors.append('incomplete trace row: ' + row[0])
            continue
        if not primary_tests.get(row[0]) or not primary_tests[row[0]].issubset(set(re.findall(r'TEST-[A-Z]+-\d{3}', row[5]))):
            errors.append('primary test mismatch: ' + row[0])
        for test in re.findall(r'TEST-[A-Z]+-\d{3}', row[5]):
            traced_tests.add(test)
            if test not in tests:
                errors.append('undefined trace test: ' + test)
    if traced_tests != set(tests):
        errors.append('test plan/trace coverage mismatch')
    screens = set(re.findall(r'^## (SCR-\d{2})\b',
                 (root / 'docs/02-ux/SCREEN_SPEC.md').read_text(), re.M))
    if screens != {f'SCR-{i:02}' for i in range(11)}:
        errors.append('screen definitions must include SCR-00 through SCR-10')
    for row in trace:
        if len(row) > 2:
            try:
                for screen in screen_ids(row[2]):
                    if screen not in screens:
                        errors.append('undefined screen: ' + screen)
            except ValueError as exc:
                errors.append(str(exc))
    # Check exact API route and entity references, allowing explicitly deferred P1.
    api_rows = table_rows((root / 'docs/03-architecture/API_CONTRACT.md').read_text())
    routes = {row[1] for row in api_rows if len(row) >= 2 and row[0] in
              ('GET','POST','PATCH','DELETE','PUT')}
    method_routes = {(row[0], row[1]) for row in api_rows if len(row) >= 2 and
                     row[0] in ('GET', 'POST', 'PATCH', 'DELETE', 'PUT')}
    try:
        contract = json.loads((root / 'docs/02-ux/screen-api-contracts.json').read_text())
        screen_routes = contract['screens']
        if contract.get('schema_version') != 1 or not isinstance(screen_routes, dict) or set(screen_routes) != screens:
            raise ValueError('all screen definitions required')
        for screen, entries in screen_routes.items():
            if not isinstance(entries, list) or not entries:
                raise ValueError('nonempty screen route list required')
            for entry in entries:
                if not isinstance(entry, dict) or set(entry) != {'method', 'path'}:
                    raise ValueError('method/path required')
                method, path = entry['method'], entry['path']
                if not isinstance(method, str) or not isinstance(path, str):
                    raise ValueError('method/path must be strings')
                if (method, path) not in method_routes:
                    errors.append(f'undefined screen API: {screen}: {method} {path}')
        required_screen_routes = {
            'SCR-00': {('POST','/auth/pairing'), ('GET','/auth/session'), ('GET','/auth/csrf')},
            'SCR-02': {('GET','/jobs')},
            'SCR-05': {('GET','/knowledge/candidates'), ('GET','/knowledge/candidates/{id}')},
            'SCR-09': {('GET','/settings'), ('GET','/consents'), ('GET','/auth/sessions'),
                       ('DELETE','/auth/sessions/{id}'), ('POST','/auth/session/refresh'),
                       ('DELETE','/auth/session')},
        }
        for screen, required_routes in required_screen_routes.items():
            actual = {(x['method'],x['path']) for x in screen_routes.get(screen, [])}
            if not required_routes.issubset(actual):
                errors.append('missing mandatory screen API: ' + screen)
        if 'REQ-SEC-001' not in reqs or 'TEST-SEC-001' not in primary_tests.get('REQ-SEC-001', set()):
            errors.append('authentication requirement/acceptance missing')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('invalid screen API contracts: ' + str(exc))
    entities = set()
    for row in table_rows((root / 'docs/03-architecture/DATA_MODEL.md').read_text()):
        if len(row) >= 3 and re.fullmatch(r'[a-z_]+(?: / [a-z_]+)*', row[0]):
            entities.update(row[0].split(' / '))
    for row in trace:
        if len(row) != 8:
            continue
        if not row[3].startswith('P1'):
            for route in row[3].split(','):
                if route.strip() not in routes:
                    errors.append('undefined API route: ' + route.strip())
        if not row[4].startswith('P1'):
            for entity in row[4].split(','):
                if entity.strip() not in entities:
                    errors.append('undefined entity: ' + entity.strip())
    errors.extend(validate_release_state(root))
    # Runtime plans are records of future work, not executed application tests.
    try:
        register = json.loads((root / 'docs/06-quality/verification-register.json').read_text())
        items = register['items']
        if not isinstance(items, list) or {x['test_id'] for x in items} != set(tests) or len(items) != len(tests):
            errors.append('runtime register/test plan mismatch')
        if type(register.get('application_implementation_authorized')) is not bool:
            errors.append('runtime register authorization must be boolean')
        for item in items:
            expected_reqs = {row[0] for row in trace if len(row) == 8 and item.get("test_id") in re.findall(r"TEST-[A-Z]+-\d{3}", row[5])}
            if not expected_reqs or set(item.get("requirement_ids", [])) != expected_reqs:
                errors.append("runtime register requirement mismatch: " + str(item.get("test_id")))
            if item.get('timing') != 'post_implementation' or item.get('status') not in ('not_run','running','passed','failed','inconclusive'):
                errors.append('invalid runtime status: ' + str(item.get('test_id')))
            for key in ('owner_role','expected','prerequisites','evidence_required','design_return_paths','on_failure'):
                if not item.get(key):
                    errors.append('incomplete runtime plan: ' + key)
            for path in item.get('design_return_paths', []):
                target = (root / path).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    errors.append('invalid design return path: ' + path)
            if item.get('status') == 'not_run':
                if any(item.get(k) is not None for k in ('actual_result','executed_by','executed_at')) or item.get('evidence_refs') or item.get('attempts'):
                    errors.append('not_run contains execution claims: ' + item['test_id'])
            else:
                if register.get('application_implementation_authorized') is not True:
                    errors.append('runtime execution without implementation authorization')
                if not all(item.get(k) for k in ('actual_result','executed_by','executed_at','evidence_refs','attempts')):
                    errors.append('runtime result lacks evidence: ' + item['test_id'])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('invalid runtime register: ' + str(exc))
    # Only Markdown links are executable references. Historical inline file:line
    # evidence intentionally remains anchored to the old reviewed commit.
    for doc in root.rglob('*.md'):
        if any(part.startswith('.') for part in doc.relative_to(root).parts):
            continue
        text = re.sub(r'```.*?```', '', doc.read_text(), flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = unquote(target.split('#', 1)[0].strip('<>'))
            if not target or re.match(r'^[a-zA-Z][\w+.-]*:', target):
                continue
            path = (doc.parent / target).resolve()
            if not path.is_relative_to(root) or not path.exists():
                errors.append(f'broken local link: {doc.relative_to(root)} -> {target}')
    return errors, {'requirements': len(reqs), 'test_plans': len(tests),
                    'screens': len(screens)}

if __name__ == '__main__':
    errors, counts = validate(ROOT)
    for error in errors:
        print('FAIL:', error)
    if not errors:
        print('PASS: design structure', counts)
        print('LIMIT: no runtime, UX, safety, reviewer identity or human acceptance verified')
    sys.exit(bool(errors))
