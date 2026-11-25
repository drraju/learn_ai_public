# Learn AI Public

An independent public draft of a vendor-neutral, project-driven Agentic AI learning platform. It progresses through **understand → experiment → build → test → evaluate → deploy → operate**. The Stage 5 readiness gate has not passed; this is an unfinished draft, with no tagged release or licence yet.

## Who this is for

Beginners with Python basics, software developers moving into AI engineering, and practitioners who want to evaluate agentic systems. The offline path needs Python 3.11+, Git, a terminal and an ordinary laptop. No paid account, GPU, model download or cloud service is needed. A code editor is optional. Hosted and local model paths have separate requirements and are never silently used by the default exercises.

## Start here

1. Clone this repository and run commands from its root.
2. Follow the [study sequence](STUDY_SEQUENCE.md). Start with [M00](modules/m00-software/README.md) and its lab, then M01; start P1 after M02 and finish its checkpoint after M03.
3. Use [learning paths](LEARNING_PATHS.md) for a diagnostic skip and the [curriculum](CURRICULUM.md) for full module outcomes. A skip does not waive project evidence.
4. Run `python -m unittest discover -s tests -p "test_*.py" -v` and `python tools/check_repo.py` from the root. These check the reference; follow each module's own exercise and independent challenge for learner work.
5. Record your results with the [assessment framework](ASSESSMENT_FRAMEWORK.md) and [project rubric](assessments/rubrics/project_rubric.md).

On macOS/Linux, `python3` may replace `python`; on Windows, use `py -3` if necessary. Run `python -m unittest discover -s modules/m00-software/labs/reference -p "test_*.py" -v` for the migrated foundations lab. The HTTP test needs loopback socket permission. From `projects/p03_tool_agent/seed`, run `python -m unittest discover -s tests -p "test_*.py" -v` for the migrated baseline.

## Providers and environments

The default generation and retrieval paths use synthetic fixtures. [Generation adapters](implementations/generation/README.md) document optional OpenAI API and Ollama choices; [embedding adapters](implementations/embeddings/README.md) document a toy vector and optional Ollama embedding path. [MCP](implementations/interoperability/mcp/README.md) is an isolated optional integration. ChatGPT and Cursor can support concept exploration or coding; they are not required runtimes. Live examples require explicit opt-in and provider-specific installation, model and cost review. No provider is claimed universally compatible.

## Structure and progress

[Architecture](ARCHITECTURE.md) explains module, project, provider and trust boundaries. [Technology register](TECHNOLOGY_REGISTER.md) records verified versus unverified claims. [Migration status](MIGRATION_STATUS.md) and the [Stage 5 QA report](QA_REPORT.md) list what runs, what was checked and what still blocks release. [Contribution guide](CONTRIBUTING.md), [roadmap](ROADMAP.md), [maintenance policy](MAINTENANCE.md) and [changelog](CHANGELOG.md) support future community work. The owner authorized publication of this unfinished draft while the Stage 5 and Stage 6 gates remain open. See the QA report before using or contributing to the material.
