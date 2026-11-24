"""Deterministic zero-cost generator for synthetic teaching issues."""


class FixtureGenerator:
    def generate(self, issue):
        return {
            "issue_id": issue.id,
            "summary": issue.title + ": " + issue.description[:120],
            "uncertainty": "Cause has not been verified",
            "sources": [issue.id],
        }
