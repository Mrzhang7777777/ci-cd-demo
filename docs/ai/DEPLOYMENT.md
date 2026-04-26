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

### 2.3 Docker Host Compose 目标

在 Docker Host 执行 `docker compose up` 后，至少应具备：

- 可访问前端页面
- 前端可请求后端接口
- 后端健康检查可访问
- 容器之间通过内部网络通信

### 2.4 Docker Host 服务关系

- Nginx 对外暴露端口
- Backend 仅在内部网络提供服务
- Frontend 产物由 Nginx 托管，或由前端镜像构建并复制到 Nginx

## 3. 服务器部署思路

### 3.1 服务器职责

服务器只保留运行时职责：

- 保存部署用 Compose 文件
- 登录镜像仓库
- 拉取最新镜像
- 启动或重启容器

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

## 5. Compose 文件规划

当前建议区分两类 Compose：

- Docker Host 验证用 Compose
- 服务器部署用 Compose

这样做的原因：

- Docker Host 验证环境可能保留更多学习与调试配置
- 服务器应尽量只保留运行必要配置

## 6. 镜像策略

建议每个核心服务独立镜像：

- `frontend`
- `backend`

Nginx 是否独立镜像有两种实现方向：

- 方案 A：前端镜像基于 Nginx，直接承载静态文件和反向代理配置
- 方案 B：前端静态文件镜像与 Nginx 网关镜像分离

当前倾向：

- 优先方案 A，减少服务数量和部署复杂度

## 7. 环境变量原则

- 本地和服务器都通过环境变量注入配置
- Win11 开发机不依赖 Docker 环境变量启动容器
- 前端只暴露必要公开变量
- 后端变量尽量保持最少
- 不把密钥写死在仓库

## 8. 低配服务器注意事项

针对 2 核 2G 服务器，建议：

- 控制镜像体积
- 控制容器数量
- 避免多余常驻进程
- 避免在运行机上做构建
- 预留一定内存给 Docker 和系统本身

## 9. 后续补充项

后续落地部署时应补充：

- Ubuntu VM 初始化步骤
- 服务器目录结构
- 环境变量示例
- 镜像命名规则
- 部署命令清单
- 回滚命令清单
