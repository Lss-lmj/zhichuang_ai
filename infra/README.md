# 部署资产

本目录用于放置部署相关配置和说明。

Suggested structure:

```text
infra/
  nginx/
  docker/
  deploy/
  monitoring/
```

当前开发入口为仓库根目录的 `docker-compose.yml`。

公网访问环境目标：

- FastAPI backend container.
- Static frontend build.
- PostgreSQL + pgvector.
- Redis.
- 学校账号和示例课程数据。

See also:

- `docs/公网访问环境部署.md`
- `docs/操作说明与展示脚本.md`
