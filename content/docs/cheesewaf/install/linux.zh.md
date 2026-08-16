---
title: Linux 部署（systemd）
linkTitle: Linux
weight: 10
description: 在 Linux 环境下安装 CheeseWAF 二进制程序、配置系统独立用户与 systemd 守护进程。
---

本指南适用于在 Linux 物理机或虚拟机中以 systemd 服务方式部署 CheeseWAF。

## 1. 下载与解压 {#unpack}

从 Releases 下载对应架构的压缩包并解压（以 AMD64 为例，ARM64 或龙芯请替换包名中的架构标识）：

```bash
tar -xzf cheesewaf-*-linux-amd64.tar.gz
cd cheesewaf-*
```

## 2. 安装可执行文件与初始化目录 {#install-files}

将二进制文件安装至系统路径，并创建运行目录与专属系统用户：

```bash
# 安装主程序与 CLI 符号链接
sudo install -m 0755 cheesewaf /usr/local/bin/cheesewaf
sudo ln -sf /usr/local/bin/cheesewaf /usr/local/bin/waf-cli

# 创建配置、数据与日志目录
sudo mkdir -p /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
sudo cp configs/cheesewaf.yaml /etc/cheesewaf/cheesewaf.yaml

# 创建不可登录的系统用户并赋予目录权限
sudo useradd --system --home /var/lib/cheesewaf --shell /usr/sbin/nologin cheesewaf
sudo chown -R cheesewaf:cheesewaf /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf
```

## 3. 配置与启动 systemd 服务 {#systemd}

使用压缩包内附带的 systemd 单元文件启动服务并设置开机自启：

```bash
sudo cp systemd/cheesewaf.service /etc/systemd/system/cheesewaf.service
sudo systemctl daemon-reload
sudo systemctl enable --now cheesewaf
sudo systemctl status cheesewaf
```

服务启动后，在浏览器中访问 `http://<服务器IP>:9443/setup` 进入初始化向导。详细流程请参考 [系统初始化](../../tutorial/setup/)。

## 系统默认路径说明 {#paths}

| 文件与目录路径 | 用途说明 |
| --- | --- |
| `/usr/local/bin/cheesewaf` | 主程序可执行文件 |
| `/etc/cheesewaf/cheesewaf.yaml` | 主配置文件 |
| `/var/lib/cheesewaf` | 运行时数据目录，保存 SQLite 数据库、证书与状态缓存 |
| `/var/log/cheesewaf` | 访问日志与告警日志目录 |

建议在完成站点配置、上游源站反代测试与基础防护规则调试后，再将数据平面端口正式接入生产公网流量。
