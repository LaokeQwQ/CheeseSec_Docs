---
title: Linux（systemd）
linkTitle: Linux
weight: 10
description: 安装 CheeseWAF 二进制，创建系统用户，启用 systemd 单元。
---

Linux 虚拟机或物理机用这条路径。

## 解压 {#unpack}

```bash
tar -xzf cheesewaf-*-linux-amd64.tar.gz
cd cheesewaf-*
```

CPU 是 ARM64 或龙芯时，把 `amd64` 换成 `arm64` 或 `loong64`。

## 安装文件 {#install-files}

```bash
sudo install -m 0755 cheesewaf /usr/local/bin/cheesewaf
sudo ln -sf /usr/local/bin/cheesewaf /usr/local/bin/waf-cli

sudo mkdir -p /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
sudo cp configs/cheesewaf.yaml /etc/cheesewaf/cheesewaf.yaml

sudo useradd --system --home /var/lib/cheesewaf --shell /usr/sbin/nologin cheesewaf
sudo chown -R cheesewaf:cheesewaf /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
```

Linux 包里带有 `systemd/cheesewaf.service`。

```bash
sudo cp systemd/cheesewaf.service /etc/systemd/system/cheesewaf.service
sudo systemctl daemon-reload
sudo systemctl enable --now cheesewaf
sudo systemctl status cheesewaf
```

打开 `http://<主机>:9443/setup`，然后看 [初始化](../../tutorial/setup/)。

## 路径 {#paths}

| 路径 | 作用 |
| --- | --- |
| `/usr/local/bin/cheesewaf` | 可执行文件 |
| `/etc/cheesewaf/cheesewaf.yaml` | 配置 |
| `/var/lib/cheesewaf` | 数据、SQLite、证书 |
| `/var/log/cheesewaf` | 日志 |

先把站点、上游和可接受的防护等级配好，再把数据平面绑到公网地址。
