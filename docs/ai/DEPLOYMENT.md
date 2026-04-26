# 部署说明

## 1. 目标

本项目部署设计要满足两个核心要求：

1. 在 Docker Host 上可以用 Docker Compose 一键启动最小完整链路
2. 服务器只负责拉镜像和启动容器，不负责源码构建

## 2. 开发机与 Docker Host 分工

### 2.1 Win11 开发机角色

Win11 物理机主要用于：

- Codex 协作开发
- 本地代码编辑
- git 提交与推送
- 运行不依赖 Docker 的开发验证

约束：

- Win11 不要求安装 Docker
- Win11 不承担 Docker 构建与运行验证
- 除非用户明确说明已安装 Docker，否则不应要求在 Win11 上执行 `docker`、`docker compose`、`docker build` 相关命令
- 涉及 Docker 的验证命令，默认应标注为在 Ubuntu VM、GitHub Actions 或云服务器执行

### 2.2 Docker Host 角色

Docker Host 可以是：

- Ubuntu VM
- 云服务器

Docker Host 主要用于：

- 验证 Dockerfile 是否可构建
- 验证 Compose 编排是否正确
- 验证前后端容器联通
- 验证 Nginx 代理链路

后端 Dockerfile 单独验证命令应默认在 Docker Host 执行，例如：

- `docker build -t ci-cd-demo-backend ./backend`
- `docker run --rm -p 8000:8000 ci-cd-demo-backend`
- 验证 `http://127.0.0.1:8000/docs`

补充说明：

- 当前后端镜像会从 `ghcr.io/astral-sh/uv` 拉取官方 `uv` 二进制
- 如果 Docker Host 拉取 `ghcr.io` 仍然很慢，问题通常在 Docker daemon 的出网链路
- 这种情况下可能仍需要为 Docker daemon 配置代理或镜像加速，而不是回退到 `pip install uv`

前端 Dockerfile 单独验证命令也应默认在 Docker Host 执行，例如：

- `docker build -t ci-cd-demo-frontend ./frontend`
- `docker run --rm -p 8080:80 ci-cd-demo-frontend`
- 验证 `http://127.0.0.1:8080`

### 2.3 Docker Host Compose 目标

在 Docker Host 执行 `docker compose up` 后，至少应具备：

- 可访问前端页面
- 前端可请求后端接口
- 后端健康检查可访问
- 容器之间通过内部网络通信

当前 T009 的最小 Compose 方案：

- `backend` 使用 `build: ./backend`
- `frontend` 使用 `build: ./frontend`
- `frontend` 容器通过挂载 `./nginx/nginx.conf` 启用统一入口与反代规则
- `frontend` 对外暴露 `8080:80`
- `backend` 只在容器内部监听 `8000`

当前 Compose 联调链路已统一收口到 Nginx 入口：

- 浏览器访问 `http://127.0.0.1:8080`
- 前端通过相对路径请求 `/api/hello`
- Nginx 将 `/api/` 和 `/health` 代理到 `backend:8000`

### 2.4 Docker Host 服务关系

- Nginx 对外暴露端口
- 目标形态下 Backend 仅在内部网络提供服务
- Frontend 产物由 Nginx 托管，或由前端镜像构建并复制到 Nginx
- 当前 T007 阶段仅验证前端静态文件可由 Nginx 镜像独立提供服务
- T008 已准备 `nginx/nginx.conf`，其中 `/api/` 和 `/health` 默认代理到 `backend:8000`
- `backend` 这个主机名依赖未来 T009 中的 Docker Compose service name
- T009 已将前端请求切到相对路径，并通过 Nginx 统一入口完成联调

## 3. 服务器部署思路

### 3.1 服务器职责

服务器只保留运行时职责：

- 保存部署用 Compose 文件
- 登录镜像仓库
- 拉取最新镜像
- 启动或重启容器

### 3.1.1 服务器目录建议

建议服务器部署目录使用：

```text
/opt/ci-cd-demo/
  compose.prod.yml
  .env
  nginx/
    nginx.conf
```

当前已准备的对应文件：

- [compose.prod.yml](/D:/Users/RX/Desktop/Agent/ci-cd-demo/compose.prod.yml)
- [deploy/.env.prod.example](/D:/Users/RX/Desktop/Agent/ci-cd-demo/deploy/.env.prod.example)
- [nginx/nginx.conf](/D:/Users/RX/Desktop/Agent/ci-cd-demo/nginx/nginx.conf)

### 3.2 服务器不做的事

- 不拉源码仓库
- 不安装 Node/Python 依赖
- 不执行前端构建
- 不执行后端打包
- 不承担 CI 校验职责

### 3.3 原因

这样做有几个直接好处：

- 服务器资源占用更低
- 部署步骤更稳定
- 构建环境与运行环境分离
- 回滚可以基于镜像标签进行

## 4. 推荐部署链路

1. 开发者提交代码到 GitHub
2. GitHub Actions 执行测试和镜像构建
3. GitHub Actions 将镜像推送到镜像仓库
4. GitHub Actions 通过 SSH 或其他方式触发服务器部署命令
5. 服务器执行 `docker compose pull`
6. 服务器执行 `docker compose up -d`

## 5. 生产部署 Compose 方案

当前已新增生产部署用 Compose：

- [compose.prod.yml](/D:/Users/RX/Desktop/Agent/ci-cd-demo/compose.prod.yml)

它与 Docker Host 验证用 `docker-compose.yml` 的区别是：

- `compose.prod.yml` 只使用 GHCR 镜像
- 不使用 `build`
- `backend` 不映射宿主机端口
- `frontend` 对外暴露 `8080:80`
- 继续挂载 `./nginx/nginx.conf:/etc/nginx/nginx.conf:ro`

当前使用的镜像为：

- `ghcr.io/mrzhang7777777/ci-cd-demo-backend:latest`
- `ghcr.io/mrzhang7777777/ci-cd-demo-frontend:latest`

说明：

- `backend` 只在 Compose 网络内部监听 `8000`
- `frontend` 通过 Nginx 代理到 `backend:8000`
- 这符合服务器只做 `pull + up` 的目标
## 6. Compose 文件规划

当前建议区分两类 Compose：

- Docker Host 验证用 Compose
- 服务器部署用 Compose

这样做的原因：

- Docker Host 验证环境可能保留更多学习与调试配置
- 服务器应尽量只保留运行必要配置

当前 Docker Host 验证命令：

- `docker compose up --build`
- 打开 `http://127.0.0.1:8080`
- 验证 `http://127.0.0.1:8080/health`
- 验证 `http://127.0.0.1:8080/api/hello`
- 如需清理，执行 `docker compose down`

本次已确认的 Ubuntu VM Docker Host 验证结果：

- 执行命令：`docker compose up --build`
- `http://127.0.0.1:8080/api/hello` 返回 `{"message":"hello from backend"}`
- `http://127.0.0.1:8080/health` 返回 `{"status":"ok"}`
- 说明当前最小 Compose 联调链路已经打通

当前服务器手动部署命令：

```bash
docker login ghcr.io
docker compose -f compose.prod.yml pull
docker compose -f compose.prod.yml up -d
docker compose -f compose.prod.yml ps
curl http://127.0.0.1:8080/health
```

本次已确认的 Ubuntu VM 生产 Compose 手动验证结果：

- 执行命令：
  - `git pull`
  - `docker compose -f compose.prod.yml pull`
  - `docker compose -f compose.prod.yml up -d`
  - `docker compose -f compose.prod.yml ps`
  - `curl http://127.0.0.1:8080/health`
  - `curl http://127.0.0.1:8080/api/hello`
- 验证结果：
  - `compose.prod.yml` 成功从 GHCR 拉取 backend/frontend 镜像
  - backend 镜像：`ghcr.io/mrzhang7777777/ci-cd-demo-backend:latest`
  - frontend 镜像：`ghcr.io/mrzhang7777777/ci-cd-demo-frontend:latest`
  - `/health` 返回 `{"status":"ok"}`
  - `/api/hello` 返回 `{"message":"hello from backend"}`
  - backend 未映射宿主机端口，只在 Compose 网络内暴露 `8000`
  - frontend 映射 `8080:80`

## 7. 镜像策略

建议每个核心服务独立镜像：

- `frontend`
- `backend`

Nginx 是否独立镜像有两种实现方向：

- 方案 A：前端镜像基于 Nginx，直接承载静态文件和反向代理配置
- 方案 B：前端静态文件镜像与 Nginx 网关镜像分离

当前倾向：

- 优先方案 A，减少服务数量和部署复杂度

补充说明：

- 当前已准备独立的 `nginx/nginx.conf`
- T009 当前采用在 Compose 中挂载该配置到前端容器
- 这样可以在不重做前端镜像结构的前提下完成最小联调

## 8. 环境变量原则

- 本地和服务器都通过环境变量注入配置
- Win11 开发机不依赖 Docker 环境变量启动容器
- 前端只暴露必要公开变量
- 后端变量尽量保持最少
- 不把密钥写死在仓库

服务器部署阶段当前预留的镜像相关变量见：

- [deploy/.env.prod.example](/D:/Users/RX/Desktop/Agent/ci-cd-demo/deploy/.env.prod.example)

当前预留变量名：

- `REGISTRY`
- `IMAGE_NAMESPACE`
- `BACKEND_IMAGE`
- `FRONTEND_IMAGE`

## 9. 低配服务器注意事项

针对 2 核 2G 服务器，建议：

- 控制镜像体积
- 控制容器数量
- 避免多余常驻进程
- 避免在运行机上做构建
- 预留一定内存给 Docker 和系统本身

## 10. 后续补充项

后续落地部署时应补充：

- 环境变量示例
- 镜像命名规则
- 部署命令清单
- 回滚命令清单
