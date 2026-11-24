# Concept guide

A local service makes an application boundary concrete: request size, authentication, error status, health and shutdown. P6 binds to loopback and uses a shared demo token. This is appropriate for teaching transport behavior, but the caller supplies the tenant and the service does not authenticate a person. It must not be exposed as a public service.

A production design needs real identity, tenant authorization, durable task and approval state, quotas, metrics, retention, TLS at the right boundary and a release/rollback procedure. A health response proves only that the process can answer a request; it does not prove retrieval correctness or provider availability. Rehearse failure and rollback using a documented release manifest and frozen evaluations before changing an external dependency.

**Decision to defend:** Which checks must pass before traffic is shifted to a new provider, and what observation triggers rollback?
