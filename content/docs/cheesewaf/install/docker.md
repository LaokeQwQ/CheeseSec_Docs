---
title: Docker Compose Deployment
linkTitle: Docker
weight: 20
description: Deploy CheeseWAF with Docker Compose featuring a read-only root filesystem and unprivileged non-root execution.
---

This deployment guide is intended for containerized infrastructures. The official CheeseWAF Docker image adheres to strict container hardening practices, running as an unprivileged user (UID `10001`) with a read-only root filesystem.

## Compose Orchestration File {#compose-file}

Reference the production Compose file located at `deploy/docker/docker-compose.yml` in the project repository:

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
When building the image locally from source, ensure the build context is set to the root directory of the CheeseWAF repository.
{{% /pageinfo %}}

## Service Launch & Initialization {#start}

Execute the following commands to launch the service in detached mode and follow the container output:

```bash
docker compose up -d
docker compose logs -f cheesewaf
```

During the initial startup, the container generates a self-signed TLS certificate for the Control Plane and prints the one-time initialization Token to stdout. Open `https://<SERVER_IP>:9443/setup` in your browser to complete the setup wizard.

Stopping the container with `docker compose down` will preserve persistent named volumes (`cheesewaf-data` storing SQLite data/certificates and `cheesewaf-logs` storing access logs).
