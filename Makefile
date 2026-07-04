.PHONY: help init dev-backend dev-frontend test lint format check smoke docker-up docker-down

help:
	@echo "智创Agent development commands"
	@echo "  make init          Prepare local env files"
	@echo "  make dev-backend   Run FastAPI backend"
	@echo "  make dev-frontend  Run Vite frontend"
	@echo "  make test          Run backend tests"
	@echo "  make check         Run repository checks"
	@echo "  make smoke         Run deployed demo smoke checks"
	@echo "  make docker-up     Start compose services"
	@echo "  make docker-down   Stop compose services"

init:
	@test -f .env || cp .env.example .env
	@mkdir -p data/local/uploads data/local/chroma
	@echo "Local env prepared."

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest

lint:
	cd backend && ruff check app tests

format:
	cd backend && ruff format app tests

check:
	./scripts/check.sh

smoke:
	./scripts/smoke.sh

docker-up:
	docker compose up --build

docker-down:
	docker compose down
