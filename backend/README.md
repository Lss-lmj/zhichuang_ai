# Backend

FastAPI backend for 智创Agent.

## Local Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

LangGraph or RAG work needs optional dependencies:

```bash
pip install -e ".[ai,rag,dev]"
```

## Database

Local development defaults to SQLite. Production should use PostgreSQL.

```bash
cd backend
alembic revision --autogenerate -m "init schema"
alembic upgrade head
```

## Module Boundaries

- `api/`: HTTP routes and request validation
- `services/`: deterministic business logic
- `ai/`: model providers, LangGraph graphs and graph nodes
- `rag/`: document parsing, chunking, retrieval and citation checking
- `db/`: database session and migration helpers
- `evaluation/`: prompt, RAG and graph evaluation assets
- `tasks/`: background task adapters for long-running agent jobs
- `models/`: database models
- `schemas/`: Pydantic API schemas

## Core Workflow

The first P0 workflow is course assignment code analysis:

```text
submission -> CodeAnalysisGraph -> assignment report -> teacher dashboard
```

Keep RBAC, persistence and report aggregation in services. Keep multi-step reasoning,
tool use and recoverable state transitions in LangGraph.
