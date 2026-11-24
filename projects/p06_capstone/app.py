"""P6 local reference service. Its demo token is not production identity."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json,os
from projects.p03_tool_agent.app import Agent

MAX_BODY=4096

def make_handler(agent,token,allowed_tenant='demo'):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path!='/health': self.send_error(404);return
            self.reply(200,{'status':'ok'})
        def do_POST(self):
            if self.path!='/investigate': self.send_error(404);return
            if self.headers.get('Authorization')!='Bearer '+token:
                self.reply(401,{'error':'unauthorized'});return
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=MAX_BODY: raise ValueError('body size')
                raw=json.loads(self.rfile.read(size))
                if not isinstance(raw,dict) or set(raw)!={'tenant','question'}: raise ValueError('fields')
                tenant=raw['tenant']; question=raw['question']
                if not isinstance(tenant,str) or not isinstance(question,str) or len(question)>200: raise ValueError('fields')
                if tenant!=allowed_tenant:
                    self.reply(403,{'error':'tenant denied'});return
                out=agent.investigate(tenant,question,[{'tool':'search','query':question}])
                self.reply(200,out)
            except (ValueError,TypeError,json.JSONDecodeError): self.reply(400,{'error':'invalid request'})
        def reply(self,status,obj):
            data=json.dumps(obj).encode()
            self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        def log_message(self,*args): pass
    return Handler

def serve():
    token=os.environ.get('LEARN_AI_DEMO_TOKEN')
    if not token or len(token)<12: raise ValueError('set LEARN_AI_DEMO_TOKEN (at least 12 characters)')
    with ThreadingHTTPServer(('127.0.0.1',8765),make_handler(Agent(),token)) as server:
        server.serve_forever()
if __name__=='__main__': serve()
