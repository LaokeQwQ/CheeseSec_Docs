---
title: Linux Deployment (systemd)
linkTitle: Linux
weight: 10
description: Install the CheeseWAF binary, configure dedicated unprivileged system users, and manage services via systemd.
---

This guide walks through deploying CheeseWAF as a systemd service on Linux bare-metal hosts or virtual machines.

## 1. Download & Unpack {#unpack}

Download the pre-compiled archive matching your system architecture from Releases and extract it (replace `amd64` with `arm64` or `loong64` as appropriate):

```bash
tar -xzf cheesewaf-*-linux-amd64.tar.gz
cd cheesewaf-*
```

## 2. Install Executables & Setup Directories {#install-files}

Install binaries to standard system paths and provision isolated runtime directories under a dedicated service account:

```bash
# Install main executable and CLI symlink
sudo install -m 0755 cheesewaf /usr/local/bin/cheesewaf
sudo ln -sf /usr/local/bin/cheesewaf /usr/local/bin/waf-cli

# Create configuration, data, and log directories
sudo mkdir -p /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
sudo cp configs/cheesewaf.yaml /etc/cheesewaf/cheesewaf.yaml

# Provision non-login system user and set directory ownership
sudo useradd --system --home /var/lib/cheesewaf --shell /usr/sbin/nologin cheesewaf
sudo chown -R cheesewaf:cheesewaf /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
```

## 3. Configure & Start systemd Service {#systemd}

Use the bundled systemd unit file to enable and launch the service:

```bash
sudo cp systemd/cheesewaf.service /etc/systemd/system/cheesewaf.service
sudo systemctl daemon-reload
sudo systemctl enable --now cheesewaf
sudo systemctl status cheesewaf
```

Once the daemon is active, navigate to `http://<SERVER_IP>:9443/setup` in your browser to access the initialization wizard. For step-by-step guidance, see [System Initialization](../../tutorial/setup/).

## Default System Layout {#paths}

| File / Directory Path | Purpose & Description |
| --- | --- |
| `/usr/local/bin/cheesewaf` | Main service binary executable |
| `/etc/cheesewaf/cheesewaf.yaml` | Main configuration file |
| `/var/lib/cheesewaf` | Runtime data directory housing SQLite databases, certificates, and state caches |
| `/var/log/cheesewaf` | Access logs and security alert logs |

It is recommended to verify reverse proxy routing, upstream connectivity, and baseline rule behavior before exposing the Data Plane port directly to public internet traffic.
