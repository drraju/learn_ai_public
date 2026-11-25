# M12 — Capstone and portfolio defense

Status: draft teaching module. Estimated time: 30 hours. Prerequisites: M11 and earlier project evidence. Required: Python 3.11+, Git and an ordinary laptop. Optional: a provider or coding assistant where linked. Offline API cost: zero; live usage varies by provider and model. No GPU is needed for the offline path.

## Study checkpoint

Prerequisite: M11 and earlier project evidence. Practice: P6 evaluation, threat model, runbook and design defense. Continue when you can show one normal and one failure demonstration, a design explanation and an honest limits list. Previous: [M11](../m11-deployment/README.md). Finish with the P6 portfolio defense and use the [study sequence](../../STUDY_SEQUENCE.md) to check your evidence.

## Problem and objectives

The practical question is how to apply **requirements traceability, release evidence and operating limits** to the synthetic support workflow. By completion, explain the concept, run the reference, change one behavior, test a failure case, and defend the trade-off.

## Concept and architecture

Read the [concept guide](CONCEPTS.md) before modifying the reference implementation.


Requirements traceability, release evidence and operating limits. Keep model or tool proposals distinct from application policy. Identity, source scope, output validation and effect approval belong to the application. A saved response or toy vector demonstrates an interface; it does not prove model quality.

```mermaid
flowchart LR
    I[Validated input] --> P[Provider independent rule]
    P --> B[Bounded implementation]
    B --> V[Validation and evaluation]
```

Text equivalent: validated input passes through a stable rule and bounded implementation; evaluation checks the result. External content is untrusted at the implementation boundary.

## Guided demonstration

Run `python -m projects.p06_capstone.evaluate` and the root test suite, then assemble your own P1–P6 evidence. Use the [P6 threat model](../../projects/p06_capstone/THREAT_MODEL.md) and [runbook](../../projects/p06_capstone/RUNBOOK.md) to defend one design decision and one production gap. On macOS/Linux, `python3` may replace `python`; on Windows, use `py -3` if necessary.

## Guided exercise

Assemble P1–P6 evidence and run the offline suite. Organize your own evidence by requirement, run its checks, and identify missing evidence before claiming completion. Record the command, test result and one limitation.

## Independent challenge

Defend one architecture decision and identify what is still unverified. Explain the invariant before reading the reference solution. Submit a short result with the input, expected result, observed result and a failure case.

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
