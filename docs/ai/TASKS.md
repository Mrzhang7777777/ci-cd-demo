# 任务拆分

## 说明

以下任务按“小步可提交”原则拆分。每个任务都应尽量满足：

- 只解决一个明确问题
- 可独立验证
- 可独立提交
- 对后续任务依赖清晰

## T001 文档初始化

- 目标：建立项目说明、架构、任务、部署、CI/CD、决策记录等基础文档
- 产出：
  - `AGENTS.md`
  - `README.md`
  - `docs/ai/*`
- 验证：
  - 文档存在
  - 内容与项目目标一致

## T002 初始化前端工程

- 状态：已完成
- 目标：创建 Vue 3 + Vite + TypeScript 前端骨架
- 产出：
  - `frontend/` 基础目录
  - 最小首页
- 验证：
  - Win11 上执行 `npm install`
  - Win11 上执行 `npm run dev`
  - Win11 上执行 `npm run build`

## T003 初始化后端工程

- 状态：已完成
- 目标：创建 FastAPI + uv + Pydantic 后端骨架
- 产出：
  - `backend/` 基础目录
  - 应用入口
- 验证：
  - Win11 上执行 `uv sync --default-index https://pypi.org/simple`
  - Win11 上执行 `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
  - 访问 `http://127.0.0.1:8000/docs`

## T004 实现最小接口

- 状态：已完成
- 目标：实现 `GET /health` 与 `GET /api/hello`
- 产出：
  - 后端路由
  - 基础响应模型
- 验证：
  - Win11 上执行 `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`
  - 访问 `http://127.0.0.1:8000/health`
  - 访问 `http://127.0.0.1:8000/api/hello`

## T005 实现前端调用后端

- 状态：已完成
- 目标：前端页面请求 `/api/hello` 并展示结果
- 产出：
  - 最小页面交互
  - API 请求封装或最小调用逻辑
- 验证：
  - Win11 上先执行 `cd backend`
  - Win11 上执行 `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`
  - Win11 上再执行 `cd frontend`
  - Win11 上执行 `npm run dev`
  - 浏览器访问 Vite 开发地址并检查是否显示 `hello from backend`

## T006 编写后端 Dockerfile

- 状态：已创建，待 Docker Host 验证
- 目标：后端可独立构建容器镜像
- 产出：
  - `backend/Dockerfile`
  - 必要的构建忽略文件
- 验证：
  - 在 Ubuntu VM、GitHub Actions 或云服务器执行 `docker build -t ci-cd-demo-backend ./backend`
  - 在 Ubuntu VM、GitHub Actions 或云服务器执行 `docker run --rm -p 8000:8000 ci-cd-demo-backend`
  - 在 Docker Host 访问 `http://127.0.0.1:8000/docs`

## T007 编写前端 Dockerfile

- 状态：已创建，待 Docker Host 验证
- 目标：前端构建产物可由容器化 Nginx 提供服务
- 产出：
  - `frontend/Dockerfile`
  - 前端构建与静态发布方案
- 验证：
  - 在 Ubuntu VM、GitHub Actions 或云服务器执行 `docker build -t ci-cd-demo-frontend ./frontend`
  - 在 Ubuntu VM、GitHub Actions 或云服务器执行 `docker run --rm -p 8080:80 ci-cd-demo-frontend`
  - 在 Docker Host 访问 `http://127.0.0.1:8080`

## T008 编写 Nginx 配置

- 状态：已创建，待 Docker Host 验证
- 目标：Nginx 统一对外提供前端与 API 代理
- 产出：
  - Nginx 配置文件
- 验证：
  - 在 Docker Host 使用 `nginx/nginx.conf`
  - 未来 T009 的 Compose 中需要存在 service name: `backend`
  - `/` 可访问前端静态页面
  - `/api/hello` 可代理到 `backend:8000`
  - `/health` 可代理到 `backend:8000`

## T009 编写 Docker Host Compose 验证方案

- 状态：已完成
- 目标：在 Docker Host 上通过 Compose 启动完整链路
- 产出：
  - `docker-compose.yml` 或等效文件
  - Docker Host 验证说明
- 验证：
  - 在 Ubuntu VM 或云服务器执行 `docker compose up --build`
  - 已在 Ubuntu VM Docker Host 验证通过
  - 访问 `http://127.0.0.1:8080`
  - 访问 `http://127.0.0.1:8080/health`
  - 访问 `http://127.0.0.1:8080/api/hello`
  - 在 Ubuntu VM 或云服务器执行 `docker compose up` 后系统可用

## T010 补充环境变量设计

- 状态：已完成
- 目标：梳理前端、后端、部署所需最小环境变量
- 产出：
  - `.env.example`
  - 文档补充
- 验证：
  - 已提供根目录 `.env.example`
  - 当前最小 Demo 阶段不要求真实密钥
  - 后续 CI/CD 与部署变量命名已预留

## T011 增加本地验证脚本或说明

- 状态：已完成
- 目标：让后续每次修改都能在 Win11 或 Docker Host 上快速验证最小链路
- 产出：
  - 简单验证说明或脚本
- 验证：
  - 已新增 `docs/ai/VERIFY.md`
  - 已包含 Win11 开发验证命令
  - 已包含 Docker Host 验证命令

## T012 建立前端 CI

- 状态：已完成
- 目标：前端代码提交后可自动执行基础检查与构建
- 产出：
  - GitHub Actions workflow
- 验证：
  - 已创建 `.github/workflows/ci-frontend.yml`
  - `push` 和 `pull_request` 到 `main` 时可触发
  - 执行 `npm ci`
  - 执行 `npm run build`

## T013 建立后端 CI

- 状态：已完成
- 目标：后端代码提交后可自动执行基础检查与构建
- 产出：
  - GitHub Actions workflow
- 验证：
  - 已创建 `.github/workflows/ci-backend.yml`
  - `push` 和 `pull_request` 到 `main` 时可触发
  - 执行 `uv sync --frozen --no-dev`
  - 执行 `uv run python -c "from app.main import app; print(app.title)"`

## T014 建立镜像构建与推送流程

- 状态：已完成
- 目标：GitHub Actions 自动构建前后端镜像并推送仓库
- 产出：
  - 镜像构建 workflow
  - 标签策略初版
- 验证：
  - 已创建 `.github/workflows/docker-release.yml`
  - `push` 到 `main` 和 `workflow_dispatch` 时可触发
  - 自动构建并推送 backend/frontend 镜像到 GHCR
  - 使用 `latest` 与 `sha-<7位提交哈希>` 标签

## T015 准备服务器部署目录与 Compose

- 状态：已完成
- 目标：定义服务器部署所需的最小文件与目录结构
- 产出：
  - 服务器部署用 Compose 文件
  - 环境变量模板
- 验证：
  - 已创建 `compose.prod.yml`
  - 已创建 `deploy/.env.prod.example`
  - 服务器可执行 `docker compose -f compose.prod.yml pull`
  - 服务器可执行 `docker compose -f compose.prod.yml up -d`

## T016 建立自动部署流程

- 目标：GitHub Actions 在满足条件时触发部署
- 产出：
  - 部署 workflow
  - 服务器拉镜像与重启服务脚本或命令方案
- 验证：
  - 推送主分支后可自动更新服务器服务

## T017 编写回滚与故障处理文档

- 目标：补充最小运维手册
- 产出：
  - 常见故障排查步骤
  - 回滚思路
- 验证：
  - 文档可用于手工恢复服务

## T018 补充项目收尾文档

- 目标：整理学习成果与后续演进方向
- 产出：
  - README 和 AI 文档更新
- 验证：
  - 文档与实际仓库状态一致

## 推荐实施顺序

建议优先顺序：

1. T001
2. T002
3. T003
4. T004
5. T005
6. T006
7. T007
8. T008
9. T009
10. T010
11. T011
12. T012
13. T013
14. T014
15. T015
16. T016
17. T017
18. T018
