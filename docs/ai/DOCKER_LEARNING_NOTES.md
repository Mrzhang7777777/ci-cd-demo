# Docker Compose 学习阶段总结

## 1. Dockerfile、Image、Container、Compose、Nginx 的关系

这几个概念在本项目中的关系可以按“从定义到运行”的顺序理解：

- `Dockerfile`
  - 描述“如何构建镜像”
  - 它本身不是运行中的程序，而是一份构建说明书

- `Image`
  - 根据 `Dockerfile` 构建出来的结果
  - 可以理解为一个打包好的、可分发的运行环境快照

- `Container`
  - 镜像启动后的运行实例
  - 同一个镜像可以启动多个容器

- `Compose`
  - 用来一次性描述多个容器如何一起运行
  - 包括谁依赖谁、谁暴露端口、谁挂载配置、谁在同一个网络里通信

- `Nginx`
  - 在本项目里承担统一入口
  - 对外提供前端静态页面
  - 同时把 `/api/` 和 `/health` 反向代理到后端

在本项目里，链路是这样的：

1. `backend/Dockerfile` 定义后端镜像
2. `frontend/Dockerfile` 定义前端镜像
3. `docker-compose.yml` 把 `frontend` 和 `backend` 串起来
4. `frontend` 容器里的 Nginx 对外暴露 `80`
5. 用户通过 Nginx 访问前端页面和后端接口

## 2. 本项目 backend Dockerfile 做了什么

[backend/Dockerfile](/D:/Users/RX/Desktop/Agent/ci-cd-demo/backend/Dockerfile) 当前做了以下事情：

1. 使用 `python:3.12-slim` 作为运行基础镜像
2. 从 `ghcr.io/astral-sh/uv:0.5.30` 复制 `uv` 二进制
3. 设置 Python 和 `uv` 运行相关环境变量
4. 复制 `pyproject.toml`、`uv.lock`、`README.md`
5. 执行 `uv sync --frozen --no-dev` 安装生产依赖
6. 复制 `app/` 源码
7. 暴露 `8000`
8. 默认启动：
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000`

它的目标很明确：把 FastAPI 应用打成一个可以独立运行的最小镜像。

## 3. 本项目 frontend Dockerfile 做了什么

[frontend/Dockerfile](/D:/Users/RX/Desktop/Agent/ci-cd-demo/frontend/Dockerfile) 使用的是多阶段构建：

### 第一阶段：构建阶段

- 基于 `node:22-alpine`
- 复制 `package.json` 和 `package-lock.json`
- 执行 `npm ci`
- 复制前端源码
- 执行 `npm run build`

这一阶段的作用是生成 Vite 的静态构建产物，也就是 `dist/`。

### 第二阶段：运行阶段

- 基于 `nginx:1.27-alpine`
- 把第一阶段生成的 `dist/` 复制到 `/usr/share/nginx/html`
- 暴露 `80`

这一阶段不再包含 Node 构建工具，只保留运行静态站点所需的最小内容。

## 4. nginx/nginx.conf 在统一入口中的作用

[nginx/nginx.conf](/D:/Users/RX/Desktop/Agent/ci-cd-demo/nginx/nginx.conf) 是本项目统一入口的关键配置。

它主要做了三件事：

### 4.1 提供前端静态资源

- `root /usr/share/nginx/html`
- `index index.html`

这表示浏览器访问 `/` 时，Nginx 会返回前端打包后的静态文件。

### 4.2 处理前端刷新 fallback

- `try_files $uri $uri/ /index.html`

这表示当某个路径找不到对应静态文件时，回退到 `index.html`。这对前端路由刷新很重要。

### 4.3 代理后端接口

- `/api/` 代理到 `http://backend:8000`
- `/health` 代理到 `http://backend:8000`

这样浏览器只需要访问一个入口地址，例如：

- `http://127.0.0.1:8080/`
- `http://127.0.0.1:8080/api/hello`
- `http://127.0.0.1:8080/health`

而不用直接访问后端容器端口。

## 5. docker-compose.yml 如何串起 frontend 和 backend

[docker-compose.yml](/D:/Users/RX/Desktop/Agent/ci-cd-demo/docker-compose.yml) 当前定义了两个服务：

### backend

- `build: ./backend`
- 在容器内监听 `8000`

### frontend

- `build: ./frontend`
- 对外暴露 `8080:80`
- 挂载：
  - `./nginx/nginx.conf:/etc/nginx/nginx.conf:ro`
- `depends_on:`
  - `backend`

它们串起来的关键点有两个：

1. `frontend` 容器通过挂载自定义 `nginx.conf`，获得统一入口和反代规则
2. `frontend` 容器所在网络里可以直接通过服务名 `backend` 找到后端容器

所以最终访问路径是：

- 浏览器访问 `http://127.0.0.1:8080`
- 前端页面请求 `/api/hello`
- Nginx 把请求代理到 `backend:8000`

## 6. 为什么容器之间用 backend:8000，而不是 127.0.0.1:8000

这是 Docker Compose 学习阶段最重要的概念之一。

### 6.1 `127.0.0.1` 指向“当前容器自己”

在容器内部，`127.0.0.1` 不是宿主机，也不是其他容器，而是“当前这个容器自身”。

如果 Nginx 容器里写：

```text
http://127.0.0.1:8000
```

它会尝试访问 Nginx 容器自己的 8000 端口，而不是后端容器。

### 6.2 Compose 会提供服务名解析

在同一个 Compose 网络里，服务名本身就是可解析的主机名。

所以：

- `backend` 指向后端容器
- `backend:8000` 指向后端容器的 8000 端口

这就是为什么 Nginx 配置里应该写：

```text
http://backend:8000
```

而不是：

```text
http://127.0.0.1:8000
```

## 7. 为什么 Ubuntu VM 不需要手动安装 node/npm/python/uv

因为本项目的 Docker Host 验证阶段使用的是容器化构建与运行。

也就是说：

- 前端构建需要的 `node/npm` 在 `frontend` 镜像构建阶段里提供
- 后端运行需要的 `python/uv` 在 `backend` 镜像构建阶段里提供
- Nginx 在 `frontend` 运行阶段镜像里提供

Ubuntu VM 只需要安装：

- Docker
- Docker Compose

它不需要手动安装：

- Node.js
- npm
- Python
- uv

因为这些都已经在镜像构建过程中被封装进各自的容器链路中。

这正是容器化的重要价值之一：把应用依赖从宿主机环境中剥离出去。

## 8. 本次遇到的 Docker daemon 代理问题

这次学习阶段遇到的一个典型问题是：

- Ubuntu VM 上 `docker compose up --build` 时
- backend 镜像卡在下载 `uv`
- 原先的 `RUN pip install --no-cache-dir uv` 非常慢，700 秒仍未完成

这个问题暴露了一个关键事实：

- Docker 构建时的出网链路，不一定和宿主机命令行工具完全一致
- 即使宿主机能访问网络，Docker daemon 拉取镜像或下载依赖也可能仍然很慢

因此在 Docker Host 上，可能还需要考虑：

- Docker daemon 代理
- 镜像加速
- 访问 `ghcr.io`、`docker.io`、PyPI 的网络条件

这类问题通常不是应用代码错误，而是 Docker 出网环境问题。

## 9. 本次 backend Dockerfile 中 uv 安装方式的优化

为了解决 `pip install uv` 过慢的问题，后端镜像做了一个很关键的优化：

### 优化前

```dockerfile
RUN pip install --no-cache-dir uv
```

问题：

- 需要通过 PyPI 下载 `uv`
- 在 Ubuntu VM 的 Docker 构建环境里很慢

### 优化后

```dockerfile
FROM ghcr.io/astral-sh/uv:0.5.30 AS uv-binary
...
COPY --from=uv-binary /uv /uvx /bin/
```

优点：

- 直接复用官方 `uv` 镜像里的二进制
- 避免在构建阶段再走一次 `pip install uv`
- 保持后续 `uv sync --frozen --no-dev` 的使用方式不变

这类优化的本质是：

- 尽量减少 Docker 构建阶段的慢速依赖下载步骤
- 优先复用已经打包好的上游官方镜像产物

## 10. 已验证通过的命令和结果

本次 Docker Compose 学习阶段已经在 Ubuntu VM Docker Host 上验证通过。

执行命令：

```bash
docker compose up --build
```

验证结果：

- `http://127.0.0.1:8080/api/hello`
  - 返回：

```json
{"message":"hello from backend"}
```

- `http://127.0.0.1:8080/health`
  - 返回：

```json
{"status":"ok"}
```

说明：

- 当前最小前后端容器链路已经跑通
- Nginx 统一入口已经生效
- 前端到后端的请求链路已经通过 Docker Compose 联调验证
