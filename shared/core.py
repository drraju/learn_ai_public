"""Small provider-neutral contracts for synthetic teaching data."""
from dataclasses import dataclass
from pathlib import Path
import json

FIXTURES = Path(__file__).parent / 'fixtures'

@dataclass(frozen=True)
class Issue:
    id: str
    tenant: str
    title: str
    description: str

@dataclass(frozen=True)
class Passage:
    id: str
    tenant: str
    version: int
    text: str

def load(name):
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))

def issue_from(raw):
    if not isinstance(raw, dict):
        raise ValueError('issue must be an object')
    values = [raw.get(k) for k in ('id','tenant','title','description')]
    if any(not isinstance(x,str) or not x.strip() or len(x)>2000 for x in values):
        raise ValueError('invalid issue fields')
    return Issue(*values)
