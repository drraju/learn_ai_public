"""Deterministic token-count vectors for teaching; not semantic embeddings."""
import math,re

def embed(text):
    counts=[0.0]*8
    for token in re.findall(r'[a-z0-9]+',text.lower()):
        counts[sum(token.encode())%8]+=1
    norm=math.sqrt(sum(x*x for x in counts))
    return [x/norm for x in counts] if norm else counts

def cosine(a,b):
    if len(a)!=len(b) or not a: raise ValueError('dimension mismatch')
    left=math.sqrt(sum(x*x for x in a))
    right=math.sqrt(sum(x*x for x in b))
    return sum(x*y for x,y in zip(a,b))/(left*right) if left and right else 0.0
