---
title: Docker Compose Deployment
linkTitle: Docker
weight: 20
description: Deploy CheeseWAF with Docker Compose supporting read-only root filesystems and unprivileged container security.
---

This guide covers deploying CheeseWAF on containerized infrastructure. The repository provides a hardened Dockerfile and Compose example; the example builds the image locally. Do not treat `cheesewaf:dev` as a vendor-signed or registry-published image unless you have separately verified the image provenance. The runtime is configured to run as an unprivileged user (UID `10001`) with a read-only root filesystem.

## Compose Configuration {#compose-file}

Reference `deploy/docker/docker-compose.yml`:

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
When building locally, ensure the build context points to the root of the CheeseWAF repository so both the frontend (`web/`) and backend Go modules build successfully.
The sample `8080:8080` mapping publishes the data-plane listener on all Docker host interfaces. Put it behind an intentional firewall/reverse-proxy policy, or bind it to a controlled interface; only the admin mapping is loopback-bound by default.
{{% /pageinfo %}}

## Launching & Initialization {#start}

Start the container daemon and view logs:

```bash
docker compose -f deploy/docker/docker-compose.yml up -d
docker compose -f deploy/docker/docker-compose.yml logs -f cheesewaf
```

On initial startup, the container generates self-signed TLS certificates for the admin API. This Compose file binds the admin port to the Docker host's loopback interface (`127.0.0.1:9443`), so open `https://127.0.0.1:9443/setup` on the Docker host. From another machine, set `CHEESEWAF_SSH_TARGET` to your SSH target and create a tunnel with `ssh -N -L 9443:127.0.0.1:9443 "$CHEESEWAF_SSH_TARGET"`, then use the same local URL; if you intentionally change the port binding, apply an appropriate access-control policy. You can also run the CLI wizard inside the container:

While first-install setup is pending, the container log never prints the setup token or complete URL. It shows only the base `/setup` URL, the protected `/var/lib/cheesewaf/setup.url` path, and an opaque receipt. Read the complete URL from that mode `0600` file within its 10-minute validity period. After setup completes, the token is revoked; expired `setup.url` files are cleaned up.

```bash
docker compose -f deploy/docker/docker-compose.yml exec -it cheesewaf \
  cheesewaf --config /var/lib/cheesewaf/config/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf setup
```

Stopping containers with `docker compose -f deploy/docker/docker-compose.yml down` safely preserves SQLite data, certificates, and log streams inside the named volumes `cheesewaf-data` and `cheesewaf-logs`. If `storage.postgresql` is configured, it receives external access-log records; the Docker volume still contains the management database for the default `storage.profile: temporary`. The reserved `production` profile currently fails closed at startup.
