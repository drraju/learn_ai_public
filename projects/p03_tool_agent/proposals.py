"""Provider-neutral proposal boundary for the bounded agent."""
from typing import Protocol


class ProposalSource(Protocol):
    def propose(self, tenant: str, question: str) -> list[dict]: ...


class FixtureProposalSource:
    def propose(self, tenant: str, question: str) -> list[dict]:
        return [{'tool': 'search', 'query': question}]
