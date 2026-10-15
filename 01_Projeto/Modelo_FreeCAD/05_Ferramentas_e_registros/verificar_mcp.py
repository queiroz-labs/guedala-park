"""Exercise the installed STDIO MCP and its live FreeCAD socket, without the UI."""
import asyncio
import json
import os
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    base=Path(os.environ['LOCALAPPDATA'])/'Programs'/'FreeCAD-MCP'
    params=StdioServerParameters(command=str(base/'.venv'/'Scripts'/'python.exe'),args=[str(base/'working_bridge.py')])
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            if len(sys.argv)>1:
                code=Path(sys.argv[1]).read_text(encoding='utf-8')
            else:
                code='result = {"version": FreeCAD.Version()[:3], "documents": list(FreeCAD.listDocuments()), "active": FreeCAD.ActiveDocument.Name if FreeCAD.ActiveDocument else None}'
            listing=await session.list_tools()
            connection=await session.call_tool('check_freecad_connection',{})
            answer=await session.call_tool('execute_python',{'code':code})
            print(json.dumps({'tools':[t.name for t in listing.tools],
                'connection':[x.text for x in connection.content if hasattr(x,'text')],
                'answer':[x.text for x in answer.content if hasattr(x,'text')]},ensure_ascii=False))

asyncio.run(main())
