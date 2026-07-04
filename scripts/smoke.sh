#!/usr/bin/env bash
set -euo pipefail

API_BASE="${1:-http://localhost:8000/api}"
WEB_BASE="${2:-http://localhost:5173}"

echo "Smoke check API: ${API_BASE}"
echo "Smoke check Web: ${WEB_BASE}"

if command -v python3.11 >/dev/null 2>&1; then
  python3.11 scripts/smoke.py "${API_BASE}" "${WEB_BASE}"
else
  python3 scripts/smoke.py "${API_BASE}" "${WEB_BASE}"
fi
