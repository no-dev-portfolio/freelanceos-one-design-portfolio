"""Cross-file DESIGN ONLY invariants; no approval authenticity claim."""
import json
from pathlib import Path


def validate(root):
    root = Path(root)
    errors = []
    records = {}
    paths = {
        'state': 'reviews/review-state.json',
        'register': 'docs/06-quality/verification-register.json',
        'design': 'docs/08-governance/DESIGN_STATUS.json',
    }
    for name, path in paths.items():
        try:
            value = json.loads((root / path).read_text())
            if not isinstance(value, dict):
                raise ValueError('object required')
            records[name] = value
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f'invalid release state: {name}: {exc}')
    if len(records) != len(paths):
        return errors
    state, register, design = (records[n] for n in ('state', 'register', 'design'))
    flags = [state.get('implementation_authorized'),
             register.get('application_implementation_authorized'),
             design.get('application_implementation_authorized')]
    if any(type(flag) is not bool for flag in flags):
        errors.append('release authorization flags must be boolean')
    elif len(set(flags)) != 1:
        errors.append('implementation authorization mismatch across state/register/design')
    if any(flag is not False for flag in flags):
        errors.append('DESIGN ONLY: all implementation authorizations must be false')
    acceptance = register.get('runtime_acceptance')
    if acceptance not in ('pending', 'accepted', 'rejected'):
        errors.append('invalid runtime acceptance')
    if design.get('runtime_acceptance') != acceptance:
        errors.append('runtime acceptance mismatch across register/design')
    items = register.get('items')
    if not isinstance(items, list) or not items or any(not isinstance(x, dict) for x in items):
        errors.append('invalid runtime acceptance test items')
        return errors
    if any(x.get('status') != 'not_run' for x in items) and not all(flag is True for flag in flags):
        errors.append('runtime execution without consistent implementation authorization')
    if acceptance == 'accepted':
        # Conservative global acceptance: no subset/waiver silently skips plans.
        # check_design additionally checks the exact test set and requirement links.
        if not all(flag is True for flag in flags):
            errors.append('runtime acceptance requires implementation authorization')
        if any(x.get('status') != 'passed' or
               not all(x.get(k) for k in ('actual_result', 'executed_by', 'executed_at',
                                        'evidence_refs', 'attempts')) for x in items):
            errors.append('runtime acceptance requires every plan passed with evidence')
        errors.append('DESIGN ONLY: runtime acceptance cannot be enabled here')
    # These scripts intentionally cannot transition to implementation/production.
    # A later authorized implementation change must introduce its approval schema.
    if any(flag is not False for flag in flags) or acceptance == 'accepted':
        return errors
    for item in items:
        if item.get('status') != 'not_run':
            continue
        if any(item.get(k) is not None for k in ('actual_result', 'executed_by', 'executed_at')) or item.get('evidence_refs') or item.get('attempts'):
            errors.append('not_run contains execution claims: ' + str(item.get('test_id')))
    return errors
