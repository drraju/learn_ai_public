# Concept guide

Freeze a small labelled case set before changing prompts, models or retrieval. Separate task success, retrieval recall, citation support and policy invariants. Always report the numerator, denominator, case versions and failure slices. A model grader can help triage ambiguous outputs, but it needs human calibration and cannot decide whether a forbidden tool was invoked.

Security evaluation includes malicious retrieved text, poisoned tool output, cross-tenant requests and approval replay. Run deterministic denial checks before scoring answer quality. Observability should capture a trace ID, stage, status, duration and chosen provider without exposing tokens or private content. Cost per successful task requires both usage and the number of successful cases; average token cost alone is misleading.

**Decision to defend:** Why can a high Recall@k coexist with unsupported answers? Show one case where the expected passage is retrieved but the answer still needs review.
