# Infrastructure

Deployment and operations assets live here.

Suggested structure:

```text
infra/
  nginx/
  docker/
  deploy/
  monitoring/
```

Current development entrypoint is `docker-compose.yml` at repository root.

Public Demo target:

- FastAPI backend container.
- Static frontend build.
- PostgreSQL + pgvector.
- Redis.
- Demo accounts and sample course data.

See also:

- `docs/公网Demo部署.md`
- `docs/演示脚本.md`
