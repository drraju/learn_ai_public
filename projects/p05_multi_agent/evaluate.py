"""Case-matched offline comparison with measured wall time and role steps."""
import json
import statistics
from pathlib import Path
from time import perf_counter
from projects.p02_rag.app import demo_store
from projects.p05_multi_agent.app import baseline, workflow

CASES = Path(__file__).resolve().parents[2] / 'assessments/cases/p02_retrieval.json'


def evaluate(repeats=30):
    if repeats < 1:
        raise ValueError('repeats must be positive')
    cases = json.loads(CASES.read_text(encoding='utf-8')) + [
        {'tenant': 'demo', 'question': 'no matching procedure', 'expected': None}]
    store = demo_store()
    rows = []
    for case in cases:
        question, tenant, expected = case['question'], case['tenant'], case['expected']
        times = {'baseline': [], 'workflow': []}
        for _ in range(repeats):
            start = perf_counter()
            base = baseline(store, tenant, question)
            times['baseline'].append((perf_counter() - start) * 1000)
            start = perf_counter()
            multi = workflow(store, tenant, question)
            times['workflow'].append((perf_counter() - start) * 1000)
        base_ok = (expected in base['citations']) if expected else base['abstained']
        multi_ok = (multi['status'] == 'verified' and expected in multi['citations']) if expected else multi['status'] == 'abstained'
        rows.append({'question': question, 'baseline_pass': base_ok, 'workflow_pass': multi_ok,
                     'baseline_steps': 1, 'workflow_steps': 2 if expected else 1,
                     'baseline_median_ms': round(statistics.median(times['baseline']), 4),
                     'workflow_median_ms': round(statistics.median(times['workflow']), 4)})
    return {'cases': len(rows), 'repeats_per_case': repeats, 'rows': rows,
            'baseline_passed': sum(row['baseline_pass'] for row in rows),
            'workflow_passed': sum(row['workflow_pass'] for row in rows),
            'api_cost': 0,
            'limit': 'Small local deterministic case set; timing is machine-specific and excludes model/provider cost.'}


if __name__ == '__main__':
    report = evaluate()
    print(json.dumps(report, indent=2))
    raise SystemExit(report['baseline_passed'] != report['cases'] or report['workflow_passed'] != report['cases'])
