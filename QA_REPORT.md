# Stage 5 quality assurance report

Date: 25 November 2026. Scope: the `learn_ai_public` draft. **Stage 5 gate result: not passed.** This report records checks and fixes. The owner subsequently authorized publication of an unfinished public draft; that exception does not change the gate result or authorize a tagged release.

## Checks completed

| Area | Evidence | Result |
|---|---|---|
| Repository separation | Original source checkout stayed clean; the independent public checkout has separate history and its own `main` and remote | Pass |
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

The sandbox initially denied loopback sockets during an ordinary test invocation; the same socket tests passed when run with local loopback permission. The denial was an execution-environment limit, not a code failure. Docker is installed but its daemon was unavailable, so no Linux container run was possible. At the time of this local audit, the GitHub workflow had not run. Hosted CI results must be recorded separately after draft publication.

## Follow-up verification — 26 November 2026

[Hosted run 45645966986](https://github.com/drraju/learn_ai_public/actions/runs/45645966986) completed successfully for commit `7e9ff7d`: Ubuntu, macOS and Windows with Python 3.11 and 3.13, plus the pinned MCP job. This closed the original Windows/Linux execution blocker for that commit. [Hosted run 45662331048](https://github.com/drraju/learn_ai_public/actions/runs/45662331048) then completed successfully for follow-up commit `dd12af6`: all six Ubuntu/macOS/Windows Python 3.11/3.13 jobs and the pinned MCP job passed.

On the current follow-up tree, the project suite passed 25 tests on local Python 3.11 and 3.13, with two optional MCP skips in each. The pinned MCP SDK 2.3.0 environment passed three MCP tests, including a negotiated-version rejection. M00 passed 14 tests; the retained P3 seed passed 10; P1, P2, P5 and P6 offline evaluation commands completed. Local Markdown links, workflow YAML and `git diff --check` passed. A new identifier/credential/home-path scan found no matching candidate; no symlink or file over 1 MB was added outside Git. The P6 service/client, authenticated metrics and SQLite ledger command were exercised against loopback.

| Project | New evidence | Remaining limit |
|---|---|---|
| P1 | Ten synthetic cases, 10/10 fixture checks; conservative rejection of a newly invented causal phrase; local Llama 3.2 and Phi-4 trials | Manual review found unsupported or speculative generated claims; no general semantic-support guarantee |
| P2 | Four offline cited-answer/abstention cases; optional generated path validates scoped citation and exact evidence quote; local Phi-4 trial passed 4/4 with the two answer claims manually checked | Small case set; Llama 3.2 failed quality cases; no verified semantic embedding model |
| P3 | SQLite approval/effect ledger passed restart, expiry, replay and mismatch tests; provider-neutral proposal source uses the same host policy | Simulated effect only; no real approval identity or external write |
| P4 | In-process MCP exchange and negotiated protocol-version denial passed | Remote transport, authentication and independent server compatibility untested |
| P5 | Same three frozen cases for baseline and two-role workflow, 3/3 each; actual local median timing and role-step counts recorded | Tiny deterministic sample; no model-call cost comparison |
| P6 | Request replay/conflict, SQLite ledger, protected metrics and retention purge passed; local service run succeeded | Shared demo token, no real identity or durable approval for real effects, no automated deployment rollback or production monitoring |

Exact runtime/model identifiers and negative outcomes are in [live verification](LIVE_VERIFICATION.md). The adapted-content inventory and missing rights decision are in [rights review](RIGHTS_REVIEW.md).

## Findings fixed during Stage 5

1. Replaced the public migration document's detailed private course timeline and source-path inventory with a public provenance summary and exclusion policy.
2. Rebranded a migrated sample text file that still used the old project name.
3. Bound the capstone's demo token to its fixed `demo` tenant and added an HTTP test requiring 403 for a cross-tenant request. This is still a teaching token, not real user authentication.
4. Corrected P6's README so evaluation runs before the service, whose token setup is in its runbook.
5. Expanded local verification records to include the tested Python versions, refreshed provider documentation dates, and updated the GitHub Actions workflow to current documented v7 actions with read-only repository permission. CI now includes the migrated seed, capstone evaluation and a separate pinned MCP job.
6. Removed generated lab output from the staging tree. Such output embeds machine-specific absolute paths and is excluded by `.gitignore`.

## Open release blockers

| Priority | Finding | Evidence needed before passing the gate |
|---|---|---|
| High | Reuse rights for the adapted M00 lab, M01 demonstrations and P3 seed, and the final licence, are not confirmed. | Owner confirmation of authorship and any third-party terms; choose a compatible licence or replace uncertain material, then review the final public history. |
| High | P6 is still a local teaching service, not the production-grade target in [project progression](PROJECT_PROGRESSION.md). Its shared demo token is not user identity; request persistence is not approval for a real effect; release rollback is manual. | Authenticated identity and tenant authorization, durable approval around any real effect, operational monitoring, retention policy and a tested deployment/rollback procedure in a selected environment. |
| High | Generated quality is not yet reliable across chosen models and cases. P1 had unsupported/speculative claims; P2 Llama 3.2 failed supported-answer cases. | Larger held-out quality/attack sets, human support review, selected-model thresholds and repeated live runs; preserve model-specific failure labels. |
| Medium | Optional provider/integration breadth remains incomplete: OpenAI has no live check, Ollama embedding lacked a supported installed model, and P4 remote MCP is untested. | Check each chosen optional path with exact model/runtime/SDK and failure cases, or explicitly leave it unsupported. No optional provider should block the offline learning route. |
| Medium | P5 model-provider cost/latency comparison and independent learner trials of M00–M12/P1–P6 are absent. | Case-matched live model trials with cost/latency records where relevant, plus independent learner walkthroughs and fixes across platforms. |

## Decision

Stage 5 and the follow-up produced reproducible offline evidence and corrected several blockers. **Release readiness is still blocked by the open items.** The owner authorized an explicitly unfinished public draft despite this result. Do not describe it as production-ready, open-source licensed or a completed course. After the high-priority items are resolved, rerun the full Stage 5 gate and update this report before a tagged release review.
