# Curriculum

Status: Stage 4 draft, 25 November 2026. This is a self-paced sequence with draft M00–M12 pages and six reference projects. Stage 5 teaching and cross-platform QA remain open.

## Learning contract

Progress through **understand → experiment → build → test → evaluate → deploy → operate**. A module is complete only when the learner can explain its mechanism, change an implementation, pass a failure-focused check, and state a limitation. The six projects in [PROJECT_PROGRESSION.md](PROJECT_PROGRESSION.md) provide the cumulative evidence.

Core concepts are independent of a model provider. Every model-backed exercise starts with a deterministic fixture or reference baseline, then offers only the provider paths whose capabilities have been verified. Model access is optional until the learner elects a runtime. An exercise may record a blocked provider path without blocking a concept assessment.

The estimated hours below are planning ranges, not deadlines. Python 3.11+, Git, and a terminal are the initial tools; a code editor is optional. No paid account, GPU, container runtime, or cloud account is required for the early modules. Later deployment can use a local process.

| ID | Module and estimated time | Prerequisites | Evidence gate | Project |
|---|---|---|---|---|
| M00 | Software and reproducible workflow, 12–20 h | None | Explain and test a Python/HTTP/SQLite change | P1 |
| M01 | AI and LLM foundations, 10–16 h | M00 basics | Compare a deterministic baseline and model behavior | P1 |
| M02 | Model interfaces and application contracts, 12–18 h | M01 | Validate input/output, timeout, refusal and budget paths | P1 |
| M03 | Prompt and context engineering, 10–16 h | M02 | Run a frozen comparison and explain failure slices | P1 |
| M04 | Data ingestion and provenance, 12–18 h | M00, M02 | Rebuild, update and delete a versioned corpus | P2 |
| M05 | Retrieval and grounded generation, 18–28 h | M04, M01 | Compare retrieval baselines and citation support | P2 |
| M06 | Tool calling and bounded agents, 18–28 h | M02, M05 | Enforce tool policy and termination outside the model | P3 |
| M07 | State, memory and human control, 14–22 h | M06 | Resume safely; deny stale or mismatched approval | P3 |
| M08 | MCP and external integration, 12–20 h | M06, M07 | Complete a versioned, permission-checked exchange | P4 |
| M09 | Orchestration and multi-agent design, 14–24 h | M06–M08 | Compare complexity and outcomes with a single-agent baseline | P5 |
| M10 | Evaluation, security and observability, 20–30 h | M05–M09 | Pass a release gate with task, trajectory and attack cases | P1–P6 |
| M11 | Deployment, reliability and governance, 20–30 h | M10 | Reproduce a release, recover a failure and report operations | P6 |
| M12 | Capstone and portfolio defense, 30–50 h | M00–M11 | Demonstrate, test and defend the complete system | P6 |

M10 is taught formally after learners have a system to evaluate, but its methods are introduced in M00 and practiced at every project gate. AI-assisted software engineering is a continuing practice: use an assistant to inspect a repository, propose a bounded change, review its diff, and verify it independently. No particular coding assistant is required.

## Module specifications

Each specification states the stable concept, practical work, assessment and implementation boundary. The [module contract](MODULE_TEMPLATE.md) and draft lesson pages implement this sequence; independent teaching review remains open.

### M00 — Software and reproducible workflow

**Concepts:** Python values and types, functions, files, JSON, HTTP, SQLite, version control, tests, error handling, and reproducibility. **Architecture:** input → validation → deterministic logic → storage/output → tests. **Lab:** extend the existing standard-library file catalogue and a synthetic request handler. **Challenge:** repair a malformed input path without changing unrelated behavior. **Assessment:** a clean run plus a boundary test and an unaided explanation. **Tools/cost/hardware:** Python and Git; zero API spend; ordinary laptop. **Limit:** the migrated lab has local macOS verification; Windows and Linux remain to be checked.

### M01 — AI and LLM foundations

**Concepts:** training versus inference, transformer intuition, tokens, context limits, embeddings, sampling, model selection, quality and latency. **Architecture:** tokenizer/model/runtime are distinct from application policy. **Lab:** compare a rule-based answer, a saved model response fixture, and an optional local or hosted model on the same synthetic inputs. **Challenge:** diagnose truncation and uncertain answers. **Assessment:** report observed behavior, not a universal model claim. **Tools/cost/hardware:** offline path is free; live path depends on provider or local memory.

### M02 — Model interfaces and application contracts

**Concepts:** request/response adapters, schema validation, timeouts, retries, refusal, provider errors, usage and cost boundaries. **Architecture:** application contract → provider adapter → external model; policy and validation stay in application code. **Lab:** build P1 with a fake provider and one chosen live provider. **Challenge:** swap providers without changing the application contract. **Assessment:** invalid output, timeout, unavailable model and budget cases pass. **Limit:** a common interface cannot promise identical provider behavior.

### M03 — Prompt and context engineering

**Concepts:** task instructions, examples, context selection, source precedence, context budgeting and prompt versioning. **Architecture:** trusted policy and untrusted task data are separate inputs. **Lab:** improve P1 on a frozen case set; record prompt, model and fixture versions. **Challenge:** reduce context while preserving answers and uncertainty. **Assessment:** compare task quality, latency and failure cases with the M02 baseline. **Limit:** prompt changes do not enforce permissions or schema validity.

### M04 — Data ingestion and provenance

**Concepts:** source rights, parsing, normalization, chunking, metadata, access scope, versioning, freshness and deletion propagation. **Architecture:** source → validated extraction → canonical records → searchable index, all linked by stable IDs. **Lab:** ingest invented runbooks in Markdown and JSON. **Challenge:** update and delete a source without leaving stale searchable copies. **Assessment:** lineage and deletion tests pass. **Tools:** standard library first; extra parsers are optional.

### M05 — Retrieval and grounded generation

**Concepts:** lexical search, embeddings, vector similarity, hybrid retrieval, reranking, answer grounding, citations and abstention. **Architecture:** retrieval evaluation is separate from answer evaluation. **Lab:** compare lexical baseline with one optional embedding path, then generate or assemble answers from authorized passages. **Challenge:** hard negatives, exact identifiers and unanswerable questions. **Assessment:** report Recall@k, citation support and abstention with denominators. **Extensions:** graph or hierarchical retrieval only when a measured task warrants it.

### M06 — Tool calling and bounded agents

**Concepts:** tool descriptions, argument schemas, dispatch, authorization, side effects, planning, observations and stopping. **Architecture:** the model may propose; application code validates and executes. **Lab:** extend the synthetic investigation baseline with read-only tools. **Challenge:** duplicate proposals, unknown tool, malformed arguments and no-progress loop. **Assessment:** every trajectory terminates within time/call limits and forbidden actions are denied. **Limit:** tool calling alone does not make a system autonomous or reliable.

### M07 — State, memory and human control

**Concepts:** explicit task state, checkpoints, scoped memory, retention, contradiction, idempotency and approval bound to an exact action. **Architecture:** durable state and approval records live outside model context. **Lab:** pause and resume P3 around a simulated write. **Challenge:** replay, stale approval and cross-tenant memory. **Assessment:** no unapproved effect, duplicate effect or hidden state loss. **Tools:** SQLite remains sufficient for the local course.

### M08 — MCP and external integration

**Concepts:** tools, resources, discovery, protocol versions, identity propagation and client/server trust. **Architecture:** host policy → MCP client → server → authorized resource. **Lab:** expose a synthetic read-only lookup, then write a client with explicit allowlist and denial tests. **Challenge:** mismatched capability or protocol version. **Assessment:** record the tested spec and SDK versions; demonstrate permitted and denied calls. **Limit:** availability and authentication differ by host and server.

### M09 — Orchestration and multi-agent design

**Concepts:** workflow versus agent, routing, parallelism, handoff, shared context, disagreement, recovery and coordination cost. **Architecture:** start with one deterministic workflow; add a graph or second agent only for an identified need. **Lab:** compare a specialized two-role workflow with P3 on the same cases. **Challenge:** contradictory agent outputs and partial failure. **Assessment:** retain extra agents only if measured quality or maintainability justifies them. **Extension:** A2A as a separately versioned interoperability experiment.

### M10 — Evaluation, security and observability

**Concepts:** labelled sets, holdouts, task/trajectory metrics, retrieval and citation metrics, prompt injection, least privilege, data leakage, traces and cost per successful task. **Architecture:** deterministic policy invariants gate model quality scores. **Lab:** freeze regression cases and instrument P1–P5. **Challenge:** a malicious source passage and poisoned tool result. **Assessment:** report passes, failures, uncertainty, denominators and release decision. **Limit:** model graders require human calibration and cannot replace policy checks.

### M11 — Deployment, reliability and governance

**Concepts:** service contracts, packaging, configuration, identity, quotas, retries, queues, rollback, SLOs, incident response, data retention and model/provider change review. **Architecture:** stateless interface + durable task state + bounded worker + controlled data store. **Lab:** deploy P6 as a local service and rehearse failure and rollback. **Challenge:** duplicate event and unavailable provider. **Assessment:** another learner reproduces the release and recovery from instructions. **Extensions:** containers, cloud or distributed serving after the local release passes.

### M12 — Capstone and portfolio defense

**Concepts:** requirements traceability, architecture trade-offs, evaluation, operations, and honest scope claims. **Lab:** assemble P6 from reusable modules; show a synthetic end-to-end case and a failure case. **Assessment:** submit source, tests, fixtures, evaluation report, threat model, release manifest, runbook and short design defense. **Completion:** the learner explains a change unaided and identifies what remains unverified. Production readiness is a separate decision.

## Assessment rules

Every module uses the same [assessment framework](ASSESSMENT_FRAMEWORK.md). A reference implementation passing tests does not prove learner competence. Independent implementation, negative cases and explanation are separate evidence. The [learning paths](LEARNING_PATHS.md) permit experienced learners to skip prerequisite instruction only after passing its diagnostic gate.

## Technology review boundary

No model, SDK, framework or protocol version is mandated by this syllabus. The implementation register in Stage 3 must hold official documentation, version, verification date, operating-system requirements and limitations. Official sources checked for this proposal include [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling), [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses), [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling), [MCP](https://modelcontextprotocol.io/specification/2026-07-28) and [A2A](https://a2a-protocol.org/latest/specification/).
