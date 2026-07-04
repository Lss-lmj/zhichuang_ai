#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d backend ]; then
  if [ -x backend/.venv/bin/python ]; then
    (cd backend && .venv/bin/python -m pytest)
  elif command -v pytest >/dev/null 2>&1; then
    (cd backend && pytest)
  elif python3.11 -m pytest --version >/dev/null 2>&1; then
    (cd backend && python3.11 -m pytest)
  else
    echo "pytest not found; skip backend tests"
    python3.11 -m compileall backend/app backend/alembic
  fi

  if [ -x backend/.venv/bin/ruff ]; then
    (cd backend && .venv/bin/ruff check app tests)
  elif command -v ruff >/dev/null 2>&1; then
    (cd backend && ruff check app tests)
  else
    echo "ruff not found; skip backend lint"
  fi
fi

if [ -d frontend ] && [ -d frontend/node_modules ]; then
  (cd frontend && npm run build)
else
  echo "frontend/node_modules not found; skip frontend build"
fi
