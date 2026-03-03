from stateful_mcp.main import mcp
from stateful_mcp.database import get_pool
from stateful_mcp.models import Task, TaskCreate
from uuid import uuid4


@mcp.tool()
async def add_task(text: str) -> dict:
    """Add a new task to the to-do list."""
    # Validate input before hitting the DB
    task_in = TaskCreate(text=text)
    if not task_in.text.strip():
        raise ValueError("Task text cannot be empty or whitespace.")

    pool = get_pool()
    async with pool.connection() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO tasks (id, text, completed, created_at, updated_at)
            VALUES ($1, $2, false, now(), now())
            RETURNING *
            """,
            uuid4(),
            task_in.text.strip(),
        )

    return Task(**row).model_dump(mode="json")