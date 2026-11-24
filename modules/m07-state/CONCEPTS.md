# Concept guide

A model context is not durable task state. A task needs an explicit status, input version, observations, pending action and checkpoint if it may pause or resume. Memory must have a scope and retention rule; otherwise a previous tenant’s facts can contaminate a new task. A human approval should name the exact action, target, tenant and expiry or nonce, then be consumed once.

P3 uses an in-memory `Approval` record and idempotency key to teach matching and replay behavior. Anyone who can construct that record can “approve” in the demo; it is not a real authentication system. In a deployable design, an authenticated approval service would persist the decision, bind it to an immutable action digest, enforce expiry and record an audit trail. The effect executor must recheck policy at execution time.

**Decision to defend:** Why does an idempotency key need to be bound to the action payload, rather than merely remembered as a string?
