import json,os,sys,types,unittest
from unittest.mock import patch
from shared.core import issue_from,load
from implementations.generation.openai.provider import OpenAIGenerator
from implementations.generation.ollama.provider import OllamaGenerator
from implementations.embeddings.ollama.provider import embed as ollama_embed
from implementations.embeddings.fixture.provider import embed,cosine
from projects.p01_llm_app.app import configured_generator,FixtureGenerator
from projects.p02_rag.app import demo_store,vector_search

class FakeResponse:
 def __init__(self,payload):self.payload=payload
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def read(self):return json.dumps(self.payload).encode()

class AdapterTests(unittest.TestCase):
 def test_selection_and_output(self):
  with patch.dict(os.environ,{'LEARN_AI_PROVIDER':'fixture'}):
   self.assertIsInstance(configured_generator(),FixtureGenerator)
  with patch.dict(os.environ,{'LEARN_AI_PROVIDER':'unknown'}):
   with self.assertRaises(ValueError):configured_generator()
 def test_openai_request_shape_mocked(self):
  calls=[]
  class Responses:
   def create(self,**kw):
    calls.append(kw);return types.SimpleNamespace(output_text='{"issue_id":"INC-101"}')
  class Client:
   def __init__(self,**kw):self.responses=Responses()
  with patch.dict(sys.modules,{'openai':types.SimpleNamespace(OpenAI=Client)}),patch.dict(os.environ,{'ALLOW_LIVE_MODEL':'1'}):
   result=OpenAIGenerator('example-model').generate(issue_from(load('issues.json')[0]))
  self.assertEqual(json.loads(result)['issue_id'],'INC-101')
  self.assertEqual(calls[0]['model'],'example-model')
 def test_ollama_request_and_failure_mocked(self):
  captured=[]
  def fake(req,timeout):
   captured.append(json.loads(req.data));return FakeResponse({'message':{'content':'{"issue_id":"INC-101"}'}})
  with patch.dict(os.environ,{'ALLOW_LIVE_MODEL':'1'}),patch('urllib.request.urlopen',side_effect=fake):
   result=OllamaGenerator('example-model').generate(issue_from(load('issues.json')[0]))
  self.assertEqual(json.loads(result)['issue_id'],'INC-101')
  self.assertFalse(captured[0]['stream'])
 def test_ollama_embedding_shape_mocked(self):
  def fake(req,timeout):return FakeResponse({'embeddings':[[1.0,2.0]]})
  with patch.dict(os.environ,{'ALLOW_LIVE_MODEL':'1'}),patch('urllib.request.urlopen',side_effect=fake):
   self.assertEqual(ollama_embed('sample','example-model'),[1.0,2.0])
  with patch.dict(os.environ,{'ALLOW_LIVE_MODEL':'1'}),patch('urllib.request.urlopen',return_value=FakeResponse({'embeddings':[]})):
   with self.assertRaises(ValueError):ollama_embed('sample','example-model')
 def test_vector_scope_and_cosine(self):
  docs=vector_search(demo_store(),'demo','login',embed)
  self.assertTrue(all(d.tenant=='demo' for d in docs))
  self.assertAlmostEqual(cosine([2,0],[5,0]),1.0)

if __name__=='__main__':unittest.main()
