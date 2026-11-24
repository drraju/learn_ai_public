"""P1: validated summary contract. Model output remains untrusted."""
import json
import os
from shared.core import issue_from
from implementations.generation.fixture.provider import FixtureGenerator

def summarize(raw, generator=None):
    issue=issue_from(raw)
    result=(generator or FixtureGenerator()).generate(issue)
    if isinstance(result,str):
        result=json.loads(result)
    if not isinstance(result,dict) or result.get('issue_id')!=issue.id:
        raise ValueError('invalid output identity')
    summary=result.get('summary'); uncertainty=result.get('uncertainty'); sources=result.get('sources')
    if not isinstance(summary,str) or not summary.strip() or len(summary)>500:
        raise ValueError('invalid summary')
    if not isinstance(uncertainty,str) or not uncertainty.strip() or len(uncertainty)>200:
        raise ValueError('invalid uncertainty')
    if sources!=[issue.id]:
        raise ValueError('unsupported source')
    return result

def configured_generator():
    provider=os.environ.get('LEARN_AI_PROVIDER','fixture')
    if provider=='fixture': return FixtureGenerator()
    if provider=='openai':
        from implementations.generation.openai.provider import OpenAIGenerator
        return OpenAIGenerator()
    if provider=='ollama':
        from implementations.generation.ollama.provider import OllamaGenerator
        return OllamaGenerator()
    raise ValueError('unsupported provider')

if __name__=='__main__':
    from shared.core import load
    print(json.dumps(summarize(load('issues.json')[0],configured_generator()),indent=2))
