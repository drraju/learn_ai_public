import json,os,urllib.request

def investigate(question,tenant='demo'):
    token=os.environ['LEARN_AI_DEMO_TOKEN']
    request=urllib.request.Request('http://127.0.0.1:8765/investigate',
        data=json.dumps({'tenant':tenant,'question':question}).encode(),
        headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
    with urllib.request.urlopen(request,timeout=3) as response:
        return json.load(response)
if __name__=='__main__': print(json.dumps(investigate('login timeout'),indent=2))
