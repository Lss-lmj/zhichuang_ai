# 公网 Demo 部署说明

目标：部署一个可访问的智创Agent 演示环境，用于展示学生报告、教师看板、成长路径、知识库问答、知识库管理和演示账号切换。

## 1. 演示入口

演示账号：

| 角色 | 账号 | 默认视图 |
| --- | --- | --- |
| 学生 | 林一舟 | 成长路径 |
| 教师 | 周老师 | 教师看板 |
| 管理员 | 平台管理员 | 知识库管理 |

演示主线：

1. 教师账号查看课程作业学情诊断。
2. 查看某个学生作业分析报告。
3. 切换学生账号查看成长路径。
4. 在知识库问答中提问“如何准备算法竞赛？”。
5. 切换管理员账号查看知识库资料清单和检索命中。

## 2. 本地 Docker Compose

准备环境：

```bash
make init
docker compose up --build
```

访问：

- 前端：`http://localhost:5173`
- 后端：`http://localhost:8000/api/health`

## 3. 服务器部署建议

建议配置：

- 2 核 CPU。
- 4GB 内存。
- 40GB 磁盘。
- Docker 和 Docker Compose。

部署流程：

```bash
git pull
cp .env.example .env
docker compose up -d --build
```

公网反向代理：

- 前端域名指向 `frontend:80`。
- 后端 API 域名或路径指向 `backend:8000`。
- 如果前端和后端不同域名，更新 `VITE_API_BASE_URL`。

学校身份接入：

- 在 `.env` 中设置 `SCHOOL_IDENTITY_SHARED_SECRET`，部署时不要使用示例值。
- 学校统一身份系统完成登录后，由受信任网关调用 `POST /api/auth/school-session`。
- 网关至少传入 `user_id`、`student_no`、`teacher_no` 或 `email` 中的一个字段，并在请求头携带 `X-School-Identity-Secret`。
- 平台只把身份断言映射到已导入的 SQLite 用户，课程、班级和本人访问范围仍由教学基础数据决定。

## 4. Smoke Check

```bash
./scripts/smoke.sh http://localhost:8000/api http://localhost:5173
```

检查项：

- 后端健康检查。
- 演示账号接口。
- 作业教师看板、教学改进建议和学生报告接口。
- 学生成长画像、学习计划、竞赛推荐、组队推荐。
- 教师竞赛梯队筛选和学生越权拦截。
- 任务保存与定期复盘。
- 知识库资料新增、资料清单和检索接口。
- Agent 问答引用来源。
- 评测看板、课程列表。
- 本地学校账号会话和学校身份网关会话。
- 前端首页可访问。

## 5. 当前 Demo 范围

当前版本使用演示数据和内置知识库资料，覆盖：

- 课程作业代码分析报告。
- 教师作业学情看板。
- 学生成长路径。
- 竞赛推荐和组队推荐。
- RAG 知识库问答。
- 知识库资料管理。
- 演示账号和角色切换。
