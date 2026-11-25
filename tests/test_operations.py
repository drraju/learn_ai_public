"""P6 local persistence, request replay, scope, metrics and retention checks."""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from projects.p03_tool_agent.app import Agent
from projects.p06_capstone.app import make_handler
from projects.p06_capstone.operations import OperationsStore


class OperationsTests(unittest.TestCase):
    def test_persistent_ledger_conflict_metrics_and_retention(self):
        with tempfile.TemporaryDirectory() as tmp:
            now = [1000.0]
            path = Path(tmp) / 'state.db'
            store = OperationsStore(path, clock=lambda: now[0])
            result = {'status': 'answered'}
            self.assertEqual(store.record('r1', 'demo', 'login timeout', result, 2.5), result)
            restarted = OperationsStore(path, clock=lambda: now[0])
            self.assertEqual(restarted.existing('r1', 'demo', 'login timeout'), result)
            with self.assertRaises(ValueError):
                restarted.record('r1', 'demo', 'different question', result, 1)
            self.assertEqual(restarted.metrics()['answered'], 1)
            now[0] += 86401
            self.assertEqual(restarted.purge_older_than(86400), 1)
            self.assertEqual(restarted.metrics()['requests'], 0)

    def test_http_request_replay_and_authenticated_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = OperationsStore(Path(tmp) / 'state.db')
            server = ThreadingHTTPServer(('127.0.0.1', 0),
                                         make_handler(Agent(), 'test-secret-123', operations=store))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            root = f'http://127.0.0.1:{server.server_port}'
            headers = {'Authorization': 'Bearer test-secret-123', 'X-Request-ID': 'request-1'}
            try:
                body = json.dumps({'tenant': 'demo', 'question': 'login timeout'}).encode()
                def post(payload, request_headers=headers):
                    return urllib.request.urlopen(urllib.request.Request(root + '/investigate', payload,
                                                                         request_headers), timeout=2)
                with post(body) as response:
                    first = json.load(response)
                with post(body) as response:
                    self.assertEqual(json.load(response), first)
                with self.assertRaises(urllib.error.HTTPError) as conflict:
                    post(json.dumps({'tenant': 'demo', 'question': 'alert latency'}).encode())
                self.assertEqual(conflict.exception.code, 409)
                with self.assertRaises(urllib.error.HTTPError) as denied:
                    urllib.request.urlopen(root + '/metrics', timeout=2)
                self.assertEqual(denied.exception.code, 401)
                with urllib.request.urlopen(urllib.request.Request(root + '/metrics', headers=headers), timeout=2) as response:
                    self.assertEqual(json.load(response)['requests'], 1)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)
