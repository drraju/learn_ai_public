"""Optional loopback-only Ollama embedding adapter."""
import json,os,urllib.request

def embed(text,model=None):
    chosen=model or os.environ.get('OLLAMA_EMBED_MODEL')
    if os.environ.get('ALLOW_LIVE_MODEL')!='1' or not chosen: raise RuntimeError('opt in and choose model')
    req=urllib.request.Request('http://127.0.0.1:11434/api/embed',
       json.dumps({'model':chosen,'input':text,'truncate':False}).encode(),
       {'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=15) as response: payload=json.load(response)
    vectors=payload.get('embeddings')
    if not isinstance(vectors,list) or len(vectors)!=1 or not isinstance(vectors[0],list) or not vectors[0]:
        raise ValueError('invalid embedding response')
    return vectors[0]
