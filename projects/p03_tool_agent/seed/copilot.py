"""Offline learning reference: tenant-scoped lexical retrieval and bounded tools.

This is an extractive, deterministic reference. It does not call an LLM or implement
production identity. The identity object must come from a trusted adapter in a real app.
"""
from dataclasses import dataclass
import json
import re

ALERTS = {
    "A1": {"id": "A1", "tenant": "alpha", "service": "checkout", "severity": 3, "symptom": "timeout"},
    "A2": {"id": "A2", "tenant": "beta", "service": "database", "severity": 2, "symptom": "backup"},
}
DOCUMENTS = [
    {"id": "runbook-1", "tenant": "alpha", "title": "Checkout timeout", "text": "For checkout timeout inspect downstream latency. Restart requires approved change.", "source": "synthetic://alpha/runbooks/timeout"},
    {"id": "runbook-2", "tenant": "beta", "title": "Database backup", "text": "For database backup failure inspect the backup job logs.", "source": "synthetic://beta/runbooks/backup"},
]

@dataclass(frozen=True)
class Identity:
    user: str
    tenant: str
    roles: frozenset[str]

def validate_alert(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError("alert must be an object")
    if not isinstance(value.get("id"), str) or not value["id"]:
        raise ValueError("non-empty id required")
    if type(value.get("severity")) is not int or not 1 <= value["severity"] <= 4:
        raise ValueError("severity must be an integer 1..4")
    return dict(value)

def get_alert(identity: Identity, alert_id: str) -> dict:
    if "reader" not in identity.roles:
        raise PermissionError("reader role required")
    # Same not-found result for absent and inaccessible records avoids existence disclosure.
    alert = ALERTS.get(alert_id)
    if alert is None or alert["tenant"] != identity.tenant:
        return {"error": "not_found"}
    return validate_alert(alert)

def terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def retrieve(identity: Identity, query: str, limit: int = 3) -> list[dict]:
    if "reader" not in identity.roles:
        raise PermissionError("reader role required")
    if not 1 <= limit <= 10:
        raise ValueError("limit must be 1..10")
    query_terms = terms(query)
    # Authorise candidates BEFORE scoring or exposing content to an adapter.
    visible = [doc for doc in DOCUMENTS if doc["tenant"] == identity.tenant]
    scored = [(len(query_terms & terms(doc["title"] + " " + doc["text"])), doc) for doc in visible]
    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [dict(doc, score=score) for score, doc in scored[:limit] if score > 0]

def investigate(identity: Identity, alert_id: str, *, max_steps: int = 3) -> dict:
    if max_steps < 1:
        raise ValueError("positive budget required")
    trace = []
    alert = get_alert(identity, alert_id)
    trace.append({"step": "get_alert", "status": "error" if "error" in alert else "ok"})
    if "error" in alert:
        return {"status": "not_found", "evidence": [], "trace": trace}
    if len(trace) >= max_steps:
        return {"status": "budget_exhausted", "evidence": [], "trace": trace}
    evidence = retrieve(identity, alert["service"] + " " + alert["symptom"])
    trace.append({"step": "retrieve", "status": "ok" if evidence else "empty"})
    if not evidence:
        return {"status": "needs_evidence", "evidence": [], "trace": trace}
    if len(trace) >= max_steps:
        return {"status": "budget_exhausted", "evidence": [], "trace": trace}
    trace.append({"step": "extract", "status": "ok"})
    return {
        "status": "ok", "alert_id": alert_id,
        "recommendation": evidence[0]["text"],
        "evidence": [{"id": d["id"], "source": d["source"]} for d in evidence],
        "limitations": ["Synthetic data", "Lexical retrieval", "Extractive output; no confirmed root cause", "No remediation tool"],
        "trace": trace,
    }

def dispatch(identity: Identity, tool: str, arguments: dict) -> dict:
    registry = {"get_alert": get_alert}
    if tool not in registry:
        raise PermissionError("tool not allowed")
    if set(arguments) != {"alert_id"} or not isinstance(arguments["alert_id"], str):
        raise ValueError("exactly one string alert_id required")
    return registry[tool](identity, **arguments)

if __name__ == "__main__":
    demo = Identity("demo-user", "alpha", frozenset({"reader"}))
    print(json.dumps(investigate(demo, "A1"), indent=2))
