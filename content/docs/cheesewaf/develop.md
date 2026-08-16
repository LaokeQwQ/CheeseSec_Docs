---
title: Build from source
linkTitle: Develop
weight: 190
description: Go and Node versions, frontend build, tests, and the attack corpus tool.
---

You only need this page if you compile CheeseWAF yourself.
Operators should use [Releases](https://github.com/LaokeQwQ/CheeseWAF/releases).

## Toolchain {#toolchain}

- Go **1.26** or newer
- Node.js **24.x** and npm

## Build {#build}

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

## Tests {#tests}

```bash
go test -v ./cmd/... ./internal/...
go vet ./cmd/... ./internal/...

cd web && npm run typecheck && npm test && cd ..

go run ./cmd/cheesewaf-corpus --mode analyzer
```

`cheesewaf-corpus` runs the built-in attack corpus against the analyzer.
It is a development check, not a production daemon.
