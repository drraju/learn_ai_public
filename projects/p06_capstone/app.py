"""P6 local reference service. Its demo token is not production identity."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json,os,re,time
from projects.p06_capstone.operations import OperationsStore
from projects.p03_tool_agent.app import Agent

MAX_BODY=4096

def make_handler(agent,token,allowed_tenant='demo',operations=None):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/health':
                self.reply(200,{'status':'ok'});return
            if self.path=='/metrics' and operations is not None:
                if self.headers.get('Authorization')!='Bearer '+token:
                    self.reply(401,{'error':'unauthorized'});return
                self.reply(200,operations.metrics());return
            self.send_error(404)
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
                request_id=self.headers.get('X-Request-ID')
                if operations is not None:
                    if not request_id or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',request_id):
                        raise ValueError('request ID')
                    try:
                        previous=operations.existing(request_id,tenant,question)
                    except ValueError:
                        self.reply(409,{'error':'request ID conflict'});return
                    if previous is not None:
                        self.reply(200,previous);return
                started=time.perf_counter()
                out=agent.investigate(tenant,question,[{'tool':'search','query':question}])
                if operations is not None:
                    try:
                        out=operations.record(request_id,tenant,question,out,
                                              (time.perf_counter()-started)*1000)
                    except ValueError:
                        self.reply(409,{'error':'request ID conflict'});return
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
    operations=OperationsStore(os.environ.get('LEARN_AI_STATE_DB','generated/p6_state.db'))
    with ThreadingHTTPServer(('127.0.0.1',8765),make_handler(Agent(),token,operations=operations)) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
if __name__=='__main__': serve()
