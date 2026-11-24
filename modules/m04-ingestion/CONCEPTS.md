# Concept guide

Ingestion begins with permission to use the source. Assign a stable source ID, version, tenant, origin and deletion policy before indexing text. Parsing and chunking can lose boundaries or merge unrelated statements, so retain lineage from each searchable passage to the source version. Normalization should be repeatable: the same input and parser version should yield the same records.

P2 stores one current passage per tenant and ID. An upsert must advance the version; an older or equal version is rejected. Deletion removes the searchable record, not merely a UI label. A production system would also handle derived embeddings, caches, backups and retention. This small store makes the invalidation rule visible without requiring a vector database.

**Decision to defend:** Why does deleting a source record require checking every derived index? Demonstrate that the deleted passage cannot be found by the baseline search.
