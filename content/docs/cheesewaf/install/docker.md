---
title: Docker Compose Deployment
linkTitle: Docker
weight: 20
description: Deploy CheeseWAF with Docker Compose supporting read-only root filesystems and unprivileged container security.
---

This guide covers deploying CheeseWAF on containerized infrastructure. The official container images follow strict security hardening practices: running as an unprivileged user (UID `10001`) with read-only root filesystem capabilities.

## Compose Configuration {#compose-file}

Reference `deploy/docker/docker-compose.yml`:

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

{{% pageinfo color="info" %}}
When building locally, ensure the build context points to the root of the CheeseWAF repository so both the frontend (`web/`) and backend Go modules build successfully.
{{% /pageinfo %}}

## Launching & Initialization {#start}

Start the container daemon and view logs:

```bash
docker compose up -d
docker compose logs -f cheesewaf
```

On initial startup, the container generates self-signed TLS certificates for the admin API. Navigate to `https://<server-ip>:9443/setup` in your browser to complete the Web setup wizard, or run the CLI wizard inside the container:

```bash
docker compose exec -it cheesewaf cheesewaf setup
```

Stopping containers with `docker compose down` safely preserves your SQLite databases, certificates, and log streams inside the named volumes `cheesewaf-data` and `cheesewaf-logs`.
