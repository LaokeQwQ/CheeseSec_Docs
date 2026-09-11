---
title: Building from Source & Developer Guide
linkTitle: Development
weight: 190
description: Go and Node.js toolchain requirements, compiling frontend and backend assets, running automated test suites, and regression testing with attack corpora.
---

This guide is intended for developers contributing code or building CheeseWAF directly from source. For standard production deployments, using official pre-compiled releases from [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) is strongly recommended.

## 1. Development Toolchain Requirements {#toolchain}

- **Go Compiler**: Go **1.26** or higher
- **Frontend Environment**: Node.js **24.x** LTS and `npm` package manager

## 2. Compile Frontend Assets & Main Daemon {#build}

{{% pageinfo color="warning" %}}
**Console Assets Embedding Note**: When compiling from source, run `bash scripts/ci/build-web.sh` before `go build`. The script uses `npm ci --ignore-scripts` and builds with `CHEESEWAF_AGENT_EYES=0`; `@agent-eyes/agent-eyes` is development-only and must not enter release packages or production images. Do not use a bare `npm ci` that triggers its monorepo `postinstall`.
{{% /pageinfo %}}

```bash
# Clone the repository
git clone https://github.com/LaokeQwQ/CheeseWAF.git
cd CheeseWAF

# Build static assets for the React Web console and copy them into the Go embed directory
bash scripts/ci/build-web.sh

# Compile the Go single-binary executable
go build -o bin/cheesewaf ./cmd/cheesewaf

# Create a runtime config copy and launch the instance
mkdir -p ./data/config
cp ./configs/cheesewaf.yaml ./data/config/cheesewaf.yaml
./bin/cheesewaf serve --config ./data/config/cheesewaf.yaml --data-dir ./data
```

## 3. Running Automated Tests & Code Quality Checks {#tests}

```bash
# Execute Go unit tests and static analysis
go test -v ./cmd/... ./internal/...
go vet ./cmd/... ./internal/...

# Install frontend dependencies without development lifecycle scripts, then run checks
cd web && npm ci --no-audit --no-fund --ignore-scripts && npm run typecheck && npm test && cd ..

# Execute AST semantic engine regression benchmarks against attack corpora
go run ./cmd/cheesewaf-corpus --mode analyzer
```

`cheesewaf-corpus` runs built-in attack samples and false-positive corpora against the AST semantic analyzer, ensuring high detection rates without regression.
