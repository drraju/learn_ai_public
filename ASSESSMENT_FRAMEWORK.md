# Assessment framework — Stage 2 proposal

## Evidence levels

| Level | Learner demonstrates | Required artifact |
|---|---|---|
| Explain | Mechanism, boundaries and one failure | Short explanation or diagram |
| Implement | Independent change on a new requirement | Source diff and execution command |
| Test | Normal and failure behavior | Automated or reproducible manual checks |
| Evaluate | Baseline, metric, denominator and error slices | Evaluation report with fixtures |
| Operate | Deployment, recovery and ownership | Release manifest and runbook |

A learner must satisfy all levels assigned to a module or project. Time spent, a working reference solution, and an AI-generated explanation are not substitutes.

## Common scoring

Each criterion is scored 0–3: 0 absent, 1 attempted with a material gap, 2 meets the stated acceptance test, 3 meets it and explains the trade-off. A project passes at 2 or higher on every critical criterion; an average score cannot hide a failed security or correctness control.

Critical criteria: input and output contract; source and citation integrity where relevant; authorization and side-effect control; bounded termination; reproducibility; failure handling; independent explanation. Later projects add retrieval, task and trajectory quality; latency and cost; observability; rollback and operational ownership.

## Evaluation sets

Keep development and holdout cases separate. Each case records source permission, input, expected behavior, version, labels and why it exists. Report both numerator and denominator for success, retrieval Recall@k, citation support, abstention, invalid tool calls, unauthorized actions and duplicate effects. Show latency and cost distributions only when sample size and measurement method are stated. Evaluate a new provider, prompt or framework against the same cases and policy invariants before promoting it.

Use deterministic checks for policy boundaries. Human review is required for ambiguous answer quality, with disagreement recorded. A model judge may assist with triage only after calibration against human-labelled cases.

## Project submission

Each project supplies: problem statement; functional and non-functional requirements; architecture diagram and text equivalent; technology choices and alternatives; runnable implementation; normal and failure tests; evaluation report; security notes; deployment and rollback steps; deliverables; extension challenges; and an honest list of unverified claims. [PROJECT_PROGRESSION.md](PROJECT_PROGRESSION.md) defines the six gates.
