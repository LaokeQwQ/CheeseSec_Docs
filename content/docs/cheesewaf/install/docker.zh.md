---
title: Docker Compose
linkTitle: Docker
weight: 20
description: 用 Compose 跑 CheeseWAF。根文件系统只读，进程用非 root 用户。
---

容器主机用这条路径。
`docker compose build` 会按宿主机 CPU 编出 `linux/amd64` 或 `linux/arm64`。

镜像以 UID `10001` 运行。
根文件系统只读。

## Compose 文件 {#compose-file}

仓库里的文件是 `deploy/docker/docker-compose.yml`。
最小副本：

```yaml
services:
  cheesewaf:
    image: cheesewaf:latest
    build:
      context: .
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
      - "9443:9443"
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

用仓库里的 Dockerfile 时，构建上下文必须是 CheeseWAF 仓库根目录。

## 启动 {#start}

```bash
docker compose up -d
docker compose logs -f cheesewaf
```

打开 `https://<主机>:9443/setup`。
容器默认给管理端用自签名证书。
首次初始化令牌在启动日志里。

`docker compose down` 不会删命名卷。
站点配置和 SQLite 在 `cheesewaf-data` 里。
