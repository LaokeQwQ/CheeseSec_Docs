---
title: Linux (systemd)
linkTitle: Linux
weight: 10
description: Install the CheeseWAF binary, create the system user, and enable the systemd unit.
---

Use this path on a Linux VM or bare metal host.

## Unpack {#unpack}

```bash
tar -xzf cheesewaf-*-linux-amd64.tar.gz
cd cheesewaf-*
```

Replace `amd64` with `arm64` or `loong64` when that is the CPU.

## Install files {#install-files}

```bash
sudo install -m 0755 cheesewaf /usr/local/bin/cheesewaf
sudo ln -sf /usr/local/bin/cheesewaf /usr/local/bin/waf-cli

sudo mkdir -p /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
sudo cp configs/cheesewaf.yaml /etc/cheesewaf/cheesewaf.yaml

sudo useradd --system --home /var/lib/cheesewaf --shell /usr/sbin/nologin cheesewaf
sudo chown -R cheesewaf:cheesewaf /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
```

The Linux tarball includes `systemd/cheesewaf.service`.

```bash
sudo cp systemd/cheesewaf.service /etc/systemd/system/cheesewaf.service
sudo systemctl daemon-reload
sudo systemctl enable --now cheesewaf
sudo systemctl status cheesewaf
```

Open `http://<host>:9443/setup` and continue with [Initialize](../../tutorial/setup/).

## Paths {#paths}

| Path | Role |
| --- | --- |
| `/usr/local/bin/cheesewaf` | Binary |
| `/etc/cheesewaf/cheesewaf.yaml` | Config |
| `/var/lib/cheesewaf` | Data, SQLite, certs |
| `/var/log/cheesewaf` | Logs |

Bind the data plane to a public address only after you have a site, an upstream, and a paranoia level you accept.
