# 决策记录

## 说明

本文件记录当前已经做出的关键技术决策。后续如有变化，应追加记录，不建议直接抹掉历史判断。

## D001 使用单仓库组织项目

- 状态：已决定
- 决策：
  - 前端、后端、部署与文档放在同一个仓库中
- 原因：
  - 适合学习整体交付链路
  - 降低多仓库协作复杂度

## D002 以最小可部署 Demo 为第一阶段目标

- 状态：已决定
- 决策：
  - 第一阶段只实现最小页面和最小 API
- 原因：
  - 当前重点是 CI/CD 与部署，不是业务复杂度

## D003 前端技术栈采用 Vue 3 + Vite + TypeScript

- 状态：已决定
- 原因：
  - 工具链成熟
  - 学习路径清晰
  - 适合作为最小前端模板

## D004 后端技术栈采用 FastAPI + uv + Pydantic

- 状态：已决定
- 原因：
  - 轻量
  - 现代 Python 工程化体验较好
  - 易于快速提供 API

## D005 部署方式采用 Docker + Docker Compose + Nginx

- 状态：已决定
- 原因：
  - 适合单机部署
  - 足以承载本项目目标
  - 能覆盖最核心的容器化与反向代理实践

## D006 CI/CD 工具采用 GitHub Actions

- 状态：已决定
- 原因：
  - 与 GitHub 仓库结合紧密
  - 足以实现本项目自动化需求

## D007 服务器不负责构建镜像

- 状态：已决定
- 决策：
  - 服务器只拉镜像并运行容器
- 原因：
  - 更接近生产职责分离
  - 更适合低配服务器
  - 部署稳定性更高

## D008 后端最小接口为 GET /health 和 GET /api/hello

- 状态：已决定
- 原因：
  - 足以验证服务可用性
  - 足以验证前后端联通

## D009 所有文档统一使用中文

- 状态：已决定
- 原因：
  - 当前项目目标是用于中文学习与协作

## D010 任务按小步独立提交推进

- 状态：已决定
- 原因：
  - 有利于学习过程清晰
  - 降低一次性改动风险
  - 便于回顾每一步工程演进

## D011 当前阶段先建文档，不写业务代码

- 状态：已决定
- 原因：
  - 先统一方向，避免后续返工

## D012 镜像仓库优先考虑 GitHub Container Registry

- 状态：倾向采用
- 原因：
  - 与 GitHub Actions 集成顺畅
  - 学习路径更统一
- 备注：
  - 后续如因可见性、配额或使用体验需要，可切换为 Docker Hub

## D013 Docker 构建与运行验证不在 Win11 开发机完成

- 状态：已决定
- 决策：
  - 由于 Win11 开发机不安装 Docker，Docker 构建与运行验证迁移到 Ubuntu VM / GitHub Actions / 云服务器完成
- 原因：
  - 保持开发机环境简洁
  - 更符合当前实际开发条件
  - 有利于明确开发、构建、运行三类职责边界

## D014 前端初始化阶段不引入额外状态管理与路由库

- 状态：已决定
- 决策：
  - T002 阶段只初始化 Vue 3 + Vite + TypeScript 最小骨架
  - 暂不引入 Pinia、Axios、Vue Router
- 原因：
  - 当前任务目标只是建立最小可启动前端
  - 过早引入额外依赖会增加学习噪音
  - 后续在 T005 或更后续任务中按需要再引入更合理

## D015 后端初始化阶段只保留 FastAPI 应用入口

- 状态：已决定
- 决策：
  - T003 阶段只创建 FastAPI 应用对象和基础项目结构
  - 暂不接入数据库、配置系统、业务路由和额外分层
- 原因：
  - 当前任务目标只是建立最小可启动后端骨架
  - `/health` 和 `/api/hello` 已明确留到 T004
  - 先把依赖管理、启动方式和 OpenAPI 文档跑通更符合当前阶段目标

## D016 前端联调阶段先使用原生 fetch 和固定后端地址

- 状态：已决定
- 决策：
  - T005 阶段使用浏览器原生 `fetch`
  - 暂不引入 Axios
  - 暂时固定请求地址为 `http://127.0.0.1:8000`
- 原因：
  - 当前目标只是建立最小前后端联调路径
  - 减少依赖和封装层，便于理解请求链路
  - 后续再根据部署与代理方案调整为环境变量或相对路径

## D017 开发环境允许 Vite 本地地址跨域访问后端

- 状态：已决定
- 决策：
  - 为开发联调在 FastAPI 中加入 `CORSMiddleware`
  - 只允许 `http://127.0.0.1:5173` 和 `http://localhost:5173`
  - 不使用 `allow_origins=["*"]`
- 原因：
  - 解决 Win11 本地 Vite 开发服务访问后端时的浏览器 CORS 限制
  - 只开放明确的开发地址，避免过宽配置
  - 该配置属于开发环境联调用途，不代表最终生产部署策略

## D018 后端镜像内使用 uv 安装依赖，运行时直接启动 uvicorn

- 状态：已决定
- 决策：
  - T006 阶段在 `backend/Dockerfile` 中使用 `uv sync` 安装依赖
  - `uv` 二进制改为从 `ghcr.io/astral-sh/uv` 官方镜像复制，不再通过 `pip install uv` 安装
  - 运行时默认命令为 `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- 原因：
  - 保持与本项目的 `uv` 依赖管理方式一致
  - 避免 Docker 构建阶段卡在通过 PyPI 慢速下载 `uv`
  - 运行命令直接、清晰，便于后续接入 Compose 和容器健康检查
  - 当前后端是最小应用，暂不需要更复杂的进程管理

## D019 前端镜像采用多阶段构建并由 Nginx 提供静态文件

- 状态：已决定
- 决策：
  - T007 阶段使用 Node 镜像构建 Vite 产物
  - 第二阶段使用 Nginx 镜像提供 `dist/` 静态文件
  - 当前不在前端镜像中加入统一反代配置
- 原因：
  - 多阶段构建可以把运行镜像保持得更小、更干净
  - Nginx 提供静态资源是后续部署链路的目标形态
  - 当前任务只验证前端静态发布，反代和 API 路径整理留到后续任务处理

## D020 Nginx 反代配置依赖未来 Compose 中的 backend service name

- 状态：已决定
- 决策：
  - T008 阶段创建 `nginx/nginx.conf`
  - 其中 `/api/` 和 `/health` 代理目标写为 `http://backend:8000`
  - 使用 `try_files $uri $uri/ /index.html` 支持前端静态路由刷新
- 原因：
  - `backend` 是未来 Docker Compose 中最稳定的服务发现方式
  - 当前阶段先固化网关路径和服务命名约定，便于 T009 直接接线
  - 刷新回退逻辑是前端静态站点的基础能力，即使当前页面尚未使用路由，也先作为标准配置保留

## D021 T009 阶段通过 Compose 挂载 nginx 配置，并采用 Nginx 统一入口

- 状态：已决定
- 决策：
  - T009 的 `docker-compose.yml` 使用 `frontend` 和 `backend` 两个服务
  - `frontend` 服务挂载 `./nginx/nginx.conf` 到容器内 `/etc/nginx/nginx.conf`
  - 前端请求改为相对路径 `/api/hello`
  - `backend` 不再暴露宿主机 `8000:8000`
- 原因：
  - 这样可以把 Docker Compose 联调链路统一收口到 Nginx 单入口
  - 容器间通信通过 `backend` service name 完成，更接近后续部署形态
  - 避免为了前端固定地址而额外暴露 backend 宿主机端口

## D022 T009 已在 Ubuntu VM Docker Host 验证通过

- 状态：已记录
- 记录：
  - 已执行 `docker compose up --build`
  - `http://127.0.0.1:8080/api/hello` 返回 `{"message":"hello from backend"}`
  - `http://127.0.0.1:8080/health` 返回 `{"status":"ok"}`
- 说明：
  - 当前最小 Docker Compose 联调链路已在 Ubuntu VM Docker Host 验证通过

## D023 当前阶段环境变量只做占位设计，不引入真实密钥

- 状态：已决定
- 决策：
  - T010 阶段创建根目录 `.env.example`
  - 只预留后续 CI/CD 与部署所需变量名
  - 当前最小 Demo 不写入真实密钥和真实服务器信息
- 原因：
  - 当前阶段重点是先把变量边界和命名约定定下来
  - 避免在文档阶段混入敏感信息
  - 便于后续 GitHub Actions 与服务器部署阶段直接接入

## D024 先建立基础 CI，再进入镜像构建与部署自动化

- 状态：已决定
- 决策：
  - T012 阶段先建立前端基础 CI
  - T013 阶段先建立后端基础 CI
  - 当前 CI 只做依赖安装、构建与最小导入校验
- 原因：
  - 先保证主分支的基础可构建性
  - 避免过早把镜像构建和服务器部署耦合进同一个阶段
  - 有利于把 CI 问题和 CD 问题分开定位

## D025 镜像发布使用 GHCR，并采用 latest + 短哈希标签

- 状态：已决定
- 决策：
  - T014 阶段使用 GitHub Actions 默认 `GITHUB_TOKEN` 登录 GHCR
  - 推送镜像到：
    - `ghcr.io/mrzhang7777777/ci-cd-demo-backend`
    - `ghcr.io/mrzhang7777777/ci-cd-demo-frontend`
  - 标签策略采用：
    - `latest`
    - `sha-<7位提交哈希>`
- 原因：
  - GHCR 与 GitHub Actions 集成最直接
  - `latest` 适合跟踪主分支最新成功构建
  - 短哈希标签便于回溯到具体提交版本

## D026 GHCR 镜像名中的 namespace 必须使用小写

- 状态：已决定
- 决策：
  - `docker-release` workflow 中的 GHCR namespace 固定为小写 `mrzhang7777777`
  - 不直接使用可能包含大写字母的 `github.repository_owner`
- 原因：
  - Docker / GHCR 镜像名要求小写
  - 避免因仓库所有者名称大小写导致 workflow 推送失败

## D027 基础 CI 与 GHCR 镜像发布已验证通过

- 状态：已记录
- 记录：
  - `ci-frontend` 已通过
  - `ci-backend` 已通过
  - `docker-release` 已通过
  - GitHub Packages 已生成：
    - `ci-cd-demo-backend`
    - `ci-cd-demo-frontend`
- 说明：
  - 当前项目已经完成“基础 CI 校验 + GHCR 镜像构建与推送”的最小闭环

## D028 服务器部署阶段使用独立的 compose.prod.yml，只通过拉镜像运行

- 状态：已决定
- 决策：
  - T015 阶段创建 `compose.prod.yml`
  - 服务器部署使用 GHCR 镜像：
    - `ghcr.io/mrzhang7777777/ci-cd-demo-backend:latest`
    - `ghcr.io/mrzhang7777777/ci-cd-demo-frontend:latest`
  - 服务器部署不使用 `build`
  - `backend` 只在 Compose 网络内部监听 `8000`
  - `frontend` 继续挂载 `./nginx/nginx.conf:/etc/nginx/nginx.conf:ro`
- 原因：
  - 保持服务器职责最小化
  - 与“服务器只负责 pull 镜像和启动容器”的目标一致
  - 避免把源码构建压力放到低配服务器上

## D029 T015 已在 Ubuntu VM 上手动验证通过

- 状态：已记录
- 记录：
  - 已执行 `docker compose -f compose.prod.yml pull`
  - 已执行 `docker compose -f compose.prod.yml up -d`
  - `/health` 返回 `{"status":"ok"}`
  - `/api/hello` 返回 `{"message":"hello from backend"}`
- 说明：
  - 当前服务器侧生产 Compose 手动部署链路已验证通过

## D030 T016 自动部署阶段先使用 Ubuntu VM 作为学习环境

- 状态：已决定
- 决策：
  - `deploy-production` workflow 当前先连接 Ubuntu VM 进行自动部署验证
  - 远程部署流程保持为 `git pull + docker compose pull + docker compose up -d + 健康检查`
- 原因：
  - 先在可控学习环境验证 GitHub Actions 到服务器的完整自动部署链路
  - 避免一开始就把自动部署直接压到正式云服务器环境
  - 与当前“服务器不构建镜像，只负责拉镜像和运行容器”的目标一致
