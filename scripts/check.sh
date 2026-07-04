#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d backend ]; then
  if command -v pytest >/dev/null 2>&1; then
    (cd backend && pytest)
  else
    echo "pytest not found; skip backend tests"
    python3.11 -m compileall backend/app backend/alembic
  fi
fi

if [ -d frontend ] && [ -d frontend/node_modules ]; then
  (cd frontend && npm run build)
else
  echo "frontend/node_modules not found; skip frontend build"
fi
