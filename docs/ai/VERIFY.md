# 验证说明

## 1. 目标

本文件用于沉淀当前最小 Demo 的验证方法，覆盖：

- Win11 开发验证
- Ubuntu VM / 云服务器 Docker Host 验证

当前阶段重点是快速确认以下链路是否正常：

- 后端单独启动是否正常
- 前端单独启动是否正常
- Docker Compose 最小联调是否正常

## 2. Win11 开发验证

### 2.1 backend

在项目根目录执行：

```powershell
cd backend
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

可手工验证：

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/api/hello`

预期：

- `/health` 返回 `{"status":"ok"}`
- `/api/hello` 返回 `{"message":"hello from backend"}`

### 2.2 frontend

另开一个终端，在项目根目录执行：

```powershell
cd frontend
npm run dev
```

浏览器访问 Vite 开发地址。

预期：

- 页面可以打开
- 页面能显示后端返回的 `hello from backend`

说明：

- Win11 开发验证不依赖 Docker
- 当前开发联调依赖后端 CORS 配置

## 3. Docker Host 验证

适用环境：

- Ubuntu VM
- 云服务器
- 其他已安装 Docker 和 Docker Compose 的 Linux Docker Host

执行命令：

```bash
docker compose up --build
```

验证命令：

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/api/hello
```

预期结果：

```json
{"status":"ok"}
```

```json
{"message":"hello from backend"}
```

说明：

- 当前 Compose 联调链路已经统一收口到 `http://127.0.0.1:8080`
- 前端通过 Nginx 统一入口访问后端
- 容器内部由 Nginx 代理到 `backend:8000`

## 4. 环境变量说明

当前最小 Demo 暂时不需要真实密钥。

根目录 [`.env.example`](/D:/Users/RX/Desktop/Agent/ci-cd-demo/.env.example) 只用于提前约定后续 CI/CD 与部署变量名：

- `REGISTRY`
- `IMAGE_NAMESPACE`
- `BACKEND_IMAGE`
- `FRONTEND_IMAGE`
- `SERVER_HOST`
- `SERVER_USER`
- `SERVER_PORT`
- `DEPLOY_PATH`

这些变量当前阶段主要用于：

- 统一命名
- 降低后续 GitHub Actions 和服务器部署阶段的返工

当前阶段不要求：

- 写入真实凭据
- 写入真实服务器信息
- 在 Win11 本地注入这些变量启动项目

## 5. GitHub Actions 与 Packages 验证

当前阶段除了本地和 Docker Host 验证，还应确认 GitHub 上的 CI/CD 结果。

### 5.1 GitHub Actions 页面检查

进入仓库的 `Actions` 页面后，重点查看以下 workflow：

- `ci-frontend`
- `ci-backend`
- `docker-release`

当前已确认通过的结果：

- `ci-frontend` 通过
- `ci-backend` 通过
- `docker-release` 通过

检查时应重点确认：

- 触发分支是否为 `main`
- workflow 最终状态是否为成功
- `docker-release` 是否执行到镜像推送完成

### 5.2 GitHub Packages / GHCR 检查

进入仓库或账号下的 `Packages` 区域，确认是否已经生成以下镜像包：

- `ci-cd-demo-backend`
- `ci-cd-demo-frontend`

检查时可重点确认：

- 包名称是否正确
- 是否能看到 `latest`
- 是否能看到 `sha-<7位提交哈希>` 形式的标签

### 5.3 当前阶段的验证结论

当前最小 CI/CD 链路已确认：

- 基础 CI 可通过
- 镜像可由 GitHub Actions 构建
- 镜像可成功推送到 GHCR
