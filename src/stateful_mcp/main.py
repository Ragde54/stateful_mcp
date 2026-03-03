from mcp.server.fastmcp import FastMCP
from stateful_mcp.database import lifespan
from stateful_mcp.config import settings

mcp = FastMCP(
    "stateful-mcp",
    lifespan=lifespan,
    host=settings.server_host,
    port=settings.server_port,
)

import stateful_mcp.tools.add_task
import stateful_mcp.tools.list_tasks
import stateful_mcp.tools.mark_complete

if __name__ == "__main__":
    mcp.run(transport="sse")