import importlib.util,unittest
from projects.p04_mcp.app import lookup
class Tests(unittest.IsolatedAsyncioTestCase):
 async def test_denied_without_sdk(self):
  with self.assertRaises(PermissionError):await lookup('RB-LOGIN',allowed_tools=())
 @unittest.skipUnless(importlib.util.find_spec('mcp'),'optional mcp SDK not installed')
 async def test_in_process_exchange(self):
  result=await lookup('RB-LOGIN')
  self.assertEqual(result['id'],'RB-LOGIN')

class VersionTests(unittest.IsolatedAsyncioTestCase):
 @unittest.skipUnless(importlib.util.find_spec('mcp'),'optional mcp SDK not installed')
 async def test_mismatched_protocol_version_is_denied(self):
  with self.assertRaisesRegex(RuntimeError,'protocol version denied'):
   await lookup('RB-LOGIN',accepted_versions=('1900-01-01',))
