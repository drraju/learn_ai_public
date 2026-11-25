# Local operations runbook

From the repository root, set `LEARN_AI_DEMO_TOKEN` to a disposable value of at least 12 characters, then run `python -m projects.p06_capstone.app`. In another terminal with the same token, run `python -m projects.p06_capstone.client`. The service binds the token to the fixed `demo` tenant and listens only on `127.0.0.1:8765`. `GET /health` returns `{"status":"ok"}`. Stop with Control-C. If port 8765 is occupied, stop the other process; this demo has no port configuration. For unauthorized responses, verify the token matches without printing it.

POSIX example: `export LEARN_AI_DEMO_TOKEN=local-demo-12345`. PowerShell: `$env:LEARN_AI_DEMO_TOKEN='local-demo-12345'`. These values are demonstrations only. Do not use real tenant data.

## Request state and metrics

The service uses ignored `generated/p6_state.db` by default. Set `LEARN_AI_STATE_DB` to another local path if needed. The client sends a fresh `X-Request-ID`; a matching retry returns the prior result, while reusing that ID for different input returns 409. The ledger stores tenant, request ID, a SHA-256 question hash, result, elapsed time and creation time, not raw question or token. A hash of a low-entropy question is not anonymous, so keep this service on synthetic data.

`GET /metrics` requires the same demo bearer token and returns total/answered/no-evidence counts plus median local processing time. Run `python -m projects.p06_capstone.operations metrics` from the repository root to inspect the same ledger without HTTP. This is a teaching metric, not a service-level objective or provider latency benchmark.

## Retention and local rollback drill

1. Stop the service before changing or restoring its SQLite file. Copy `generated/p6_state.db` to an ignored backup path before a code or schema change.
2. Record the reviewed Git revision and run `python -m projects.p06_capstone.evaluate` plus the offline tests. Start the new revision and check `/health`, an authorized investigation, an unauthorized request and `/metrics`.
3. If the check fails, stop the service, restore the reviewed code revision and the saved SQLite file, restart, and repeat those checks. Do not overwrite a newer ledger without reviewing what records would be lost.
4. For the local retention exercise, run `python -m projects.p06_capstone.operations purge --days 7`, then `python -m projects.p06_capstone.operations metrics`. The purge is irreversible for the selected file; make a backup first. Choose a retention period for a real deployment only after policy review.

For malformed requests, inspect the JSON shape without logging token values. This local drill has no automated deployment rollback, identity provider, durable approval for a real effect, TLS boundary or production monitoring. Do not expose the reference service publicly.
