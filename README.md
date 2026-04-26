# ci-cd-demo

一个用于从零学习生产级 CI/CD、Docker 打包部署、GitHub Actions 自动部署，以及 Codex 协作方法的最小前后端 Demo。

## 学习目标

本项目不是为了堆业务功能，而是为了完整走通一条最小但接近生产实践的交付链路：

- 本地开发与联调
- Docker 镜像构建
- Docker Compose 编排
- Nginx 反向代理
- GitHub Actions 持续集成
- GitHub Actions 持续部署
- 云服务器拉镜像并启动容器

## 计划技术栈

- 前端：Vue 3 + Vite + TypeScript
- 后端：FastAPI + uv + Pydantic
- 部署：Docker + Docker Compose + Nginx
- CI/CD：GitHub Actions
- 服务器：2 核 2G 低配云服务器

## 最小目标

1. 本地可通过 `docker compose up` 启动完整系统
2. 前端页面可请求后端接口
3. 后端提供 `GET /health` 和 `GET /api/hello`
4. GitHub Actions 构建镜像并推送到镜像仓库
5. 云服务器只负责拉取镜像并执行 `docker compose up -d`

## 当前状态

当前仓库只完成文档初始化，尚未开始编写前端、后端和部署实现代码。

## 文档导航

- 项目简介：[docs/ai/PROJECT_BRIEF.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/PROJECT_BRIEF.md)
- 架构说明：[docs/ai/ARCHITECTURE.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/ARCHITECTURE.md)
- 技术栈说明：[docs/ai/TECH_STACK.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/TECH_STACK.md)
- API 约定：[docs/ai/API_SPEC.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/API_SPEC.md)
- 任务拆分：[docs/ai/TASKS.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/TASKS.md)
- 部署思路：[docs/ai/DEPLOYMENT.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/DEPLOYMENT.md)
- CI/CD 计划：[docs/ai/CI_CD_PLAN.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/CI_CD_PLAN.md)
- 决策记录：[docs/ai/DECISIONS.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docs/ai/DECISIONS.md)
- Codex 协作规则：[AGENTS.md](/D:/Users/RX/Desktop/Agent/ci-cd-demo/AGENTS.md)

## 建议学习顺序

1. 先阅读 `README.md`、`AGENTS.md`、`PROJECT_BRIEF.md`
2. 再阅读 `ARCHITECTURE.md`、`TECH_STACK.md`、`API_SPEC.md`
3. 然后按 `TASKS.md` 一项一项实现
4. 每完成一个任务，都同步更新相关文档

## 后续实施原则

- 先保证最小链路跑通
- 再补充工程化细节
- 每个任务独立提交
- 先本地验证，再推进 CI/CD
