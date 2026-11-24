"""Optional OpenAI Responses adapter; no request without explicit live opt-in."""
import os

class OpenAIGenerator:
    def __init__(self,model=None):
        self.model=model or os.environ.get('OPENAI_MODEL')
    def generate(self,issue):
        if os.environ.get('ALLOW_LIVE_MODEL')!='1' or not self.model:
            raise RuntimeError('live model opt-in and OPENAI_MODEL required')
        from openai import OpenAI
        response=OpenAI(timeout=15,max_retries=0).responses.create(
            model=self.model,
            input=('Return only JSON with issue_id, summary, uncertainty, sources. '
                   'Use sources as an array containing the issue ID only. Do not infer cause. '
                   f'Issue: {issue!r}'))
        return response.output_text
