# Concept guide

A model adapter converts a stable task into a provider request and converts the response back. The application owns its input schema, output schema, timeout, error handling and usage boundary. The provider owns transport and model-specific fields. The interface must not pretend that every model supports the same structured-output or tool capability.

P1 first runs a fixture generator, then permits an optional model adapter. Output validation checks identity, length, uncertainty and source IDs. These checks catch malformed responses; they do not prove that every sentence is factually supported. Record refusal, invalid JSON, timeout and missing fields separately so retries do not hide a systematic failure. Never retry a write-capable action without an idempotency plan.

**Decision to defend:** Why is a model response with the correct JSON keys still untrusted? Add a test where it cites an unrelated source.
