from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from stateful_mcp.config import settings

_pool: AsyncConnectionPool | None = None

@asynccontextmanager
async def lifespan(_):
    global _pool

    connection_info = settings.database_url.replace("postgresql+psycopg://", "postgresql://")

    _pool = AsyncConnectionPool(
        conninfo=connection_info,
        min_size=1,
        max_size=5,
        open=False,
    )
    # --- STARTUP ---
    await _pool.open()
    try:
        yield # <-- server runs here
    finally:
    # --- SHUTDOWN ---
        await _pool.close()

def get_pool() -> AsyncConnectionPool:
    global _pool
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Server has not started yet")
    return _pool