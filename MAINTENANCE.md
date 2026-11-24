# Curriculum and technology maintenance

## Separate stable material from changing integrations

Concept lessons explain mechanisms and invariants. Provider directories hold APIs, models, SDKs and environment instructions. Projects choose implementations, then evaluate them with shared cases. A change to a provider module should not require rewriting the concept lesson unless the underlying concept or its teaching sequence is genuinely wrong.

## Review cadence

| Review | Frequency after publication | Scope | Recorded outcome |
|---|---|---|---|
| Incoming issue triage | Weekly when activity exists | Broken links, security, example failures, learner confusion | Owner, priority and next action |
| Provider and SDK check | Monthly for recommended adapters | Official docs, supported versions, deprecations, live smoke test where access exists | Dated manifest and verification result |
| Curriculum and project review | Quarterly | Prerequisites, learner evidence, project relevance, overlap and gaps | Decision record and roadmap change |
| Security and rights audit | Before every release and after a material data/tool change | Secrets, provenance, licences, prompt injection, authorization and dependency risk | Gate report |
| Watchlist review | Quarterly | Emerging standards and framework proposals | Adopt, keep experimental, defer or remove |

These are target cadences, not a claim that future volunteers are already assigned. A recommended adapter without a maintainer or current verification is downgraded to “unverified”; the offline path remains available.

## Technology register states

- **Documented:** official source checked; no local compatibility claim.
- **Verified:** exact version and environment exercised with reproducible result and date.
- **Limited:** works only for a stated capability or configuration.
- **Unverified:** verification expired, unavailable or never performed.
- **Deprecated:** replacement or migration path published; no new lessons depend on it.
- **Removed:** code no longer shipped; historical decision remains in changelog.

The register in [TECHNOLOGY_REGISTER.md](TECHNOLOGY_REGISTER.md) records the current state. Implementation manifests hold finer-grained model, SDK, runtime and OS results. A release may include a documented but unverified alternative only if clearly labelled optional and excluded from the recommended path.

## Upgrade procedure

1. Identify the change in official documentation or a reproducible failure.
2. State affected lessons, adapters, projects and evaluation cases.
3. Update an adapter in isolation; pin or record exact tested versions in its environment.
4. Run offline contract tests and optional live tests with documented account/cost limits.
5. Compare behavior, latency and cost on frozen cases; note capability differences.
6. Update manifest, register, lesson link, changelog and migration note.
7. Promote only after review. Roll back or mark limited when results regress.

Model names, prices and subscription access change; do not hardcode them in stable lessons. Record a dated example and direct learners to official pricing/availability pages before paid work. Do not automatically adopt a new model, framework or protocol release.

## Deprecation and breakage

When an API is deprecated, first mark the adapter limited or deprecated with the official notice, last working version and fallback. Keep the concept and offline fixture usable. Provide a replacement and migration exercise if the old path taught a distinct concept; otherwise remove the adapter after its dependent examples have migrated. A security-critical break can disable a provider path immediately while the maintainer records why.

A broken example receives an issue with reproduction steps and affected platforms. If the required path fails, mark the module unverified until repaired. Optional paths may remain with an explicit known limitation. Do not hide failures by weakening tests or changing expected results without explaining the behavior change.

## New technology entry rule

A proposal must show learner value, maturity, real-world relevance, alternatives, limits, maintenance owner, security implications and a measurable comparison to a simpler baseline. Mature patterns can enter core modules; provider-specific products enter implementations; emerging standards enter experiments; speculative ideas stay in the watchlist. An experiment expires or is renewed at its next quarterly review.
