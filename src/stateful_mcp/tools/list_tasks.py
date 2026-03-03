from stateful_mcp.main import mcp
from stateful_mcp.database import get_pool
from stateful_mcp.models import Task


@mcp.tool()
async def list_tasks(limit: int = 20, offset: int = 0) -> list[dict]:
    """List tasks with pagination."""
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100.")
    if offset < 0:
        raise ValueError("offset must be 0 or greater.")

    pool = get_pool()
    async with pool.connection() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM tasks
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )

    return [Task(**row).model_dump(mode="json") for row in rows]