"""Bind review artifacts and sequencing metadata; no identity/authenticity claim."""
import hashlib
import json
import re
import sys
from pathlib import Path
from check_release_state import validate as validate_release_state

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('codex_review_recorded', 'codex_complete', 'claude_reviewing',
          'claude_complete', 'ready_for_design_approval')

def validate(root):
    root = Path(root).resolve()
    errors = []
    def artifact(name):
        if not isinstance(name, str) or not name:
            errors.append('artifact reference missing')
            return ''
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append('invalid artifact reference: ' + name)
            return ''
        try:
            return path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append('unreadable artifact: ' + str(exc))
            return ''
    def read_json(name):
        value = artifact(name)
        try:
            result = json.loads(value)
            if not isinstance(result, dict):
                raise ValueError('object required')
            return result
        except (ValueError, TypeError) as exc:
            errors.append('invalid JSON: ' + str(name) + ': ' + str(exc))
            return {}
    def sha40(value):
        return isinstance(value, str) and re.fullmatch('[0-9a-f]{40}', value)
    def sha256(value):
        return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value)
    state = read_json('reviews/review-state.json')
    required = {'schema_version','phase','reviewed_commit','review_artifact',
                'execution_artifact','remediation_artifact','remediation_status',
                'human_acceptance','human_acceptance_ref','claude_started',
                'claude_artifact','claude_execution_ref','claude_reviewed_commit',
                'implementation_authorized','design_approval','design_approval_ref'}
    if required != set(state):
        errors.append('state fields mismatch')
    if type(state.get('schema_version')) is not int or state['schema_version'] != 1:
        errors.append('unsupported schema version')
    phase = state.get('phase')
    if phase not in PHASES:
        errors.append('unknown phase')
    sha = state.get('reviewed_commit')
    if not sha40(sha):
        errors.append('invalid reviewed commit')
    report = artifact(state.get('review_artifact'))
    target_rows = re.findall(r'^\|\s*対象commit\s*\|\s*`([0-9a-f]{40})`\s*\|', report, re.M)
    if target_rows != [sha] or '## 3. 上位10課題' not in report:
        errors.append('active report target commit missing/mismatched')
    artifact(state.get('remediation_artifact'))
    execution = read_json(state.get('execution_artifact'))
    terminal = execution.get('terminal_event')
    if (execution.get('reviewed_commit') != sha or not execution.get('session_id') or
        type(execution.get('exit_code')) is not int or execution.get('exit_code') != 0 or
        not isinstance(terminal, dict) or terminal.get('type') != 'turn.completed'):
        errors.append('successful CLI evidence/commit missing')
    active = read_json('reviews/active-review.json')
    if active.get('schema_version') != 1 or type(active.get('active_round')) is not int:
        errors.append('invalid active review schema/round')
    if active.get('reviewed_commit') != sha or active.get('cli_session_id') != execution.get('session_id'):
        errors.append('active review commit/session mismatch')
    refs = active.get('artifacts')
    if not isinstance(refs, dict) or set(refs) != {'report','execution','raw_cli','source_manifest'}:
        errors.append('active artifact manifest incomplete')
        refs = {}
    texts = {}
    for key, record in refs.items():
        if not isinstance(record, dict):
            errors.append('invalid artifact metadata: ' + key)
            continue
        content = artifact(record.get('path'))
        texts[key] = content
        if not sha256(record.get('sha256')) or hashlib.sha256(content.encode('utf-8')).hexdigest() != record.get('sha256'):
            errors.append('active artifact digest mismatch: ' + key)
    for key, value in [('report',state.get('review_artifact')),
                       ('execution',state.get('execution_artifact')),
                       ('raw_cli',execution.get('raw_cli_report')),
                       ('source_manifest',execution.get('source_manifest'))]:
        if not isinstance(refs.get(key), dict) or refs[key].get('path') != value:
            errors.append('active artifact path mismatch: ' + key)
    if hashlib.sha256(report.encode('utf-8')).hexdigest() != execution.get('saved_report_sha256'):
        errors.append('execution/saved report digest mismatch')
    if hashlib.sha256(texts.get('raw_cli','').encode('utf-8')).hexdigest() != execution.get('cli_report_sha256'):
        errors.append('execution/raw CLI digest mismatch')
    for field, allowed in [('human_acceptance',('pending','accepted','rejected')),
                           ('remediation_status',('proposed','accepted','rejected')),
                           ('design_approval',('pending','accepted','rejected'))]:
        if state.get(field) not in allowed:
            errors.append('invalid ' + field)
    for field in ('claude_started','implementation_authorized'):
        if type(state.get(field)) is not bool:
            errors.append('boolean required: ' + field)
    if state.get('implementation_authorized') is not False:
        errors.append('DESIGN ONLY: implementation authorization cannot be enabled here')
    if phase == 'codex_review_recorded':
        if state.get('human_acceptance') == 'accepted' or state.get('claude_started') is not False:
            errors.append('recorded phase conflicts with acceptance/Claude start')
    elif phase in PHASES:
        if state.get('human_acceptance') != 'accepted':
            errors.append('phase requires human acceptance')
        artifact(state.get('human_acceptance_ref'))
    if phase == 'codex_complete' and state.get('claude_started') is not False:
        errors.append('Claude start requires claude_reviewing phase')
    claude_phase = phase in ('claude_reviewing','claude_complete','ready_for_design_approval')
    if claude_phase and state.get('claude_started') is not True:
        errors.append('Claude phase requires started=true')
    if state.get('claude_started') is False:
        if any(state.get(k) is not None for k in ('claude_artifact','claude_execution_ref','claude_reviewed_commit')):
            errors.append('Claude evidence present but start is false')
    if state.get('claude_started') is True:
        if not claude_phase:
            errors.append('Claude started outside Claude phase')
        if state.get('human_acceptance') != 'accepted':
            errors.append('Claude requires accepted primary review')
        if state.get('claude_reviewed_commit') != sha or not sha40(state.get('claude_reviewed_commit')):
            errors.append('Claude baseline mismatch')
        ce = read_json(state.get('claude_execution_ref'))
        expected_status = 'running' if phase == 'claude_reviewing' else 'completed'
        if (ce.get('reviewed_commit') != sha or ce.get('status') != expected_status or
            not ce.get('session_id') or ce.get('session_id') == execution.get('session_id')):
            errors.append('Claude execution metadata mismatch')
        if phase != 'claude_reviewing':
            cr = artifact(state.get('claude_artifact'))
            if hashlib.sha256(cr.encode('utf-8')).hexdigest() != ce.get('report_sha256'):
                errors.append('Claude report digest mismatch')
    if phase == 'ready_for_design_approval' and state.get('remediation_status') != 'accepted':
        errors.append('ready phase requires accepted remediation')
    if state.get('design_approval') == 'accepted':
        if phase != 'ready_for_design_approval':
            errors.append('design approval requires ready phase')
        artifact(state.get('design_approval_ref'))
    errors.extend(validate_release_state(root))
    return errors, {'phase':phase,'human_acceptance':state.get('human_acceptance'),
                    'design_approval':state.get('design_approval')}

def review_warnings(root):
    """Report source drift separately from historical review integrity."""
    root = Path(root).resolve()
    try:
        state = json.loads((root / 'reviews/review-state.json').read_text())
        active = json.loads((root / 'reviews/active-review.json').read_text())
        relative = active['artifacts']['source_manifest']['path']
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise ValueError('source manifest outside root')
        manifest = json.loads(target.read_text())
        changes = []
        for entry in manifest['tree']:
            if entry['type'] != 'blob':
                continue
            path = (root / entry['path']).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                changes.append(entry['path'])
                continue
            content = path.read_bytes()
            digest = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            if digest != entry['sha']:
                changes.append(entry['path'])
        known_paths = {entry['path'] for entry in manifest['tree'] if entry['type'] == 'blob'}
        new_paths = []
        for folder in ('docs', 'scripts', 'handoff', 'wireframes', '.github'):
            for path in (root / folder).rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                    relative_path = path.relative_to(root).as_posix()
                    if relative_path not in known_paths:
                        new_paths.append(relative_path)
        if changes or new_paths:
            return [f"REVIEW_SOURCE_DRIFT: historical reviewed commit {state['reviewed_commit']}; "
                    f"{len(changes)} reviewed files differ/missing; {len(new_paths)} new source files. "
                    "Current source is not covered by this review; fresh review required before approval."]
        return []
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return ['REVIEW_SOURCE_UNVERIFIED: cannot compare source: ' + str(exc)]

if __name__ == '__main__':
    errors, summary = validate(ROOT)
    for error in errors:
        print('FAIL:', error)
    for warning in review_warnings(ROOT):
        print('WARN:', warning)
    if not errors:
        print('PASS: review metadata and artifact binding', summary)
        print('LIMIT: no identity, independence, approval authenticity or runtime safety verified')
    sys.exit(bool(errors))
