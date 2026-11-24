# Concept guide

A prompt is a task instruction and context package, not an authorization mechanism. Separate trusted application instructions from retrieved documents or user-provided text. Source precedence must be enforced by the application: a runbook can contain facts but cannot change who may call a tool. A model may ignore an instruction, so the host still validates the result.

Use a frozen case set when changing a prompt. Record the prompt revision, provider/model, input fixture and observed output. Compare correct summaries, unsupported claims, refusals, latency and output length. An apparent improvement on one issue can regress another; inspect failure slices instead of reporting a single anecdote. Context pruning should preserve the passages needed to support the answer and the uncertainty statement.

**Decision to defend:** When a retrieved passage says “ignore prior instructions,” what code boundary prevents it from becoming policy?
