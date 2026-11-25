"""Case-level evaluation for extractive and optional generated RAG."""
import json
from pathlib import Path
from projects.p02_rag.app import answer, answer_with_generator, demo_store

CASES = Path(__file__).resolve().parents[2] / 'assessments/cases/p02_grounded.json'


def evaluate(generator=None):
    store = demo_store()
    rows = []
    for case in json.loads(CASES.read_text(encoding='utf-8')):
        try:
            if generator is None:
                out = answer(store, case['tenant'], case['question'])
            else:
                out = answer_with_generator(store, case['tenant'], case['question'], generator)
            expected = case['expected_citation']
            passed = (out['citations'] == [expected] and not out['abstained']) if expected else (out['abstained'] and not out['citations'])
            rows.append({'question': case['question'], 'tenant': case['tenant'],
                         'passed': passed, 'abstained': out['abstained'],
                         'citations': out['citations'],
                         'needs_human_answer_review': generator is not None and not out['abstained']})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            rows.append({'question': case['question'], 'tenant': case['tenant'],
                         'passed': False, 'error': type(exc).__name__,
                         'needs_human_answer_review': True})
    return {'passed': sum(row['passed'] for row in rows), 'total': len(rows),
            'rows': rows,
            'note': 'Citation and quote checks do not prove the answer is semantically supported.'}


if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(report, indent=2))
    raise SystemExit(report['passed'] != report['total'])
