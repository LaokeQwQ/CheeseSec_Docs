---
title: 从源码构建与开发指南
linkTitle: 开发
weight: 190
description: 开发环境依赖、前后端编译流程、单元测试与内置攻击语料评测工具。
---

本指南适用于参与 CheeseWAF 核心引擎开发、前端定制或需要从源代码独立构建二进制的场景。生产环境部署推荐直接使用官方发布的 [预编译发行包](https://github.com/LaokeQwQ/CheeseWAF/releases)。

## 开发环境工具链要求 {#toolchain}

- **Go 编译器**：Go **1.26** 或更高版本
- **Node.js 运行时**：Node.js **24.x** 及匹配的 npm 包管理器

## 源码拉取与编译流程 {#build}

CheeseWAF 采用单二进制打包架构，编译时会将前端 React 产物嵌入 Go 二进制中：

{{% pageinfo color="warning" %}}
**前端资源嵌入提醒**：从源码构建可执行文件若需包含 Web 控制台，必须先执行 `bash scripts/ci/build-web.sh`。该脚本使用 `npm ci --ignore-scripts` 并以 `CHEESEWAF_AGENT_EYES=0` 构建；`@agent-eyes/agent-eyes` 只允许本地开发使用，不得进入发布包或生产镜像。不要直接执行会触发该依赖 monorepo `postinstall` 的裸 `npm ci`。
{{% /pageinfo %}}

```bash
# 克隆仓库
git clone https://github.com/LaokeQwQ/CheeseWAF.git
cd CheeseWAF

# 1. 编译 Web 控制台前端静态资源，并同步到 Go 嵌入目录
bash scripts/ci/build-web.sh

# 2. 编译 Go 主程序二进制
go build -o bin/cheesewaf ./cmd/cheesewaf

# 3. 使用运行时配置副本启动本地服务，避免污染模板
mkdir -p ./data/config
cp ./configs/cheesewaf.yaml ./data/config/cheesewaf.yaml
./bin/cheesewaf serve --config ./data/config/cheesewaf.yaml --data-dir ./data
```

## 自动化测试与质量校验 {#tests}

在提交代码前，请执行以下完整的单元测试、静态检查与攻击语料评测：

```bash
# 后端 Go 单元测试与代码静态检查
go test -v ./cmd/... ./internal/...
go vet ./cmd/... ./internal/...

# 前端 TypeScript 类型检查与单元测试
cd web && npm ci --no-audit --no-fund --ignore-scripts && npm run typecheck && npm test && cd ..

# 运行内置攻击语料库压测与 AST 语义分析器评测
go run ./cmd/cheesewaf-corpus --mode analyzer
```

{{% pageinfo color="info" %}}
`cheesewaf-corpus` 是专用于研发阶段验证 AST 分析器检出率与误报率的评测工具，仅用于本地测试，严禁作为生产守护进程运行。
{{% /pageinfo %}}
