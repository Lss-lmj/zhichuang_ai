#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
if [ -x .venv/bin/uvicorn ]; then
  .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi
