#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-0.0.0.0}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
VITE_API_BASE_URL="${VITE_API_BASE_URL:-http://localhost:${BACKEND_PORT}/api}"
CORS_ORIGINS="${CORS_ORIGINS:-[\"http://localhost:${FRONTEND_PORT}\",\"http://127.0.0.1:${FRONTEND_PORT}\"]}"

cd "$ROOT_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
fi

mkdir -p data/local/uploads data/local/chroma

if [ ! -x backend/.venv/bin/python ]; then
  python3.11 -m venv backend/.venv
fi

if ! backend/.venv/bin/python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
  backend/.venv/bin/python -m pip install -e "backend[dev]"
fi

if [ ! -d frontend/node_modules ]; then
  if [ -f frontend/package-lock.json ]; then
    (cd frontend && npm ci)
  else
    (cd frontend && npm install)
  fi
fi

cleanup() {
  if [ -n "${BACKEND_PID:-}" ] && kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
  if [ -n "${FRONTEND_PID:-}" ] && kill -0 "$FRONTEND_PID" >/dev/null 2>&1; then
    kill "$FRONTEND_PID" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT
trap 'cleanup; exit 0' INT TERM

echo "Starting backend:  http://localhost:${BACKEND_PORT}/api"
PYTHONPATH="$ROOT_DIR/backend" CORS_ORIGINS="$CORS_ORIGINS" backend/.venv/bin/python -m uvicorn app.main:app \
  --reload \
  --reload-dir "$ROOT_DIR/backend/app" \
  --host "$BACKEND_HOST" \
  --port "$BACKEND_PORT" &
BACKEND_PID=$!

echo "Starting frontend: http://localhost:${FRONTEND_PORT}"
(
  cd frontend
  VITE_API_BASE_URL="$VITE_API_BASE_URL" ./node_modules/.bin/vite \
    --host "$FRONTEND_HOST" \
    --port "$FRONTEND_PORT"
) &
FRONTEND_PID=$!

echo
echo "智创Agent local dev is starting."
echo "Backend API:  http://localhost:${BACKEND_PORT}/api"
echo "Frontend:     http://localhost:${FRONTEND_PORT}"
echo "Press Ctrl+C to stop both services."
echo

wait "$BACKEND_PID" "$FRONTEND_PID"
