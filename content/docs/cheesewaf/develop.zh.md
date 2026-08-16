---
title: 从源码构建
linkTitle: 开发
weight: 190
description: Go 和 Node 版本、前端构建、测试，以及攻击语料工具。
---

只有自己编译 CheeseWAF 时才需要这一页。
运维人员请用 [Releases](https://github.com/LaokeQwQ/CheeseWAF/releases)。

## 工具链 {#toolchain}

- Go **1.26** 或更新
- Node.js **24.x** 和 npm

## 构建 {#build}

```bash
git clone https://github.com/LaokeQwQ/CheeseWAF.git
cd CheeseWAF

cd web
npm ci
npm run build
cd ..

go build -o bin/cheesewaf ./cmd/cheesewaf
./bin/cheesewaf serve --config ./configs/cheesewaf.yaml
```

## 测试 {#tests}

```bash
go test -v ./cmd/... ./internal/...
go vet ./cmd/... ./internal/...

cd web && npm run typecheck && npm test && cd ..

go run ./cmd/cheesewaf-corpus --mode analyzer
```

`cheesewaf-corpus` 用内置攻击语料打分析器。
它是开发检查，不是生产守护进程。
