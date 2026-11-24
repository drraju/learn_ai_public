"""Deterministic capstone task and tenant-scope evaluation."""
from pathlib import Path
import json
from projects.p03_tool_agent.app import Agent

def evaluate():
    cases=json.loads((Path(__file__).resolve().parents[2]/'assessments/cases/p06_investigation.json').read_text())
    agent=Agent()
    rows=[]
    for case in cases:
        result=agent.investigate(case['tenant'],case['question'],[{'tool':'search','query':case['question']}])
        citations=result.get('result',{}).get('citations',[])
        passed=result['status']==case['expected'] and ((case['citation'] in citations) if case['citation'] else not citations)
        rows.append({'question':case['question'],'tenant':case['tenant'],'passed':passed})
    return {'passed':sum(row['passed'] for row in rows),'total':len(rows),'cases':rows}

if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
