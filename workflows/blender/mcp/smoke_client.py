"""Exercise the full stdio MCP path against a running Blender bridge."""

from __future__ import annotations

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def smoke() -> dict[str, object]:
    server = StdioServerParameters(command=sys.executable, args=["-m", "blmcp"])
    async with stdio_client(server) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = sorted(tool.name for tool in tools.tools)
            path_info = await session.call_tool(
                "get_blendfile_summary_path_info", arguments={}
            )
            return {
                "tool_count": len(tool_names),
                "tools": tool_names,
                "path_info": path_info.model_dump(mode="json"),
            }


def main() -> int:
    print(json.dumps(asyncio.run(smoke()), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
