# Contributing

This public draft documents the proposed contribution process. Outside contributions begin only after the rights and licence gate is complete.

## Choose a bounded contribution

| Contribution | Primary area | What may change |
|---|---|---|
| Concept correction or new exercise | `modules/mNN-topic/` | One module and its tests, rubric and links |
| New provider or local runtime | `implementations/capability/provider/` | One adapter, manifest, fixtures and contract tests |
| Project increment | `projects/pNN-topic/` | One project, its evaluation cases and documentation |
| Evaluation or synthetic data | `assessments/` or `shared/fixtures/` | Labelled cases with rights and provenance |
| Emerging technology trial | `experiments/` | Time-bounded experiment and keep/remove decision |
| Documentation, accessibility or translation | Affected pages | Clear navigation, accurate commands, diagrams with text equivalents |

Open a focused issue or proposal before changing the module order, shared contract or security policy. Small fixes may proceed directly after outside contributions are opened. A provider contribution should not rewrite the concept lesson merely to match its SDK.

## Contribution format

Use `mNN-topic` for lesson directories and `pNN_topic` for importable Python project directories. Provider paths use `implementations/<capability>/<provider>`. Keep one concept or behavior per change. Explain:

1. The learner problem and the concept taught.
2. The source or official documentation used, with date.
3. The exact files and expected outcome.
4. Commands run, operating systems tested and results.
5. Costs, hardware, account or API requirements.
6. Limitations, known failures and alternatives.
7. Whether any material came from another source and its reuse terms.

Do not include private or customer data, credentials, paid-course text, model weights, local home paths, generated environments or copied repository history. Use invented fixtures with explicit provenance. External URLs are references, not permission to copy content.

## Checks by contribution type

- **Documentation:** resolve all local links; check commands from the stated directory; verify diagrams have text equivalents; run privacy and portability scans.
- **Core code:** add tests for normal, boundary and failure behavior. Keep the required offline path dependency-free unless an architectural decision approves a change.
- **Provider adapter:** include mocked contract tests that run without an account, plus separately marked live verification with exact model/SDK/runtime versions. Test refusal, timeout, malformed output, unsupported capability and budget path where applicable.
- **Tool or protocol integration:** prove allowlist, argument validation, identity scope, denial, timeout and version/capability handling. Do not treat server discovery as authorization.
- **Project or evaluation cases:** state the problem, requirements, diagram, test data permission, scoring denominator, security boundary and deployment instructions.

Do not make paid calls or download large models in default CI. Mark optional integration tests so they cannot run accidentally. A passing reference test is not evidence that a learner completed the exercise.

## Review and acceptance

A reviewer checks correctness, prerequisite fit, concept/provider separation, learner accessibility, security, rights and maintenance cost. A second reviewer is required for a new external tool, write-capable action, identity boundary or material change to a shared contract when the community has enough maintainers. Until then, the maintainer records the same checklist and unresolved risk in the change.

Acceptance requires:

- A clear learner gain and an independently runnable or reviewable artifact.
- Official documentation for version-sensitive claims and a dated manifest.
- Offline tests and the appropriate optional integration evidence.
- A named maintainer or review owner and an update path.
- No sensitive data, unsupported compatibility claim or unexplained broken link.

Review may request a simpler baseline or reject a technology that adds maintenance without measurable learning value. A rejected experiment can remain documented in the watchlist with its reason.

## Versioning and change notices

Conceptual curriculum revisions use a dated changelog entry and a migration note when prerequisites change. Provider adapters record their own tested versions; a framework upgrade is not silently treated as a curriculum rewrite. Breaking shared-contract changes require an architecture decision, affected-module list, migration path and full offline regression check. [MAINTENANCE.md](MAINTENANCE.md) defines deprecation.

The repository licence is pending a rights and compatibility review. Do not solicit or merge outside contributions before that decision is published. Issue, feature-request and provider templates are present and will be reviewed again at the release gate.
