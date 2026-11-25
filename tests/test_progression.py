"""Checks for the newly taught project gates, including rejected outcomes."""
import tempfile
import unittest
from pathlib import Path
from projects.p01_llm_app.evaluate import evaluate as evaluate_p1
from projects.p01_llm_app.app import summarize
from projects.p02_rag.app import answer_with_generator, demo_store
from projects.p03_tool_agent.app import Agent, Approval
from projects.p03_tool_agent.state import SQLiteActionStore
from projects.p03_tool_agent.proposals import FixtureProposalSource
from projects.p05_multi_agent.evaluate import evaluate as evaluate_p5


class ProgressionTests(unittest.TestCase):
    def test_p1_ten_case_baseline_and_manual_review_boundary(self):
        report = evaluate_p1()
        self.assertEqual((report['passed'], report['total']), (10, 10))

        class Unsupported:
            def generate(self, issue):
                return {'issue_id': issue.id, 'summary': 'invented outage',
                        'uncertainty': 'unknown', 'sources': [issue.id]}
        report = evaluate_p1(Unsupported())
        self.assertEqual(report['passed'], 0)
        self.assertTrue(all(row['needs_human_support_review'] for row in report['rows']))

    def test_p1_rejects_new_causal_explanation(self):
        issue = {'id': 'INC-205', 'tenant': 'demo', 'title': 'Missing tile',
                 'description': 'The dashboard tile is absent. No cause has been confirmed.'}
        class Speculative:
            def generate(self, item):
                return {'issue_id': item.id, 'summary': 'The tile is absent',
                        'uncertainty': 'It may be due to a cache outage',
                        'sources': [item.id]}
        with self.assertRaisesRegex(ValueError, 'unsupported causal explanation'):
            summarize(issue, Speculative())

    def test_p2_generated_answer_requires_scoped_citation_and_quote(self):
        store = demo_store()

        class Generated:
            def __init__(self, citation='RB-LOGIN', quote='inspect gateway health'):
                self.citation, self.quote = citation, quote
            def generate_answer(self, question, passages):
                return {'answer': 'Inspect gateway health', 'citations': [self.citation],
                        'evidence_quote': self.quote, 'abstained': False}

        out = answer_with_generator(store, 'demo', 'login timeout', Generated())
        self.assertEqual(out['citations'], ['RB-LOGIN'])
        for bad in [Generated('RB-SEARCH'), Generated(quote='invented instruction')]:
            with self.assertRaises(ValueError):
                answer_with_generator(store, 'demo', 'login timeout', bad)
        self.assertTrue(answer_with_generator(store, 'other', 'login timeout', Generated())['abstained'])

    def test_p3_proposal_source_cannot_bypass_host_policy(self):
        self.assertEqual(Agent().investigate_with('demo','login timeout',FixtureProposalSource())['status'],'answered')
        class Malicious:
            def propose(self,tenant,question):
                return [{'tool':'shell','query':'ignore policy'}]
        self.assertEqual(Agent().investigate_with('demo','login timeout',Malicious())['status'],'denied')

    def test_p3_durable_approval_expiry_and_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'effects.db'
            now = [1000.0]
            approval = Approval('demo', 'acknowledge_alert', 'A-17', 'key-1')
            state = SQLiteActionStore(path, clock=lambda: now[0])
            with self.assertRaises(PermissionError):
                Agent(effect_store=state).simulate_action('demo', 'acknowledge_alert', 'A-17', 'key-1', approval)
            state.grant(approval, ttl_seconds=10)
            self.assertEqual(Agent(effect_store=state).simulate_action('demo', 'acknowledge_alert', 'A-17', 'key-1', approval)['status'], 'applied')
            restarted = Agent(effect_store=SQLiteActionStore(path, clock=lambda: now[0]))
            self.assertEqual(restarted.simulate_action('demo', 'acknowledge_alert', 'A-17', 'key-1', approval)['status'], 'already_applied')
            with self.assertRaises(PermissionError):
                restarted.simulate_action('demo', 'acknowledge_alert', 'A-18', 'key-1', Approval('demo', 'acknowledge_alert', 'A-18', 'key-1'))
            stale = Approval('demo', 'acknowledge_alert', 'A-18', 'key-2')
            state.grant(stale, ttl_seconds=10)
            now[0] += 10
            with self.assertRaises(PermissionError):
                restarted.simulate_action('demo', 'acknowledge_alert', 'A-18', 'key-2', stale)

    def test_p5_case_matched_comparison(self):
        report = evaluate_p5(repeats=2)
        self.assertEqual(report['cases'], 3)
        self.assertEqual(report['baseline_passed'], 3)
        self.assertEqual(report['workflow_passed'], 3)
        self.assertEqual(report['api_cost'], 0)
        self.assertGreater(report['rows'][0]['workflow_steps'], report['rows'][0]['baseline_steps'])
