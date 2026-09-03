---
title: Linux Deployment (systemd)
linkTitle: Linux
weight: 10
description: Install CheeseWAF on Linux with dedicated system accounts, static Web UI assets, and systemd service supervision.
---

This guide covers deploying CheeseWAF on Linux bare-metal or virtual machines using systemd.

## 1. Download & Extract {#unpack}

Download the official release archive for your architecture from GitHub Releases (example below uses AMD64; replace with ARM64 or LoongArch as appropriate):

```bash
tar -xzf cheesewaf-amd64-linux-*.tar.gz
cd cheesewaf-*
```

{{% pageinfo color="info" %}}
Official `.tar.gz` release archives include the `cheesewaf` binary, pre-compiled Web Console assets (`web/dist`), configuration templates (`configs/`), systemd service definitions, and an automated installer script.
{{% /pageinfo %}}

## 2. Automated Installation (Recommended) {#automated-install}

An FHS-compliant automated installation script is included at the root of the archive:

```bash
sudo ./install-linux.sh
```

This script standardizes the deployment:
- Installs the binary to `/usr/local/bin/cheesewaf` and creates the symlink `/usr/local/bin/waf-cli`.
- Installs the Web Console static assets to `/usr/share/cheesewaf/web`.
- Copies the initial configuration to `/etc/cheesewaf/cheesewaf.yaml`.
- Installs the systemd unit to `/etc/systemd/system/cheesewaf.service`.
- Creates a dedicated non-login system user `cheesewaf` and assigns ownership of `/var/lib/cheesewaf`.

## 3. Manual Step-by-Step Installation {#manual-install}

For environments with custom filesystem hierarchies or Ansible playbooks, follow the manual steps:

```bash
# 1. Install binary and create CLI symlink
sudo install -m 0755 cheesewaf /usr/local/bin/cheesewaf
sudo ln -sfn /usr/local/bin/cheesewaf /usr/local/bin/waf-cli

# 2. Create standard system directories
sudo mkdir -p /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf /usr/share/cheesewaf/web

# 3. Deploy Web Console static assets (Essential: required for Web UI to load)
sudo cp -R ./web/dist/. /usr/share/cheesewaf/web/

# 4. Copy initial configuration template
sudo cp configs/cheesewaf.yaml /etc/cheesewaf/cheesewaf.yaml

# 5. Create unprivileged system user and set ownership
sudo useradd --system --home /var/lib/cheesewaf --shell /usr/sbin/nologin cheesewaf
sudo chown -R cheesewaf:cheesewaf /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf

# 6. Install systemd service unit
sudo cp systemd/cheesewaf.service /etc/systemd/system/cheesewaf.service
```

## 4. Start & Verify the Service {#systemd}

Reload the systemd daemon and launch the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cheesewaf
sudo systemctl status cheesewaf
```

Once running, by default the management plane binds to loopback (`127.0.0.1:9443`). Use an SSH tunnel (`ssh -L 9443:127.0.0.1:9443 user@server` and browse to `http://127.0.0.1:9443/setup`). If you initialize from the server terminal instead, target the same systemd paths explicitly so setup does not create a second configuration under the current directory:

```bash
sudo -u cheesewaf /usr/local/bin/cheesewaf \
  --config /etc/cheesewaf/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf setup
```

See [System Initialization](../../tutorial/setup/) for details.

## Standard Filesystem Hierarchy {#paths}

| Path | Purpose |
| --- | --- |
| `/usr/local/bin/cheesewaf` | Main application binary |
| `/usr/share/cheesewaf/web` | Static Web Console frontend assets |
| `/etc/cheesewaf/cheesewaf.yaml` | Primary configuration file |
| `/var/lib/cheesewaf` | Runtime data directory (SQLite database, certificates, cache) |
| `/var/log/cheesewaf` | Access logs (`access.log`) and audit logs (`audit.log`) |

It is recommended to test reverse proxy routes and protection rules before switching production DNS records to the WAF ingress.
