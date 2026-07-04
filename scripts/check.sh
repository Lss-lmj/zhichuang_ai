#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d backend ]; then
  (cd backend && pytest)
fi

if [ -d frontend ] && [ -d frontend/node_modules ]; then
  (cd frontend && npm run build)
else
  echo "frontend/node_modules not found; skip frontend build"
fi
