---
title: Linux 部署（systemd）
linkTitle: Linux
weight: 10
description: 在 Linux 环境下安装 CheeseWAF 二进制程序、配置系统独立用户、静态 Web 资源与 systemd 守护进程。
---

本指南适用于在 Linux 物理机或虚拟机中以 systemd 服务方式部署 CheeseWAF。

资源建议：逻辑核数不超过 2 或内存不超过 2 GB 的主机使用初始化向导推荐的 `low` 档。探测超时、取消或请求失败时，向导会回退到 `low`。主 WAF 的管理面默认只监听 `127.0.0.1:9443`；`storage.profile: production` 在完整生产启动接线完成前会拒绝启动，不会回退到 SQLite。

## 1. 下载与解压 {#unpack}

从 GitHub Releases 下载对应架构的完整发布包并解压（以 AMD64 为例，ARM64 或龙芯请替换包名中的架构标识）：

```bash
tar -xzf cheesewaf-amd64-linux-*.tar.gz
cd cheesewaf-*
```

{{% pageinfo color="info" %}}
官方发布的 `.tar.gz` 压缩包内不仅包含 `cheesewaf` 主程序，还包含了编译好的 Web 控制台静态资源目录（`web/dist`）、配置模板（`configs/`）、systemd 单元文件以及自动化安装脚本。
{{% /pageinfo %}}

## 2. 自动化一键安装（推荐） {#automated-install}

解压包根目录下附带了符合 Linux FHS 规范的官方安装脚本，一键完成文件分发、系统用户创建与权限配置：

```bash
sudo ./install-linux.sh
```

该脚本将自动执行以下标准化操作：
- 安装主程序至 `/usr/local/bin/cheesewaf`，并创建符号链接 `/usr/local/bin/waf-cli`。
- 安装 Web 控制台静态文件至 `/usr/share/cheesewaf/web`。
- 安装默认配置文件至 `/etc/cheesewaf/cheesewaf.yaml`。
- 安装 systemd 单元文件至 `/etc/systemd/system/cheesewaf.service`。
- 创建专用无登录权限系统用户 `cheesewaf`，并设置 `/var/lib/cheesewaf` 数据目录权限。

## 3. 手动分步安装指南 {#manual-install}

若您的生产环境有严格的目录定制规范或通过配置管理工具部署，可执行以下手动步骤：

```bash
# 1. 安装主程序与 CLI 符号链接
sudo install -m 0755 cheesewaf /usr/local/bin/cheesewaf
sudo ln -sfn /usr/local/bin/cheesewaf /usr/local/bin/waf-cli

# 2. 创建系统标准目录
sudo mkdir -p /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf /usr/share/cheesewaf/web

# 3. 部署 Web 控制台静态前端资源（关键：缺失会导致管理控制台 404）
sudo cp -R ./web/dist/. /usr/share/cheesewaf/web/

# 4. 将版本库模板复制到专用运行时配置路径
#    （后续编辑运行时副本，不要把初始化状态写回 configs/）
sudo install -m 0640 configs/cheesewaf.yaml /etc/cheesewaf/cheesewaf.yaml

# 5. 创建专用系统用户并配置目录归属
sudo useradd --system --home /var/lib/cheesewaf --shell /usr/sbin/nologin cheesewaf
sudo chown -R cheesewaf:cheesewaf /etc/cheesewaf /var/lib/cheesewaf /var/log/cheesewaf

# 6. 配置 systemd 单元文件
sudo cp systemd/cheesewaf.service /etc/systemd/system/cheesewaf.service
```

## 4. 启动与管理 systemd 服务 {#systemd}

重载 systemd 守护进程并启动 CheeseWAF：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cheesewaf
sudo systemctl status cheesewaf
```

服务启动后，管理平面默认仅绑定回环地址（`server.admin_listen: 127.0.0.1:9443`）。远程服务器推荐通过 SSH 隧道端口转发访问（`ssh -L 9443:127.0.0.1:9443 user@server` 后在本地访问 `http://127.0.0.1:9443/setup`）。若直接在服务器终端初始化，必须显式指向 systemd 使用的配置与数据目录，避免在当前目录另建一套配置：

```bash
sudo -u cheesewaf /usr/local/bin/cheesewaf \
  --config /etc/cheesewaf/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf setup
```

首次初始化尚未完成时，服务日志只显示基础 `/setup` 地址、受保护的 `/var/lib/cheesewaf/setup.url` 路径和不含秘密的随机回执。请在 10 分钟有效期内，从权限为 `0600` 的文件读取完整地址。初始化完成后，Token 会被撤销；过期的 `setup.url` 文件会被清理。

详细指引请参考 [系统初始化](../../tutorial/setup/)。

## 系统标准路径参考 {#paths}

| 文件与目录路径 | 用途说明 |
| --- | --- |
| `/usr/local/bin/cheesewaf` | 主程序二进制可执行文件 |
| `/usr/share/cheesewaf/web` | Web 控制台静态前端资源文件 |
| `/etc/cheesewaf/cheesewaf.yaml` | 主配置文件 |
| `/var/lib/cheesewaf` | 运行时数据目录，默认 `storage.profile: temporary` 时保存 SQLite 数据库、证书和状态缓存。配置 `storage.postgresql` 时，它只接收外部日志记录。 |
| `/var/log/cheesewaf` | 访问日志（`access.log`）与审计日志（`audit.log`）目录 |

建议在完成站点接入、反向代理与基础防护调试后，再正式将流量切换至 WAF 监听端口。
