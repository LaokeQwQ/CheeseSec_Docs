---
title: Docker Compose
linkTitle: Docker
weight: 20
description: Run CheeseWAF in Compose with a read-only root filesystem and a non-root user.
---

Use this path in a container host.
`docker compose build` produces `linux/amd64` or `linux/arm64` for the host CPU.

The image runs as UID `10001`.
The root filesystem is read-only.

## Compose file {#compose-file}

The repository file is `deploy/docker/docker-compose.yml`.
A minimal copy:

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

Build context must be the CheeseWAF repository root when you use that Dockerfile.

## Start {#start}

```bash
docker compose up -d
docker compose logs -f cheesewaf
```

Open `https://<host>:9443/setup`.
The container uses a self-signed admin certificate by default.
The first-run token is in the startup log.

`docker compose down` keeps the named volumes.
Site config and SQLite live in `cheesewaf-data`.
