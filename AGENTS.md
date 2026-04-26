# AGENTS.md

## 1. 目标

本文件定义 Codex 在本仓库中的工作规则，确保后续协作过程可重复、可审计、可渐进推进。

本项目当前阶段目标不是快速写业务代码，而是建立一个适合学习生产级 CI/CD、Docker 镜像构建与部署、GitHub Actions 自动化发布流程的最小可部署 Demo。

## 2. 项目定位

- 项目名称：`ci-cd-demo`
- 项目类型：前后端分离最小示例
- 学习重点：
  - Docker Host 联调
  - 前后端镜像化
  - Nginx 反向代理
  - GitHub Actions 持续集成与持续部署
  - 云服务器拉取镜像并启动容器
  - 使用 Codex 进行规范化协作

开发环境职责约束：

- Win11 物理机只负责 Codex 开发、git 提交、推送代码
- Win11 物理机不要求安装 Docker
- Docker 构建与运行验证在 Docker Host 上完成
- Docker Host 可以是 Ubuntu VM，也可以是云服务器

## 3. Codex 工作原则

### 3.1 先文档，后实现

在架构、目录、接口、部署流程未明确前，Codex 不应直接生成业务代码。

### 3.2 小步提交

每次只处理一个清晰任务。任务应满足：

- 可以独立开发
- 可以独立验证
- 可以独立提交
- 不依赖大规模返工

### 3.3 不做隐式决策

涉及以下事项时，必须先更新文档再落代码：

- 目录结构变更
- 接口约定变更
- 镜像构建方式变更
- GitHub Actions 流程变更
- 部署方式变更
- 环境变量命名变更

### 3.4 优先可部署，而不是功能多

本项目的优先级如下：

1. 能在 Docker Host 上通过 `docker compose up` 跑起来
2. 前端能访问后端
3. 镜像能被 CI 构建
4. 云服务器能只通过拉镜像完成部署
5. 在此基础上再补充更完整的工程细节

### 3.5 保持低复杂度

项目运行目标服务器为 2 核 2G 低配云主机，因此默认遵守：

- 不引入不必要中间件
- 不拆分多余服务
- 不加入重量级监控栈
- 不在服务器上进行源码构建
- 优先使用单机单实例部署模型

## 4. Codex 执行规则

### 4.1 开始任务前必须做的事

Codex 在开始任何实现任务前应先检查：

- `README.md`
- `docs/ai/TASKS.md`
- `docs/ai/ARCHITECTURE.md`
- `docs/ai/API_SPEC.md`
- `docs/ai/DEPLOYMENT.md`
- `docs/ai/CI_CD_PLAN.md`
- `docs/ai/DECISIONS.md`

如果代码计划与文档冲突，应先指出冲突，并优先更新文档或请求确认。

### 4.2 写代码时必须遵守

- 不提前创建超出当前任务范围的功能
- 不引入未在 `TECH_STACK.md` 中声明的核心依赖
- 不擅自扩展 API
- 不把 Win11 开发机便利方案直接当成 Docker Host 或生产部署方案
- 不在没有说明的情况下新增复杂脚本
- 不默认假设开发机具备 Docker 运行环境

### 4.3 Windows 开发机限制

- 除非用户明确说明已安装 Docker，否则 Codex 不得要求在 Win11 上执行 `docker`、`docker compose`、`docker build` 相关命令
- 涉及 Docker 的验证命令，默认应标注为在 Ubuntu VM、GitHub Actions 或云服务器执行

### 4.4 修改文档时必须遵守

新增或修改文档时应区分三类信息：

- 已确定：当前已经决定并计划执行的内容
- 候选方案：尚未最终采纳的备选项
- 待确认：需要在未来某个任务节点再决定的事项

### 4.5 输出要求

Codex 的输出应尽量包含：

- 改了什么
- 为什么这么改
- 如何验证
- 是否影响后续任务

## 5. 禁止事项

当前阶段，Codex 不应主动做以下事情：

- 不创建与当前任务无关的业务页面
- 不增加认证、数据库、缓存等未计划模块
- 不接入 Kubernetes
- 不引入重量级观测平台
- 不把部署流程设计成“服务器拉代码后构建”
- 不在没有任务要求时重构整个项目

## 6. 推荐协作方式

建议后续与 Codex 的协作流程如下：

1. 先从 `docs/ai/TASKS.md` 选择一个最小任务
2. 让 Codex 只完成该任务涉及的代码和文档
3. 完成后要求 Codex 说明验证方法
4. Win11 本地验证或 Docker Host 验证通过后再进入下一个任务

## 7. 文档优先级

当多份文档存在冲突时，默认按以下优先级理解：

1. `docs/ai/DECISIONS.md`
2. `docs/ai/ARCHITECTURE.md`
3. `docs/ai/API_SPEC.md`
4. `docs/ai/DEPLOYMENT.md`
5. `docs/ai/CI_CD_PLAN.md`
6. `docs/ai/TASKS.md`
7. `README.md`

## 8. 当前阶段边界

当前阶段只建立文档和执行规则，不创建前端、后端、Docker、Nginx、GitHub Actions 的实际实现文件。后续所有实现都应基于这些文档逐步推进。
