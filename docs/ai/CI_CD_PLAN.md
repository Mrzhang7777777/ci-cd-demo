# CI/CD 阶段计划

## 1. 目标

建立一条从代码提交到镜像构建、再到服务器部署的最小自动化链路。

本项目的 CI/CD 目标不是追求复杂平台能力，而是先搭起一条可运行、可理解、可维护的基础流程。

## 2. 总体阶段

### 阶段一：Win11 开发与 Docker Host 容器化

目标：

- 前后端代码可运行
- Docker Host Compose 可联调
- 前后端镜像可构建

说明：

- Win11 开发机不要求安装 Docker
- Win11 负责代码编写、Codex 协作、git 提交与推送
- Ubuntu VM 可作为学习 Docker Compose 的验证环境
- 云服务器可作为后续部署验证环境

产出：

- 前后端基础工程
- Dockerfile
- Nginx 配置
- Docker Host Compose

### 阶段二：持续集成 CI

目标：

- 每次提交都能自动执行最小检查
- 保证主分支不会频繁进入不可构建状态

当前已完成的基础 CI：

- `ci-frontend`
  - 触发：`push` / `pull_request` 到 `main`
  - 环境：`Node 22`
  - 步骤：
    - `npm ci`
    - `npm run build`

- `ci-backend`
  - 触发：`push` / `pull_request` 到 `main`
  - 环境：`Python 3.12`
  - 步骤：
    - 安装 `uv`
    - `uv sync --frozen --no-dev`
    - `uv run python -c "from app.main import app; print(app.title)"`

建议步骤：

1. 拉取代码
2. 安装依赖
3. 执行前端构建检查
4. 执行后端基础检查
5. 可选执行简单测试

### 阶段三：镜像构建与推送

目标：

- 在主分支或版本标签触发时构建镜像
- 将镜像推送到镜像仓库

原则：

- 镜像构建优先由 GitHub Actions 完成
- 不把 Win11 开发机作为镜像构建必需节点

当前已完成的镜像发布流程：

- `docker-release`
  - 触发：`push` 到 `main`，或手动 `workflow_dispatch`
  - 权限：
    - `contents: read`
    - `packages: write`
  - 登录方式：
    - 使用 GitHub Actions 默认 `GITHUB_TOKEN` 登录 GHCR
  - 推送镜像：
    - `ghcr.io/${{ github.repository_owner }}/ci-cd-demo-backend`
    - `ghcr.io/${{ github.repository_owner }}/ci-cd-demo-frontend`
  - 标签策略：
    - `latest`
    - `sha-<7位提交哈希>`

当前已确认的结果：

- `docker-release` 已在 GitHub Actions 成功通过
- GHCR / GitHub Packages 已成功生成：
  - `ci-cd-demo-backend`
  - `ci-cd-demo-frontend`
- 当前基础 CI 状态：
  - `ci-frontend` 通过
  - `ci-backend` 通过
  - `docker-release` 通过

建议步骤：

1. 登录镜像仓库
2. 构建前端镜像
3. 构建后端镜像
4. 打上标签
5. 推送镜像

### 阶段四：持续部署 CD

目标：

- 服务器只拉取镜像并更新服务

当前已准备的部署基础文件：

- `compose.prod.yml`
- `deploy/.env.prod.example`
- `nginx/nginx.conf`

当前部署约束已经明确：

- 服务器不使用 `build`
- 服务器只拉 GHCR 镜像
- 服务器通过 `docker compose -f compose.prod.yml pull` 和 `up -d` 运行服务

当前已确认的手动部署结果：

- 已在 Ubuntu VM 上执行：
  - `docker compose -f compose.prod.yml pull`
  - `docker compose -f compose.prod.yml up -d`
- 已验证：
  - `http://127.0.0.1:8080/health` 返回 `{"status":"ok"}`
  - `http://127.0.0.1:8080/api/hello` 返回 `{"message":"hello from backend"}`
- 说明服务器侧“pull + up -d”手动验证已通过

建议步骤：

1. GitHub Actions 连接服务器
2. 服务器登录镜像仓库
3. 执行 `docker compose pull`
4. 执行 `docker compose up -d`
5. 执行简单健康检查

约束：

- 服务器不在部署时构建镜像
- 服务器只负责 `pull` 镜像与 `docker compose up -d`

## 3. Workflow 规划建议

建议至少包含以下 workflow：

### 3.1 `ci-frontend`

- 触发：PR、push
- 内容：
  - 安装前端依赖
  - 构建检查
  - 当前已建立

### 3.2 `ci-backend`

- 触发：PR、push
- 内容：
  - 安装后端依赖
  - 基础校验
  - 当前已建立

### 3.3 `docker-release`

- 触发：主分支 push，或版本 tag
- 内容：
  - 构建前后端镜像
  - 推送镜像
  - 当前已建立

### 3.4 `deploy-production`

- 触发：手动触发，或主分支镜像构建成功后触发
- 内容：
  - SSH 到服务器
  - 拉取镜像
  - 重启容器
  - 健康检查
  - 当前基础部署文件已准备，自动部署 workflow 仍未建立

## 4. 推荐推进顺序

不要一开始就写完整自动部署，建议按以下顺序推进：

1. 先保证 Win11 上代码开发顺畅，Docker Host 上容器链路可验证
2. 再加前后端基础 CI
3. 再加镜像构建与推送
4. 最后加服务器自动部署

## 5. Secrets 规划

后续大概率需要以下 GitHub Secrets：

- 镜像仓库用户名
- 镜像仓库令牌
- 服务器 SSH Host
- 服务器 SSH Port
- 服务器 SSH User
- 服务器 SSH Private Key
- 服务器部署目录或相关变量

## 6. 标签策略初步建议

可从简单策略开始：

- `latest`：主分支最新成功构建
- `sha-<commit>`：按提交哈希标记

后续再考虑：

- 语义化版本标签
- 环境标签

## 7. 风险点

- 前后端镜像职责划分不清
- Docker Host Compose 与服务器 Compose 漂移
- Secrets 配置不完整导致部署失败
- 服务器缺少 Docker 运行前置条件
- 镜像标签策略过早复杂化

## 8. 当前建议

当前阶段不急于追求：

- 多环境矩阵
- 自动回滚
- 高级发布策略

先把最小闭环跑通，再逐步增强。
