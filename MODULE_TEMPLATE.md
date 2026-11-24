# Module authoring contract — Stage 2 proposal

Use this contract for every M00–M12 lesson in Stage 4. A module may comprise several lessons, but its landing page must make all fields discoverable.

## Metadata

- ID and title:
- Status: proposed / draft / verified / deprecated
- Last verified date:
- Estimated time:
- Prerequisites and diagnostic:
- Required tools and minimum versions:
- Optional tools:
- Model/API requirements and whether an offline path exists:
- Expected expenditure: offline zero API spend; list variable paid usage separately
- Hardware and operating-system requirements:
- Expected output and completion criteria:

## Teaching sequence

1. **Overview and problem:** a practical question the learner can answer after the module.
2. **Objectives:** observable verbs and evidence, not familiarity claims.
3. **Conceptual foundation:** mechanism independent of any provider.
4. **Architecture:** diagram plus text equivalent; identify trust and data boundaries.
5. **Provider-independent pattern:** inputs, outputs, invariants, errors and tests.
6. **Guided demonstration:** exact commands and expected result on synthetic fixtures.
7. **Alternative implementations:** link to independently maintained provider modules; state capability and cost differences.
8. **Guided exercise:** partial scaffold and checks.
9. **Independent challenge:** changed requirement or unseen failure case.
10. **Project integration:** the increment and its acceptance criteria.
11. **Testing and evaluation:** normal, boundary, failure and permission cases; relevant metrics and denominators.
12. **Security and privacy:** data scope, secrets, tool permissions and trace redaction as applicable.
13. **Common mistakes and troubleshooting:** symptom, likely cause and verification.
14. **Knowledge assessment:** explain, implement, evaluate and defend a trade-off.
15. **Further reading:** official documentation and selected stable references, each dated.
16. **Limitations:** capabilities not supported, not tested or requiring separate authorization.

## Editorial checks

Commands must work from a stated relative directory. Screenshots and diagrams need text equivalents. A provider adapter may be omitted when the capability is unavailable. No lesson may claim that a passing reference solution proves the learner passed. Report actual verification separately from an expected outcome.
