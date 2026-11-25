# M10 — Evaluation, security and observability

Status: draft teaching module. Estimated time: 20 hours. Prerequisites: M09. Required: Python 3.11+, Git and an ordinary laptop. Optional: a provider or coding assistant where linked. Offline API cost: zero; live usage varies by provider and model. No GPU is needed for the offline path.

## Study checkpoint

Prerequisite: M09. Practice: frozen P1–P5 cases and P6 evaluation plan. Continue when you can show a report with denominators, attack cases and open failures; then M11. Previous: [M09](../m09-orchestration/README.md); next: [M11](../m11-deployment/README.md). See the [study sequence](../../STUDY_SEQUENCE.md).

## Problem and objectives

The practical question is how to apply **frozen cases, denominators, policy invariants and traces** to the synthetic support workflow. By completion, explain the concept, run the reference, change one behavior, test a failure case, and defend the trade-off.

## Concept and architecture

Read the [concept guide](CONCEPTS.md) before modifying the reference implementation.


Frozen cases, denominators, policy invariants and traces. Keep model or tool proposals distinct from application policy. Identity, source scope, output validation and effect approval belong to the application. A saved response or toy vector demonstrates an interface; it does not prove model quality.

```mermaid
flowchart LR
    I[Validated input] --> P[Provider independent rule]
    P --> B[Bounded implementation]
    B --> V[Validation and evaluation]
```

Text equivalent: validated input passes through a stable rule and bounded implementation; evaluation checks the result. External content is untrusted at the implementation boundary.

## Guided demonstration

From the root run `python -m projects.p01_llm_app.evaluate`, `python -m projects.p02_rag.evaluate`, `python -m projects.p05_multi_agent.evaluate`, and `python -m projects.p06_capstone.evaluate`. Read its case-level results, then revisit P2 retrieval and P3 policy tests. Separate task-quality measures from invariant failures. On macOS/Linux, `python3` may replace `python`; on Windows, use `py -3` if necessary.

## Guided exercise

Extend the P2 case file and report hits, total and Recall@k. Start from the project code, write a failing test first, then make the smallest change that passes it. Record the command, test result and one limitation.

## Independent challenge

Add a malicious passage and show that it cannot change tool policy. Explain the invariant before reading the reference solution. Submit a short result with the input, expected result, observed result and a failure case.

## Project integration and assessment

Integrate the result into [P06_CAPSTONE](../../projects/p06_capstone/README.md). Completion requires a working change, a normal and a negative test, a measured or counted result with denominator where relevant, and an explanation of one design choice. Use the [assessment framework](../../ASSESSMENT_FRAMEWORK.md). A passing reference suite alone is not learner completion.

## Alternatives and limits

The fixture path is required. [Generation adapters](../../implementations/generation/README.md) and [embedding adapters](../../implementations/embeddings/README.md) are optional where relevant. ChatGPT or Cursor can assist development, but they are not interchangeable with a runtime API. Local inference requires a suitable model and hardware; hosted inference may incur cost. Compatibility must be tested per model and version.

## Common mistakes and troubleshooting

- If imports fail, run from the repository root.
- If a live call fails, return to the fixture path and check opt-in, model name, service availability and provider requirements.
- If a test passes but the claim is broad, add a negative case and state the untested boundary.

## Knowledge check and reading

Explain the data boundary, predict one failure, implement and test the challenge, then compare one alternative. Further reading: [Python documentation](https://docs.python.org/3/), [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28) for integration topics, and the official provider links in the [technology register](../../TECHNOLOGY_REGISTER.md). Links and example APIs were reviewed on 25 November 2026; this module's end-to-end teaching flow is not yet independently verified.
