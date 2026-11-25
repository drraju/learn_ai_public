"""Ten synthetic P1 cases; literal support is a conservative review signal."""
import json
from pathlib import Path
from shared.core import issue_from
from projects.p01_llm_app.app import summarize

CASES = Path(__file__).resolve().parents[2] / 'assessments/cases/p01_quality.json'

def evaluate(generator=None):
    cases = json.loads(CASES.read_text(encoding='utf-8'))
    rows = []
    for case in cases:
        raw = case['issue']
        try:
            out = summarize(raw, generator)
            required = case['required_term'].lower() in out['summary'].lower()
            source = out['sources'] == [raw['id']]
            # Exact source wording is strong evidence; paraphrases still need review.
            literal = out['summary'].lower() == (raw['title'] + ': ' + raw['description'][:120]).lower()
            rows.append({'id': raw['id'], 'valid': True, 'required_term': required,
                         'source_id': source, 'literal_support': literal,
                         'needs_human_support_review': not literal,
                         'passed_automatic_checks': required and source})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            rows.append({'id': raw['id'], 'valid': False, 'error': type(exc).__name__,
                         'passed_automatic_checks': False,
                         'needs_human_support_review': True})
    return {'passed': sum(r['passed_automatic_checks'] for r in rows),
            'total': len(rows), 'rows': rows,
            'note': 'Automatic checks do not establish semantic support; review every generated claim against the issue.'}

if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(report, indent=2))
    raise SystemExit(report['passed'] != report['total'])
