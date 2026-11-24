# Local operations runbook

From the repository root, set `LEARN_AI_DEMO_TOKEN` to a disposable value of at least 12 characters, then run `python -m projects.p06_capstone.app`. In another terminal with the same token, run `python -m projects.p06_capstone.client`. The service binds the token to the fixed `demo` tenant and listens only on `127.0.0.1:8765`; `GET /health` returns `{"status":"ok"}`. Stop with Control-C. If port 8765 is occupied, stop the other process; this demo has no port configuration. If responses are unauthorized, verify the token matches. For malformed requests, inspect the JSON shape without logging token values. Rollback means stop this local process and return to the last reviewed revision; no deployment automation or data migration exists. Do not use real tenant data.

POSIX example: `export LEARN_AI_DEMO_TOKEN=local-demo-12345`. PowerShell: `$env:LEARN_AI_DEMO_TOKEN='local-demo-12345'`. These values are demonstrations only.
