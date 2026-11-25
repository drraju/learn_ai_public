"""P4: optional real SDK in-process MCP exchange with host allowlist."""
from dataclasses import dataclass
from shared.core import load

@dataclass
class LookupResult:
    id: str
    text: str

def build_server():
    from mcp.server import MCPServer
    server=MCPServer('Synthetic runbook lookup')
    @server.tool()
    def lookup_runbook(doc_id: str) -> LookupResult:
        """Look up one synthetic demo runbook by exact ID."""
        if not isinstance(doc_id,str) or len(doc_id)>80: raise ValueError('invalid ID')
        for row in load('runbooks.json'):
            if row['tenant']=='demo' and row['id']==doc_id:
                return LookupResult(row['id'],row['text'])
        raise ValueError('not found')
    return server

async def lookup(doc_id,allowed_tools=('lookup_runbook',),accepted_versions=('2026-07-28',)):
    if 'lookup_runbook' not in allowed_tools: raise PermissionError('host denied tool')
    if not isinstance(doc_id,str) or not doc_id.startswith('RB-') or len(doc_id)>80:
        raise ValueError('invalid ID')
    from mcp import Client
    denied_version=None
    async with Client(build_server(),raise_exceptions=True) as client:
        if client.protocol_version not in accepted_versions:
            denied_version=client.protocol_version
        else:
            tools=await client.list_tools()
            if 'lookup_runbook' not in [x.name for x in tools.tools]:
                raise RuntimeError('capability unavailable')
            result=await client.call_tool('lookup_runbook',{'doc_id':doc_id})
            return result.structured_content
    raise RuntimeError('protocol version denied: '+denied_version)
