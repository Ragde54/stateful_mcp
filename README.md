# stateful-mcp

A **production-ready blueprint** for a stateful [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server. It demonstrates how to wire up a persistent database (PostgreSQL), expose tools over SSE/HTTP, containerise everything with Docker Compose, and connect it to Claude Desktop — all with minimal boilerplate.

---

## ✨ Features

- **Stateful tools** — MCP tools backed by a real PostgreSQL database (not in-memory)
- **SSE / HTTP transport** — exposes the MCP server over `http://host:port/sse`, ready for remote clients
- **Docker Compose** — one command spins up Postgres + the MCP server, with a health-checked dependency
- **Schema migrations** — [Alembic](https://alembic.sqlalchemy.org) manages the DB schema; no manual SQL needed
- **Async connection pooling** — uses `psycopg-pool` for efficient, non-blocking database access
- **Pydantic settings** — all configuration is validated and loaded from environment variables / `.env`
- **Claude Desktop compatible** — works out of the box with the remote MCP URL config
- **`uv` project** — fast dependency management and reproducible builds via `uv.lock`

---

## 🗂 Project Structure

```
stateful_mcp/
├── src/stateful_mcp/
│   ├── main.py          # FastMCP server entry point
│   ├── config.py        # Pydantic settings (env vars)
│   ├── database.py      # Async connection pool + lifespan
│   ├── models.py        # Pydantic models (Task, TaskCreate)
│   └── tools/
│       ├── add_task.py       # Tool: add a task
│       ├── list_tasks.py     # Tool: list tasks (paginated)
│       └── mark_complete.py  # Tool: mark a task as done
├── alembic/
│   ├── env.py                # Alembic config (reads from settings)
│   └── versions/             # Migration scripts
├── alembic.ini
├── compose.yaml         # Docker Compose (db + app)
├── Dockerfile
├── entrypoint.sh        # Runs migrations then starts the server
├── pyproject.toml
├── .env.example         # Copy to .env and fill in
└── uv.lock
```

---

## 🚀 Quick Start

### 1. Clone & configure

```bash
git clone <repo-url>
cd stateful_mcp

cp .env.example .env
# Edit .env with your preferred credentials
```

Your `.env` should look like:

```env
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=todo_db
DATABASE_URL=postgresql+psycopg://todo_user:changeme@localhost:5432/todo_db
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
APP_ENV=dev
LOG_LEVEL=INFO
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

This starts:
- `db` — Postgres 16 with a health check
- `app` — the MCP server (waits for `db` to be healthy)

The server is available at **`http://localhost:8000/sse`**.

### 3. Migrations run automatically

The container's entrypoint runs `alembic upgrade head` before starting the server — no manual step needed. On every `docker compose up`, the schema is always in sync.

---

## 🖥 Connect to Claude Desktop

Add the following to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "todo": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

Restart Claude Desktop and the **todo** server will appear in your tools list.

---

## 🛠 Local Development (without Docker)

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
# Install dependencies
uv sync

# Start a local Postgres instance (e.g. via Homebrew or Docker):
docker run -d \
  --name mcp-pg \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_PASSWORD=changeme \
  -e POSTGRES_DB=todo_db \
  -p 5432:5432 \
  postgres:16

# Run migrations
uv run alembic upgrade head

# Start the MCP server
uv run python -m stateful_mcp.main
```

---

## ⚡ stdio Transport (Claude Desktop, local)

The server currently runs in **SSE mode** by default (`mcp.run(transport="sse")`). SSE requires a running server process and is the recommended approach for production and Docker.

If you want to run it over **stdio** (e.g. for direct Claude Desktop integration without a separate server process), change the transport in `main.py`:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")  # changed from "sse"
```

Then configure Claude Desktop to launch it directly:

```json
{
  "mcpServers": {
    "todo": {
      "command": "uv",
      "args": ["run", "python", "-m", "stateful_mcp.main"],
      "cwd": "/absolute/path/to/stateful_mcp"
    }
  }
}
```

> **Note:** stdio mode still requires a running Postgres instance. Docker Compose is **not** compatible with stdio transport since Claude Desktop spawns the process itself — use local Postgres instead.

---

## 🔧 Available MCP Tools

| Tool | Description |
|------|-------------|
| `add_task(text)` | Add a new task to the to-do list |
| `list_tasks(limit, offset)` | List tasks with pagination (default: 20 per page) |
| `mark_complete(task_id)` | Mark a task as complete by its UUID |
