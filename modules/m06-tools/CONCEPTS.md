# Concept guide

A tool call has two phases: a model or deterministic selector proposes an action, then host code decides whether to execute it. Tool names, argument schemas, tenant scope and step budgets belong to the host. A prompt asking the model to “be careful” cannot replace these checks. Read-only lookup and write-capable effects should have different policies.

P3 accepts only a `search` proposal with one bounded string argument. Its loop stops when evidence is found, when no evidence remains, when a proposal is denied or when the step budget is exhausted. A real model proposal adapter may be added, but it should feed the same policy function. Store a trace of tool choice and citations without recording secrets or whole private documents.

**Decision to defend:** Show an unknown tool proposal and explain why it is denied before dispatch, even if its text claims urgency.
