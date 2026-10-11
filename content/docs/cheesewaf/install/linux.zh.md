---
title: Linux 部署（systemd）
linkTitle: Linux
weight: 10
description: 通过一键脚本或离线发行包安装 CheeseWAF，并完成公网 HTTPS 管理入口与一次性初始化。
---

本指南适用于 Linux 物理机、云服务器和虚拟机。在线安装会自动选择语言、识别 CPU 架构、拉取最新稳定版发行包、校验校验和文件、在可用时安装 systemd 服务并输出初始化地址；无法访问 GitHub 时，请使用文末的离线流程。

## 1. 一键安装（推荐） {#one-click}

只需复制并粘贴以下命令。脚本会在交互终端中询问语言，随后自动完成下载、校验和安装：

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | sudo bash
```

如果当前用户已经是 `root`，可以省略 `sudo`：

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | bash
```

脚本需要从 `/dev/tty` 读取语言、安装根目录和安全入口输入，因此即使脚本内容通过标准输入传入，也不会把交互输入误当作脚本内容。无人值守环境请设置文档列出的 `CHEESEWAF_*` 环境变量后运行已下载的脚本；不要把密码或安装 Token 写入命令行历史。

如需安装指定的稳定版或 Beta 版本，可设置 `CHEESEWAF_RELEASE`（`v` 前缀可省略）：

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh \
  | sudo env CHEESEWAF_RELEASE=v0.4.2-beta bash
```

选择语言后，交互流程会询问应用安装根目录。例如输入 `/opt/cheesewaf`，二进制、Web 资源、运行时配置、数据和日志会分别放在该目录下的 `bin/`、`web/`、`config/`、`data/`、`logs/` 子目录。直接回车则保留下面列出的分散式 FHS 默认布局。除非显式设置 `CHEESEWAF_UNIT_DIR`，systemd 单元仍安装在 `/etc/systemd/system`。

自动化部署时，可在调用安装器前设置 `CHEESEWAF_INSTALL_DIR`。如果同时设置 `CHEESEWAF_PREFIX`、`CHEESEWAF_WEB_DIR`、`CHEESEWAF_CONFIG_DIR`、`CHEESEWAF_DATA_DIR` 或 `CHEESEWAF_LOG_DIR`，对应的单独目录覆盖根目录派生值：

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh \
  | sudo env CHEESEWAF_INSTALL_DIR=/opt/cheesewaf bash
```

安装根目录必须是绝对路径，并且每个路径段只能使用 ASCII 字母、数字、`.`、`_` 或 `-`；共享系统目录以及含 Shell 元字符的路径会被拒绝。

安装过程会依次完成：

1. 选择中文或 English，并检测 Linux、架构、磁盘空间、`curl`、`tar`、`sha256sum`、`awk` 和 `od` 等前置条件。
2. 从 GitHub Releases 拉取指定服务器发行包，校验对应的唯一 `SHA256SUMS` 条目；校验失败会立即停止，不会启动旧或未知来源的程序。
3. 将二进制、Web 控制台、运行时配置和 systemd 单元安装到标准路径，并创建无登录权限的 `cheesewaf` 系统用户。
4. 生成 HTTPS 管理监听、一次性初始化 Token 和安全入口。入口路径只允许 ASCII 字母和数字；脚本会默认生成随机值，也允许你输入自定义值，不符合规则时会拒绝继续。
5. 在可用时启动 systemd 服务，检查端口和健康状态，并打印版本、架构、安装路径、配置/数据/日志路径、服务状态、公网管理地址、检测到的内网管理地址、Token 有效期和后续操作。没有 systemd 时只安装文件，并明确报告服务未启动。

安装结束时请保存终端输出中的完整初始化地址。交互终端会打印公网初始化地址和安全入口，也会打印每个检测到的内网地址；非交互运行默认不向标准输出回显敏感信息，而是写入仅 root 可读的 `install-secrets.txt` 回执，只有在输出环境受保护时才设置 `CHEESEWAF_SHOW_SECRETS=1`。Token 只在首次初始化阶段有效，默认短期有效且完成初始化后立即撤销；不要把完整地址提交到工单、截图、Shell 历史或日志。

## 2. 首次初始化与公网入口 {#first-setup}

初始化期间，使用安装器输出的 `https://` 地址打开向导。初始化地址固定使用 `/setup` 路径：

```text
https://PUBLIC_IP:9443/setup#setup_token=ONE_TIME_TOKEN
```

其中 `ONE_TIME_TOKEN` 是一次性初始化 Token。浏览器会从 URL fragment 读取 Token，随后清理地址栏，并通过 `X-CheeseWAF-Setup-Token` 请求头提交；Token 不会放在查询参数、Cookie 或 `localStorage` 中。

初始化完成后，访问 `https://PUBLIC_IP:9443/SECURITY_ENTRY`。安全入口只包含 ASCII 字母和数字，由安装器默认生成，也可以使用通过校验的自定义值。入口会签发访问 Cookie 并跳转到登录页；初始化路由与完成后的安全入口是两个独立路径。

该安装路径默认使用 HTTPS 并公开绑定管理面。安装器会将检测到的公网主机写入 `admin.env`；如果服务器位于 NAT 或反向代理之后且没有直接公网地址，请设置 `CHEESEWAF_ADMIN_PUBLIC_HOST`。生产环境应进一步限制安全组、防火墙和反向代理来源，只允许受信管理网络访问 `9443`；不要把初始化地址分享给其他人。若证书由本机临时生成，浏览器首次访问会显示证书警告，生产环境请替换为受信证书。

向导完成后，初始化 Token 立即失效。遗失地址时，可在服务器上查看权限为 `0600` 的运行时文件，或在管理员尚未创建前重置 Token：

```bash
sudo -u cheesewaf cheesewaf setup token reset
```

重置后必须使用命令输出的新地址；旧地址不可恢复。

对已有配置再次运行安装器会执行升级：现有监听地址、TLS、站点、策略和安全入口会保留。请使用同一安装根目录，或再次设置相同的 `CHEESEWAF_*_DIR` 覆盖项，确保升级的是预期实例。

## 3. 安装后检查 {#verify}

```bash
systemctl status cheesewaf --no-pager
ss -ltnp | grep ':9443'
sudo journalctl -u cheesewaf -n 100 --no-pager
```

检查输出中的版本和架构是否与目标服务器匹配，并确认管理端口只由预期进程监听。完成初始化后，再到控制台接入第一个站点和配置数据面监听。

默认 FHS 路径如下：

| 路径 | 用途 |
| --- | --- |
| `/usr/local/bin/cheesewaf` | 主程序二进制 |
| `/usr/local/bin/waf-cli` | CLI 符号链接 |
| `/usr/share/cheesewaf/web` | Web 控制台静态文件 |
| `/etc/cheesewaf/cheesewaf.yaml` | 运行时配置副本 |
| `/var/lib/cheesewaf` | 数据、证书和一次性初始化状态 |
| `/var/log/cheesewaf` | 访问日志与审计日志 |

当设置 `CHEESEWAF_INSTALL_DIR=/opt/cheesewaf` 时，对应的应用路径为 `/opt/cheesewaf/bin/cheesewaf`、`/opt/cheesewaf/web`、`/opt/cheesewaf/config/cheesewaf.yaml`、`/opt/cheesewaf/data` 和 `/opt/cheesewaf/logs`。

## 4. 离线或手动安装 {#offline}

在可联网机器上，从 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 下载与服务器架构匹配的完整 `.tar.gz`、`SHA256SUMS` 和（发布时提供的）签名文件，再将它们传到目标服务器。在下载目录先校验并解压，然后进入解压目录执行安装器：

```bash
sha256sum --check SHA256SUMS --ignore-missing
tar -xzf cheesewaf-*-linux-*.tar.gz
cd cheesewaf-*-linux-*
sudo ./install-linux.sh
```

离线脚本仍会在本地交互选择语言、生成安全入口并启动服务，但不会尝试重新下载发行包。若系统没有 systemd，请改用手动方式复制二进制和 `web/dist`，并由现有进程管理器启动；必须保留运行时配置副本与数据目录，不能直接修改仓库中的 `configs/cheesewaf.yaml` 模板。

不要使用未经校验的二进制、第三方镜像或旧版安装脚本。完整安装包包含 `cheesewaf`、Web 资源、配置模板、systemd 单元和本安装脚本；缺少其中任一项时应停止并重新下载。
