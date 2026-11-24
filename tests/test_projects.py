import json,unittest,threading,urllib.request,urllib.error
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch,MagicMock
from shared.core import load
from projects.p01_llm_app.app import summarize
from projects.p02_rag.app import demo_store,answer,recall_at_k
from projects.p03_tool_agent.app import Agent,Approval
from projects.p05_multi_agent.app import workflow
from projects.p06_capstone.app import make_handler
from implementations.embeddings.fixture.provider import embed,cosine
from implementations.generation.openai.provider import OpenAIGenerator
from implementations.generation.ollama.provider import OllamaGenerator
from implementations.embeddings.ollama.provider import embed as ollama_embed

class Tests(unittest.TestCase):
 def test_p1_valid_and_invalid(self):
  raw=load('issues.json')[0];self.assertEqual(summarize(raw)['sources'],['INC-101'])
  with self.assertRaises(ValueError): summarize({**raw,'title':''})
  class Bad:
   def generate(self,issue):return {'issue_id':issue.id,'summary':'invented','uncertainty':'none','sources':['outside']}
  with self.assertRaises(ValueError): summarize(raw,Bad())
 def test_p2_scope_version_and_deletion(self):
  store=demo_store();self.assertEqual(answer(store,'demo','login timeout')['citations'],['RB-LOGIN'])
  self.assertTrue(answer(store,'other','login timeout')['abstained'])
  with self.assertRaises(ValueError): store.upsert(load('runbooks.json')[0])
  store.delete('demo','RB-LOGIN');self.assertTrue(answer(store,'demo','login timeout')['abstained'])
 def test_p2_evaluation(self):
  cases=json.loads((Path(__file__).resolve().parents[1]/'assessments/cases/p02_retrieval.json').read_text())
  report=recall_at_k(demo_store(),cases);self.assertEqual(report['total'],2);self.assertEqual(report['hits'],2)
 def test_p3_policy_and_replay(self):
  agent=Agent(max_steps=1)
  good=agent.investigate('demo','login timeout',[{'tool':'search','query':'login timeout'}]);self.assertEqual(good['status'],'answered')
  self.assertEqual(agent.investigate('demo','x',[{'tool':'shell','query':'x'}])['status'],'denied')
  self.assertEqual(agent.investigate('demo','zzzz',[{'tool':'search','query':'zzzz'},{'tool':'search','query':'login'}])['status'],'limit')
  approval=Approval('demo','acknowledge_alert','A-17','key1')
  self.assertEqual(agent.simulate_action('demo','acknowledge_alert','A-17','key1',approval)['status'],'applied')
  self.assertEqual(agent.simulate_action('demo','acknowledge_alert','A-17','key1',approval)['status'],'already_applied')
  with self.assertRaises(PermissionError):agent.simulate_action('other','acknowledge_alert','A-17','key2',approval)
  with self.assertRaises(PermissionError):agent.simulate_action('demo','acknowledge_alert','A-18','key1',Approval('demo','acknowledge_alert','A-18','key1'))
 def test_p5_verification(self):
  self.assertEqual(workflow(demo_store(),'demo','login timeout')['status'],'verified')
  self.assertEqual(workflow(demo_store(),'demo','login timeout',lambda _:False)['status'],'disputed')
 def test_p6_handler_contract(self):
  server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(Agent(),'test-secret-123'))
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  root=f'http://127.0.0.1:{server.server_port}'
  try:
   with urllib.request.urlopen(root+'/health',timeout=2) as response:
    self.assertEqual(json.load(response),{'status':'ok'})
   body=json.dumps({'tenant':'demo','question':'login timeout'}).encode()
   request=urllib.request.Request(root+'/investigate',body,{'Authorization':'Bearer test-secret-123'})
   with urllib.request.urlopen(request,timeout=2) as response:
    self.assertEqual(json.load(response)['status'],'answered')
   with self.assertRaises(urllib.error.HTTPError) as denied:
    urllib.request.urlopen(urllib.request.Request(root+'/investigate',body),timeout=2)
   self.assertEqual(denied.exception.code,401)
   other=json.dumps({'tenant':'other','question':'login timeout'}).encode()
   cross=urllib.request.Request(root+'/investigate',other,{'Authorization':'Bearer test-secret-123'})
   with self.assertRaises(urllib.error.HTTPError) as forbidden:
    urllib.request.urlopen(cross,timeout=2)
   self.assertEqual(forbidden.exception.code,403)
   oversized=urllib.request.Request(root+'/investigate',b'x'*4097,{'Authorization':'Bearer test-secret-123'})
   with self.assertRaises(urllib.error.HTTPError) as bad:
    urllib.request.urlopen(oversized,timeout=2)
   self.assertEqual(bad.exception.code,400)
  finally:
   server.shutdown();server.server_close();thread.join(timeout=2)
 def test_fixture_vector(self):
  self.assertAlmostEqual(cosine(embed('hello'),embed('hello')),1.0)
  with self.assertRaises(ValueError):cosine([1],[1,2])
 def test_live_opt_in(self):
  raw=load('issues.json')[0]
  with patch.dict('os.environ',{},clear=True):
   with self.assertRaises(RuntimeError):OpenAIGenerator('sample').generate(raw)
   with self.assertRaises(RuntimeError):OllamaGenerator('sample').generate(raw)
   with self.assertRaises(RuntimeError):ollama_embed('hello','sample')

if __name__=='__main__':unittest.main()
