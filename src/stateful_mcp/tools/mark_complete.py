from stateful_mcp.main import mcp
from stateful_mcp.database import get_pool
from stateful_mcp.models import Task
from uuid import UUID


@mcp.tool()
async def mark_complete(task_id: str) -> dict:
    """Mark a task as complete by its ID."""
    # Validate that task_id is a valid UUID before hitting the DB
    try:
        parsed_id = UUID(task_id)
    except ValueError:
        raise ValueError(f"'{task_id}' is not a valid task ID.")

    pool = get_pool()
    async with pool.connection() as conn:
        row = await conn.fetchrow(
            """
            UPDATE tasks
            SET completed = true, updated_at = now()
            WHERE id = $1
            RETURNING *
            """,
            parsed_id,
        )

    if row is None:
        raise ValueError(f"No task found with ID '{task_id}'.")

    return Task(**row).model_dump(mode="json")