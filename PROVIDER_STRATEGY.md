# Provider and environment strategy

The course teaches application contracts first. A provider implementation is a replaceable example, not the definition of a concept. Provider support is capability-specific and must be verified against an exact model, runtime, SDK and date before a lesson claims it works.

## Common application contracts

1. **Generation:** request contains task data, context, limits and a trace ID; response records text or structured data, refusal/error status, usage when available, model identifier and timing.
2. **Embedding:** request contains permitted text and batching limits; response records vectors, dimension, model identifier and normalization assumptions.
3. **Tool proposal:** the model may suggest a named call with arguments; application code validates schema, identity, policy, budget and approval before dispatch.
4. **Retrieval:** query, identity and source version produce authorized passages with stable IDs and provenance. Retrieval is application behavior, not a model feature.
5. **Evaluation:** the same labelled cases and deterministic invariants run against every adapter; provider-specific results remain separate.

The interface must expose capability differences instead of hiding them. It may return “unsupported” for a feature, and an exercise must provide an alternate route or mark that path unavailable. Avoid a single “OpenAI-compatible” flag as proof of full interoperability.

## Learning environments

| Environment | Course role | Access and limitations | Fallback |
|---|---|---|---|
| Offline fixtures | Required reproducible baseline | No live model behavior | None needed |
| ChatGPT | Manual exploration, explanation and prompt experiments | Availability and features depend on account; manual sessions do not replace API tests | Offline case worksheets |
| OpenAI API | Optional programmatic generation, structured output and tool proposal | Account and usage billing may apply; use the official API guide and model-specific support | Offline fixtures or another verified API |
| Cursor or another coding assistant | Optional help editing, testing and reviewing the repository | It is a development environment; application runtime is configured separately | Any editor and terminal |
| Ollama or compatible local runtime | Optional local generation, embeddings and tool proposal where the model supports them | Model availability, memory, speed and feature behavior vary by hardware and runtime | Offline fixtures or optional hosted API |
| Other hosted/open-source provider | Independent adapter contribution | API and data-handling differences need their own tests | Another verified adapter |

OpenAI's current documentation distinguishes [function calling](https://developers.openai.com/api/docs/guides/function-calling), where a model requests a tool action, from [structured responses](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses), which constrain the answer format. Neither replaces application-side authorization or validation. Ollama documents [tool calling](https://docs.ollama.com/capabilities/tool-calling), [embeddings](https://docs.ollama.com/capabilities/embeddings) and [structured output](https://docs.ollama.com/capabilities/structured-outputs); its structured-output page notes a cloud limitation. These documentation findings were rechecked on 25 November 2026, not compatibility claims for every model.

## Exercise fallback ladder

1. Run the deterministic fixture and tests.
2. Run a small local model if the learner's hardware and selected model support the capability.
3. Run one budgeted hosted provider if the learner has access.
4. Compare a second provider only when it tests a meaningful difference.

Each provider lesson records: official documentation URL, exact SDK/runtime/model version, verification date, operating systems tested, configuration variables, expected expenditure category, hardware observations, supported capabilities, observed limitations, security/data-handling considerations, test command and fallback. Never hardcode a real credential or publish a model weight.

## Interoperability boundary

MCP is taught as a client/server protocol for tools and resources, using a [dated specification](https://modelcontextprotocol.io/specification/2026-07-28). A2A is an advanced option for independent agent communication using its [published specification](https://a2a-protocol.org/latest/specification/). Neither protocol is a substitute for authorization, trust-boundary review or task evaluation. New protocol features enter lessons only after a versioned local demonstration and a maintenance owner are available.

The first local model results and failure cases are in [LIVE_VERIFICATION.md](LIVE_VERIFICATION.md). Optional providers remain capability-specific: a passed generation case does not imply embedding support.
