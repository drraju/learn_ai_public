# Content provenance and migration decisions

This public record describes what was brought into the independent course and why. It does not publish the structure, schedule, progress records or notes from the private source project. The new repository has fresh Git history.

| Public artifact | Origin and treatment | Verification still required |
|---|---|---|
| `modules/m00-software/labs/` | Screened standard-library teaching code and invented sample files were adapted into the software foundations module. The sample text was rebranded for the public course. | Windows and Linux execution; final reuse-rights review |
| `modules/m01-foundations/labs/` | Three small offline demonstrations of token budgeting, vector similarity and attention were selected, with explicit warnings that they are teaching analogies. | Independent teaching review; final reuse-rights review |
| `projects/p03_tool_agent/seed/` | A deterministic synthetic investigation example was retained as a comparison baseline for the controlled-agent project. | Independent teaching review; final reuse-rights review |
| `modules/`, `projects/`, `implementations/`, `shared/`, `assessments/` | New public curriculum structure, synthetic fixtures, project increments and optional adapters were authored for this repository. | Stage 5 QA and Stage 6 release review |

Personal learning logs, schedules, private notes, downloaded documents, generated binaries, external course material, company-specific material, credentials, machine configuration and source Git history were excluded. The public project uses synthetic support issues and runbooks, relative paths and a default offline route.

## Acceptance workflow for future migrations

1. Record the learner outcome and why the material is needed.
2. Establish reuse rights and note any third-party attribution requirements.
3. Remove personal, company, customer and machine-specific details.
4. Replace external-note dependencies with self-contained explanation and official links.
5. Provide an offline fixture, a guided exercise, an independent challenge and failure-focused checks.
6. Validate local links, secret and privacy patterns, platform commands and version-sensitive claims.
7. Mark untested provider or operating-system paths as unverified.
8. Review the contribution boundary and update the technology register and changelog.

A file is not publication-ready merely because it passes a local test. The [QA report](QA_REPORT.md) records current evidence and gaps; the publication gate will review the final file set and licence compatibility.
