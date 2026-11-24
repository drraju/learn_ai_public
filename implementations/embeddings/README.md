# Embedding choices

The fixture is a deterministic token-hash vector for teaching cosine similarity; it has no semantic model. The optional Ollama adapter calls loopback `/api/embed` with truncation disabled and validates one returned vector. Live runtime/model/hardware compatibility is unverified. Lexical retrieval remains the required P2 baseline. [Ollama embed API](https://docs.ollama.com/api/embed), reviewed 25 November 2026.
