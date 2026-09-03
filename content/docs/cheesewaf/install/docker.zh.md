---
title: Docker Compose 部署
linkTitle: Docker
weight: 20
description: 使用 Docker Compose 编排部署 CheeseWAF，支持容器只读根文件系统与非 root 安全运行。
---

本方案适用于容器化云原生基础设施。CheeseWAF 官方镜像严格遵循安全生产加固规范，默认以专属非 root 系统用户（UID `10001`）运行，并支持启用只读根文件系统（Read-only Root Filesystem）。

## 编排配置（Compose 文件） {#compose-file}

参考项目仓库中的 `deploy/docker/docker-compose.yml`：

```yaml
services:
  cheesewaf:
    image: cheesewaf:dev
    build:
      context: ../..
      dockerfile: deploy/docker/Dockerfile
    user: "10001:10001"
    restart: unless-stopped
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777,noexec,nosuid,nodev
    ports:
      - "8080:8080"
      - "127.0.0.1:9443:9443"
    volumes:
      - cheesewaf-data:/var/lib/cheesewaf
      - cheesewaf-logs:/var/log/cheesewaf
    healthcheck:
      test: ["CMD", "/usr/local/bin/cheesewaf-entrypoint", "healthcheck"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  cheesewaf-data:
  cheesewaf-logs:
```

{{% pageinfo color="info" %}}
本地自行构建镜像时，构建上下文（context）须指向 CheeseWAF 项目的根目录，以确保 Web 前端源码（`web/`）与后端 Go 模块均能正常参与多阶段构建。
{{% /pageinfo %}}

## 启动与初始化 {#start}

执行以下命令在后台启动容器并观察日志：

```bash
docker compose -f deploy/docker/docker-compose.yml up -d
docker compose -f deploy/docker/docker-compose.yml logs -f cheesewaf
```

容器首次启动时会自动在持久化目录生成初始管理员配置，并为管理平面签发自签名证书。本 Compose 文件将管理端口仅绑定到 Docker 宿主机回环地址（`127.0.0.1:9443`），请在宿主机浏览器中打开 `https://127.0.0.1:9443/setup`。从其他机器访问时，请先将 `CHEESEWAF_SSH_TARGET` 设置为 SSH 目标，再执行 `ssh -N -L 9443:127.0.0.1:9443 "$CHEESEWAF_SSH_TARGET"` 建立隧道，之后仍使用同一回环地址；如需直接暴露端口，请显式修改绑定并配置相应的访问控制。亦可执行以下命令通过容器终端进行 CLI 初始化：

```bash
docker compose -f deploy/docker/docker-compose.yml exec -it cheesewaf \
  cheesewaf --config /var/lib/cheesewaf/config/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf setup
```

停止容器（`docker compose -f deploy/docker/docker-compose.yml down`）时，保存在 `cheesewaf-data`（包含 SQLite 数据库、证书与自定义规则）与 `cheesewaf-logs` 中的持久化数据均会被完整保留。
