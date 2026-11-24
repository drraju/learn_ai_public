# Stage 5 quality assurance report

Date: 25 November 2026. Scope: the local `learn_ai_public` working tree intended for eventual publication. **Gate result: not passed.** This report records checks and fixes; it does not authorize a release or a push.

## Checks completed

| Area | Evidence | Result |
|---|---|---|
| Repository separation | Original source checkout stayed clean; the public checkout remains a separate local `main` with no remote, commit or push | Pass |
| Privacy and secrets | Scanned 127 candidate files before this report for personal/company identifiers, email addresses, home paths and common credential shapes; manually reviewed matches from a broader keyword search. No candidate hit remained after fixes. No symlinks, files over 1 MB or non-text candidate files. | Pass for scanned patterns; no scan proves absence of every secret |
| Source and syntax | Parsed 36 Python files; no syntax errors. Screened migrated examples and synthetic fixtures. | Pass for syntax; reuse rights still require final review |
| Local Markdown links | `python tools/check_repo.py` resolved repository-relative links and validated module metadata. No local anchor links are used. | Pass |
| External references | Opened all 18 distinct documentation URLs in the draft, including official Python, SQLite, provider, protocol, framework and GitHub Actions pages. | Pass for reachability on review date; links can later change |
| YAML | Parsed the workflow and three issue templates with Ruby's YAML parser. | Syntax pass; GitHub-hosted execution unverified |
| Python compatibility | On macOS, the project suite ran 15 tests on Python 3.11.17 and 3.13.14 (one optional MCP skip in each). With Python 3.12.12 and MCP SDK 2.3.0, all 15 passed, including the in-process exchange. | Pass for these local environments |
| Migrated labs | M00's 14 tests passed on macOS Python 3.11.17 and 3.13.14 with loopback access. The 10 retained P3 seed tests passed on Python 3.11.17. The M00 CLI produced three records and two `.txt` results; M01's three demonstrations ran. | Pass on macOS |
| Project execution | P1, P2, P3 and P5 entry points ran; P6's frozen cases passed 3/3. P6 service and client succeeded as separate loopback processes. The P6 HTTP suite now tests unauthorized, cross-tenant and oversized requests. | Pass for the reference paths |
| Provider claims | OpenAI Responses, Ollama chat/embed and MCP interfaces were compared with official documentation. OpenAI/Ollama request shapes have mocked tests; MCP SDK exchange has an in-process test. | Documentation and mock checks pass; live model compatibility unverified |
| Original project | Rechecked source checkout status after changes to the public staging tree. | Clean |

The sandbox initially denied loopback sockets during an ordinary test invocation; the same socket tests passed when run with local loopback permission. The denial was an execution-environment limit, not a code failure. Docker is installed but its daemon was unavailable, so no Linux container run was possible. The GitHub workflow has not run because the repository remains local and unpublished.

## Findings fixed during Stage 5

1. Replaced the public migration document's detailed private course timeline and source-path inventory with a public provenance summary and exclusion policy.
2. Rebranded a migrated sample text file that still used the old project name.
3. Bound the capstone's demo token to its fixed `demo` tenant and added an HTTP test requiring 403 for a cross-tenant request. This is still a teaching token, not real user authentication.
4. Corrected P6's README so evaluation runs before the service, whose token setup is in its runbook.
5. Expanded local verification records to include the tested Python versions, refreshed provider documentation dates, and updated the GitHub Actions workflow to current documented v7 actions with read-only repository permission. CI now includes the migrated seed, capstone evaluation and a separate pinned MCP job.
6. Removed generated lab output from the staging tree. Such output embeds machine-specific absolute paths and is excluded by `.gitignore`.

## Open release blockers

| Priority | Finding | Required evidence before passing this gate |
|---|---|---|
| High | Windows and Linux execution is unverified. The configured CI matrix has not run; the local Docker daemon was unavailable. | Successful hosted or local runs on both operating systems, with failures repaired and results recorded. |
| High | P1–P6 do not yet meet every target in [project progression](PROJECT_PROGRESSION.md). P1 lacks the planned ten-case quality set and semantic support checks; P2 has an extractive lexical baseline rather than evaluated generated RAG; P3 approval is in memory; P4 lacks remote/version-mismatch tests; P5 lacks measured comparative cost/latency; P6 lacks production identity, durable state, metrics, retention and rollback automation. | Implement or explicitly rescope each project gate, then rerun normal, negative and evaluation cases. Do not describe P6 as production-ready. |
| High | OpenAI and Ollama paths were not run against a selected live model/runtime. Mocked tests prove request/response handling only. | Exact model, SDK/runtime, OS, hardware, cost and observed result recorded in implementation manifests; refusal/timeout/unsupported cases exercised where feasible. |
| High | Reuse rights for migrated source code and the final licence have not been established. | Stage 6 rights and licence compatibility review of the final file set before public release. |
| Medium | Module pages and independent challenges have not been trialled with learners across platforms. The reference tests do not prove the learning assessments. | Independent walkthroughs of M00–M12 and P1–P6, recording ambiguous steps and fixing them. |

## Decision

Stage 5 produced a reproducible QA baseline and corrected the findings above. **Publication readiness is blocked by the open items.** Keep the repository local, with no remote or push. After the high-priority items are resolved, rerun the full Stage 5 gate and update this report before Stage 6 publication review.
