# Concept guide

A reproducible AI application still starts as ordinary software. Separate input parsing, validation, deterministic logic, storage and output. A test should show both the expected path and the path where a file, network call or database update fails. The catalogue lab uses a transaction so a failed refresh does not erase its previous snapshot. That property matters more than the choice of model.

A Python virtual environment isolates optional dependencies, while a lock or recorded version makes a result reproducible. Keep fixtures small and invented. Never write generated output into the input directory; otherwise a later scan can accidentally ingest its own artifacts. A local HTTP server makes request/response boundaries visible, but loopback access is still a network operation and may be blocked by a sandbox.

**Decision to defend:** Why does a database transaction protect the index but not make a CSV export and database update one atomic operation? Run the failure test and explain the remaining recovery step.
