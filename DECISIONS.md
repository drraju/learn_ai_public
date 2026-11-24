# Architecture decisions — Stage 3

These decisions set the direction for Stage 4. Revisit a decision when evidence changes; record the new decision and its migration impact instead of silently rewriting history.

| ID | Decision | Reason | Alternative considered | Revisit when |
|---|---|---|---|---|
| ADR-001 | Keep a fresh Git history and migrate screened files individually | Source history and archives are outside the public-content boundary | Clone full source history | Rights and privacy review proves a specific history segment safe and useful |
| ADR-002 | Require an offline fixture path for every core concept | Learners may lack subscriptions, API credits or hardware | Require one live provider | A concept cannot be represented faithfully offline; document a genuine exception |
| ADR-003 | Separate modules from provider implementations | SDK changes should not force conceptual rewrites | Embed SDK code in each lesson | A small exception reduces complexity without coupling the lesson |
| ADR-004 | Use plain Python and SQLite before orchestration frameworks or extra stores | Controls and failure paths stay visible to beginners | Start with a graph framework and vector database | Evaluation shows the simpler baseline cannot meet a project requirement |
| ADR-005 | Treat model output and retrieved/tool content as untrusted | Application policy must enforce permissions and approvals | Rely on prompts or provider guardrails | Never for authorization; adjust validation method as threats evolve |
| ADR-006 | Keep experimental standards and distributed systems outside prerequisites | Maintenance burden and access needs are high | Teach every emerging technology as core | Reproducible learning benefit, stable implementation and owner are demonstrated |

See [ARCHITECTURE.md](ARCHITECTURE.md) for the target layout and [TECHNOLOGY_REGISTER.md](TECHNOLOGY_REGISTER.md) for technology-specific status.

## ADR-005 — Importable project directory names (25 November 2026)

Use underscores for Python project package names while keeping hyphens in lesson directory names. This enables stable `python -m` commands on all supported shells. Update architecture and contributor examples accordingly.
