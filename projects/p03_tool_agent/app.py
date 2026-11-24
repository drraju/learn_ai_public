"""P3: bounded deterministic tool proposals and exact simulated approval."""
from dataclasses import dataclass
from projects.p02_rag.app import answer, demo_store

@dataclass(frozen=True)
class Approval:
    tenant: str
    action: str
    target: str
    key: str

class Agent:
    def __init__(self,store=None,max_steps=3):
        self.store=store or demo_store();self.max_steps=max_steps;self.effects={}
    def investigate(self,tenant,question,proposals):
        if not tenant or not question: raise ValueError('identity and question required')
        trace=[]
        for step,proposal in enumerate(proposals):
            if step>=self.max_steps: return {'status':'limit','trace':trace}
            if not isinstance(proposal,dict) or proposal.get('tool')!='search' or set(proposal)!={'tool','query'}:
                return {'status':'denied','trace':trace}
            query=proposal['query']
            if not isinstance(query,str) or not query.strip() or len(query)>200:
                return {'status':'denied','trace':trace}
            response=answer(self.store,tenant,query)
            trace.append({'tool':'search','citations':response['citations']})
            if not response['abstained']:
                return {'status':'answered','result':response,'trace':trace}
        return {'status':'no_evidence','trace':trace}
    def simulate_action(self,tenant,action,target,key,approval):
        if action!='acknowledge_alert' or not target.startswith('A-') or not key:
            raise PermissionError('action denied')
        expected=Approval(tenant,action,target,key)
        if approval!=expected: raise PermissionError('approval mismatch')
        prior=self.effects.get(key)
        if prior and prior!=expected: raise PermissionError('idempotency key reused')
        self.effects[key]=expected
        return {'status':'already_applied' if prior else 'applied','target':target}

if __name__=='__main__':
    print(Agent().investigate('demo','login timeout',[{'tool':'search','query':'login timeout'}]))
