# Learning paths — Stage 2 proposal

All paths use the same module gates in [CURRICULUM.md](CURRICULUM.md). Hours are estimates; the learner progresses by evidence. Required software begins with Python 3.11+ and Git. A terminal and ordinary laptop are sufficient for offline work. A GPU, paid subscription, API key, container runtime and cloud account are optional.

| Path | Start | Core sequence | Portfolio target |
|---|---|---|---|
| Beginner | No professional AI experience | M00 → M01 → M02 → M03 → M04 → M05 → M06, then M07–M12 | P1–P3 first, then P4–P6 |
| Software developer | Can pass M00 diagnostic | M01–M12; revisit M00 gaps | P1–P6 |
| AI engineer | Can pass M00–M05 diagnostics | M06–M12; re-evaluate P1/P2 on frozen cases | P3–P6 plus comparative evaluation |
| Architect or technical lead | Demonstrates technical gates with working code | M02, M05–M12, including security and operations | P6 architecture, risk, and operation defense |
| Local-first | Any entry level | Same core sequence; offline fixtures then compatible local model | Reproducible local implementation and hardware report |

## Entry diagnostics

- **M00:** change a Python program that reads JSON and writes a SQLite result; add one failure test; explain HTTP status, timeout and Git diff.
- **M01–M03:** distinguish inference from training, context from memory, structured output from validation, and model proposal from tool permission; demonstrate on a small application.
- **M04–M05:** build a source-labelled corpus; calculate retrieval and citation outcomes on labelled cases, including an unanswerable one.
- **M06–M09:** trace a bounded tool trajectory, deny an unsafe action, and explain whether an extra agent or framework improves the baseline.

Passing a diagnostic permits skipping instruction; it does not waive project evidence, security gates or the capstone defense. A learner may use a coding assistant to learn but must review the change and explain it without assistant-generated narration.

## Environment choices

| Choice | Useful for | Limitation to teach |
|---|---|---|
| Offline fixtures and deterministic code | Every core concept and CI | Does not measure live model quality |
| ChatGPT | Concept exploration and manual experiments | A chat session is not a reproducible API-backed application |
| OpenAI API | Optional programmatic provider implementation | Requires account access and usage controls; availability varies |
| Cursor or another coding assistant | Repository exploration and assisted implementation | Editor assistance is separate from the application's model runtime |
| Ollama or another local runtime | Optional private/local inference and embeddings | Capability and performance depend on model, runtime and hardware |
| Other hosted providers | Comparative adapters | APIs, schemas, tool behavior, price and data handling differ |

No path requires all of these. The learner chooses one live inference path when available, records the exact configuration, and keeps offline tests runnable.

## Accessibility and cost rules

Course instructions must state whether a step is offline, local-inference, free-tier-dependent, or paid. Do not promise free access or a fixed cost. Provide a small fixture and expected behavior for any concept that otherwise needs a model. Large-model, vector-database, cloud and distributed-inference tasks are advanced extensions rather than prerequisites. Provide shell examples for POSIX shells and PowerShell when commands differ; use repository-relative paths throughout.
