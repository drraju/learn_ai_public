"""P5: compare a single role with evidence and verification roles."""
from projects.p02_rag.app import answer, demo_store

def baseline(store,tenant,question): return answer(store,tenant,question)

def workflow(store,tenant,question,verifier=None):
    evidence=answer(store,tenant,question)
    if evidence['abstained']: return {'status':'abstained','citations':[],'roles':2}
    approved=(verifier or (lambda e: bool(e['citations']) and e['answer'] in [d.text for d in store.docs.values() if d.tenant==tenant]))(evidence)
    return {'status':'verified' if approved else 'disputed',
            'citations':evidence['citations'] if approved else [],'roles':2}

if __name__=='__main__': print(workflow(demo_store(),'demo','login timeout'))
