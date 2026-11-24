# Technology register

Documentation rechecked on 25 November 2026; Stage 5 local test evidence is recorded in [QA_REPORT.md](QA_REPORT.md). A documentation check or mocked test does not establish live model compatibility. Pin versions only after tested evidence is available.

| Technology | Role and maturity | Local verification | Official source | Alternatives and limitations |
|---|---|---|---|---|
| Python standard library | Established; required offline path | Reference suites passed on macOS Python 3.11.17 and 3.13.14; Windows/Linux CI pending | [Python docs](https://docs.python.org/3/) | Other languages later; current code is Python |
| SQLite | Established; migrated M00 lab | M00 lab passed on macOS Python 3.11.17 and 3.13.14 with loopback enabled | [SQLite](https://www.sqlite.org/about.html) | Not identity or access control; PostgreSQL for measured scale |
| OpenAI Responses API | Optional hosted generation | Documentation and mocked contract only; model/SDK live version unverified | [Text generation](https://developers.openai.com/api/docs/guides/text) | Ollama or other adapters; billing and data handling vary |
| Ollama chat and embed API | Optional local generation and vectors | Endpoint shape reviewed, live model/runtime unverified | [Chat](https://docs.ollama.com/api/chat), [Embed](https://docs.ollama.com/api/embed) | Hardware and model capabilities vary; fixture/lexical fallback |
| MCP | Interoperability concept and optional P4 SDK example | MCP Python SDK 2.3.0 in-process exchange passed on macOS Python 3.12.12; remote transport and identity untested | [Protocol](https://modelcontextprotocol.io/specification/2026-07-28), [Python SDK](https://py.sdk.modelcontextprotocol.io/get-started/testing/) | Direct adapter baseline; protocol does not authorize tools |
| A2A, graph orchestration, OpenTelemetry | Optional experiments/watchlist | No course integration verified | [A2A](https://a2a-protocol.org/latest/specification/), [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) | Plain Python workflow and structured local traces first |

| GitHub Actions checkout/setup-python | Cross-platform CI configuration | v7 examples match official action docs; workflow has not run because the repository is unpublished | [Checkout](https://github.com/actions/checkout), [Setup Python](https://github.com/actions/setup-python) | Local macOS checks only until hosted runners execute |

Provider adapters should record exact package/runtime/model version, OS and hardware, date, cost category, failure paths and maintainer after a live check. Empty verification fields mean unverified. See [maintenance policy](MAINTENANCE.md).
