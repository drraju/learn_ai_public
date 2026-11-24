# Concept guide

Retrieval quality and answer quality are different questions. A lexical baseline matches query terms exactly and is useful for IDs or error codes; semantic embeddings may help paraphrases but can miss precise identifiers. Hybrid search and reranking add complexity and should be justified against a frozen case set. The toy vector adapter is intentionally not a semantic model.

P2 filters by tenant before scoring, returns passage IDs, and abstains when no passage scores above zero. Recall@k is the number of cases where the expected passage appears in the top k divided by the total labelled cases. It says nothing about whether the final answer faithfully uses that passage. Citation support must be checked against the exact retrieved version, and a citation alone is not proof of truth.

**Decision to defend:** Add a question containing an exact alert ID and compare lexical to vector retrieval. Report both numerator and denominator and identify a hard negative.
