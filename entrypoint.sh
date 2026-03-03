#!/bin/sh
set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting MCP server..."
exec uv run python -m stateful_mcp.main
