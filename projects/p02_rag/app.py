"""P2: versioned lexical retrieval with exact citation IDs and abstention."""
import re
from shared.core import Passage, load

def tokens(text):
    return set(re.findall(r'[a-z0-9]+',text.lower()))

class DocumentStore:
    def __init__(self): self.docs={}
    def upsert(self, raw):
        doc=Passage(**raw)
        if not doc.id or not doc.tenant or not doc.text or doc.version<1:
            raise ValueError('invalid passage')
        old=self.docs.get((doc.tenant,doc.id))
        if old and doc.version<=old.version:
            raise ValueError('stale version')
        self.docs[(doc.tenant,doc.id)]=doc
    def delete(self, tenant, doc_id): self.docs.pop((tenant,doc_id),None)
    def search(self, tenant, query, k=2):
        if not tenant or not query.strip() or not 1<=k<=10: raise ValueError('invalid query')
        q=tokens(query)
        ranked=[(len(q & tokens(d.text+' '+d.id)),d) for d in self.docs.values() if d.tenant==tenant]
        return [d for score,d in sorted(ranked,key=lambda x:(-x[0],x[1].id)) if score>0][:k]

def demo_store():
    store=DocumentStore()
    for row in load('runbooks.json'): store.upsert(row)
    return store

def answer(store,tenant,question):
    hits=store.search(tenant,question)
    if not hits: return {'answer':'I do not have supporting evidence.','citations':[],'abstained':True}
    return {'answer':hits[0].text,'citations':[hits[0].id],'abstained':False}

def recall_at_k(store,cases,k=2):
    if not cases: raise ValueError('cases required')
    hits=sum(c['expected'] in [d.id for d in store.search(c['tenant'],c['question'],k)] for c in cases)
    return {'hits':hits,'total':len(cases),'recall':hits/len(cases)}

def vector_search(store,tenant,query,embedder,k=2):
    """Optional comparison path. A toy embedder is not semantic retrieval."""
    if not tenant or not query.strip() or not 1<=k<=10: raise ValueError('invalid query')
    from implementations.embeddings.fixture.provider import cosine
    query_vector=embedder(query)
    ranked=[]
    for doc in store.docs.values():
        if doc.tenant!=tenant: continue
        doc_vector=embedder(doc.text)
        ranked.append((cosine(query_vector,doc_vector),doc))
    return [doc for score,doc in sorted(ranked,key=lambda x:(-x[0],x[1].id)) if score>0][:k]

if __name__=='__main__':
    print(answer(demo_store(),'demo','login timeout'))
