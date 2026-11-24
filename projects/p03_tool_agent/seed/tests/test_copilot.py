import unittest
from copilot import Identity, validate_alert, get_alert, retrieve, investigate, dispatch

class CopilotTests(unittest.TestCase):
    def setUp(self):
        self.alpha = Identity("u1", "alpha", frozenset({"reader"}))
        self.beta = Identity("u2", "beta", frozenset({"reader"}))
    def test_severity_boundary(self):
        self.assertEqual(validate_alert({"id":"A", "severity":4})["severity"], 4)
        for value in (0, 5, True, "3", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_alert({"id":"A", "severity":value})
    def test_missing_id(self):
        with self.assertRaises(ValueError): validate_alert({"severity":3})
    def test_tenant_denial_matches_absent(self):
        self.assertEqual(get_alert(self.alpha,"A2"),get_alert(self.alpha,"missing"))
    def test_retrieval_filters_before_output(self):
        self.assertEqual(retrieve(self.alpha,"database backup"), [])
        self.assertEqual(retrieve(self.beta,"database backup")[0]["id"], "runbook-2")
    def test_role_denied(self):
        identity = Identity("u", "alpha", frozenset())
        with self.assertRaises(PermissionError): retrieve(identity, "checkout")
    def test_citation_and_trace(self):
        result=investigate(self.alpha,"A1")
        self.assertEqual(result["status"],"ok")
        self.assertEqual(result["evidence"][0]["id"],"runbook-1")
        self.assertEqual(len(result["trace"]),3)
    def test_budget_stops_work(self):
        result=investigate(self.alpha,"A1",max_steps=1)
        self.assertEqual(result["status"],"budget_exhausted")
        self.assertEqual(len(result["trace"]),1)
    def test_forbidden_tool(self):
        with self.assertRaises(PermissionError): dispatch(self.alpha,"restart",{"alert_id":"A1"})
    def test_bad_arguments(self):
        with self.assertRaises(ValueError): dispatch(self.alpha,"get_alert",{"alert_id":"A1","tenant":"beta"})
    def test_unknown_alert(self):
        self.assertEqual(investigate(self.alpha,"missing")["status"],"not_found")
if __name__ == "__main__": unittest.main()
