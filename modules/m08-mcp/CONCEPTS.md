# Concept guide

MCP separates a host, its client and a server exposing tools, resources or prompts. Discovery tells the host what a server offers; it does not grant the model permission to use everything. The host must allowlist capabilities and validate arguments, while the server must validate again at its own data boundary. Identity and authorization differ by transport and deployment.

P4 uses the optional Python SDK in memory. It exposes one synthetic read-only runbook lookup and tests an allowed call and host denial. This verifies a local SDK exchange, not remote transport, user identity or compatibility with every host. Record the tested SDK version and protocol reference; use a direct adapter as a simpler comparison when interoperability is not needed.

**Decision to defend:** If an MCP server advertises a write tool after discovery, which boundary should block an unapproved call?
