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
**Console Assets Embedding Note**: When compiling from source, you must run `bash scripts/ci/build-web.sh` (or `cd web && npm ci && npm run build` and copy `web/dist` to `internal/webui/dist/`) before `go build`, otherwise web console routes will return 404.
{{% /pageinfo %}}

```bash
# Clone the repository
git clone https://github.com/LaokeQwQ/CheeseWAF.git
cd CheeseWAF

# Build static assets for the React Web console
cd web
npm ci
npm run build
cd ..
# Copy the generated bundle into the Go embed directory
cp -R web/dist/. internal/webui/dist/

# Compile the Go single-binary executable
go build -o bin/cheesewaf ./cmd/cheesewaf

# Launch the newly compiled instance
./bin/cheesewaf serve --config ./configs/cheesewaf.yaml
```

## 3. Running Automated Tests & Code Quality Checks {#tests}

```bash
# Execute Go unit tests and static analysis
go test -v ./cmd/... ./internal/...
go vet ./cmd/... ./internal/...

# Run frontend TypeScript type checking and test suites
cd web && npm run typecheck && npm test && cd ..

# Execute AST semantic engine regression benchmarks against attack corpora
go run ./cmd/cheesewaf-corpus --mode analyzer
```

`cheesewaf-corpus` runs built-in attack samples and false-positive corpora against the AST semantic analyzer, ensuring high detection rates without regression.
