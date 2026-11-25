# Migration status

Reviewed 25 November 2026. This is a public, unfinished draft at [drraju/learn_ai_public](https://github.com/drraju/learn_ai_public), not a tagged release or readiness claim.

| Stage | Status | Evidence and next gate |
|---|---|---|
| 1. Discovery and audit | Complete for planning | Source inventory and privacy risks reviewed |
| 2. Curriculum redesign | Accepted for implementation | [Curriculum](CURRICULUM.md), [learning paths](LEARNING_PATHS.md), [project progression](PROJECT_PROGRESSION.md) |
| 3. Public architecture | Accepted for implementation | [Architecture](ARCHITECTURE.md), [contribution guide](CONTRIBUTING.md), [decisions](DECISIONS.md) |
| 4. Creation and migration | Implementation draft | M00–M12 teaching pages and concept guides, six reference projects, fixture and optional provider paths, issue templates and offline CI exist. Local verification: 15 project/adapter tests including MCP and HTTP, 14 M00 lab tests, 10 migrated seed tests, metadata/links and project commands passed on macOS. Independent teaching, Windows/Linux CI and live-provider verification remain open. |
| 5. Quality assurance | Audited; gate not passed | [QA report](QA_REPORT.md) records local passes, fixes and high-priority cross-platform, project-completion, live-provider and rights gaps |
| 6. Release readiness | Pending | Rights and licence decision, final release review and explicit approval for a tagged release |

The independent repository has its own `main` history and GitHub remote. The owner authorized publication as an unfinished public draft despite the failed Stage 5 gate. No licence is granted by this repository yet; external contributions remain closed pending the rights and licence review.

## Reuse and limitations

The M00 standard-library lab was migrated from a screened source seed; M01's three toy demonstrations came from the source archive after review. The original deterministic investigation lives at `projects/p03_tool_agent/seed/` for comparison. Other personal learning records, downloads, proprietary material, generated binaries and source Git history were excluded. P6 is a local engineering reference with documented production gaps. Any external contributions wait for a licence and rights decision.
