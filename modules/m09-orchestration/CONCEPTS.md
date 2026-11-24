# Concept guide

Multiple roles can improve separation of concerns, but they add handoffs, latency and failure modes. Start with a single-role baseline on frozen cases. Add a second role only when it can detect an error or perform a distinct task that the baseline misses. Shared context should be explicit, minimal and versioned; one role’s text cannot authorize another role’s tools.

P5 has evidence and verification roles in a deterministic workflow. The verifier checks whether the answer matches a scoped passage; a forced disagreement yields a disputed result. This is not two independent LLMs or a distributed system. Compare case success and step count against the one-role baseline. A graph framework or A2A protocol becomes relevant only after a concrete coordination need is demonstrated.

**Decision to defend:** When the two-role workflow matches the baseline but uses more steps, what evidence would justify keeping it?
