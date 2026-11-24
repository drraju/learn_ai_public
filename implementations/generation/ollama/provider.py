"""Optional loopback-only Ollama chat adapter."""
import json,os,urllib.request

class OllamaGenerator:
    def __init__(self,model=None): self.model=model or os.environ.get('OLLAMA_MODEL')
    def generate(self,issue):
        if os.environ.get('ALLOW_LIVE_MODEL')!='1' or not self.model:
            raise RuntimeError('live model opt-in and OLLAMA_MODEL required')
        body=json.dumps({'model':self.model,'stream':False,'format':'json',
          'messages':[{'role':'user','content':'Return JSON with issue_id, summary, uncertainty, sources. Do not infer cause. Issue: '+repr(issue)}]}).encode()
        req=urllib.request.Request('http://127.0.0.1:11434/api/chat',body,{'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=15) as response: payload=json.load(response)
        return payload['message']['content']
