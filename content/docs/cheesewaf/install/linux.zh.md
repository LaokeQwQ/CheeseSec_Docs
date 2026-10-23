---
title: Linux 部署（systemd）
linkTitle: Linux
weight: 10
description: 通过一键脚本或离线发行包安装 CheeseWAF，并完成公网 HTTPS 管理入口的首次初始化。
---

本指南适用于 Linux 物理机、云服务器和虚拟机。一键安装器会询问语言、识别 CPU 架构、优先从 CheeseSec 官方来源下载并校验最新稳定版，在可用时安装 systemd 服务，并输出初始化地址。GitHub 用作下载失败时的备用来源；主机无法访问外网时，请使用离线流程。

## 流程摘要 {#summary}

```text
执行一键安装
        ↓
打开安装器输出的 HTTPS 初始化地址
        ↓
创建首个管理员
        ↓
检查服务、监听和就绪探针
        ↓
接入一个测试站点
```

主机无法访问外网时：下载发行包和 `SHA256SUMS`，校验后解压完整包，再在包根目录执行 `sudo ./install-linux.sh`。

## 准备工作 {#prepare}

| 项目 | 要求 |
| --- | --- |
| 操作系统 | 与发行包匹配的 64 位 Linux：`amd64`、`arm64` 或 `loong64` |
| 资源 | 1～2 核、2 GB 内存可运行轻量档；生产流量较大时应增加资源 |
| 权限 | `root` 或具备 `sudo` 权限的管理员 |
| 磁盘 | 足够保存发行包、Web 资源、运行时数据和日志 |
| 访问方式 | 能访问 `9443` 的浏览器，必要时经过受控网络或 SSH 隧道 |
| 防火墙 | 把 `9443` 限制在受信管理网络；数据面端口只对业务流量开放 |
| 工具 | `curl`、`tar`、`sha256sum`、`systemctl` 和 `ss` |

## 1. 一键安装（推荐） {#one-click}

```bash
curl --proto '=https' --proto-redir '=https' -fsSL https://cheesesec.com/install.sh | sudo bash
```

如果当前用户已经是 `root`，可以省略 `sudo`：

```bash
curl --proto '=https' --proto-redir '=https' -fsSL https://cheesesec.com/install.sh | bash
```

脚本从 `/dev/tty` 读取语言、安装根目录和安全入口输入，因此即使脚本内容通过标准输入传入，交互输入也不会被误当作脚本内容。无人值守环境请设置文档列出的 `CHEESEWAF_*` 环境变量后运行已下载的脚本；不要把密码或初始化 Token 写入命令行参数或历史记录。

下载及重定向必须使用 HTTPS。安装器优先获取官方发行信息和文件，只有官方下载失败时才尝试 GitHub。校验和或签名验证失败会在解压或安装前终止；不要切换来源绕过校验失败。如需在校验和之外验证发行来源，请单独安装可信的 `cosign`，并设置 `CHEESEWAF_VERIFY_SIGNATURE=1`；签名验证要求发行工作流身份与所选版本标签精确匹配。

### GitHub 备用入口 {#github-fallback}

如果无法下载官网的 `install.sh`，可使用 GitHub 发行入口：

```bash
curl --proto '=https' --proto-redir '=https' -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | sudo bash
```

该入口只用于下载失败的情况。安装因校验和或签名错误而终止后，不应使用备用来源重试来绕过校验。

### 选择版本或安装目录 {#install-options}

如需安装指定的稳定版或 Beta 版本，可设置 `CHEESEWAF_RELEASE`（`v` 前缀可省略）：

```bash
curl --proto '=https' --proto-redir '=https' -fsSL https://cheesesec.com/install.sh \
  | sudo env CHEESEWAF_RELEASE=v0.4.5 bash
```

选择语言后，交互流程会询问应用安装根目录。例如输入 `/opt/cheesewaf`，二进制、Web 资源、运行时配置、数据和日志会分别放在该目录下的 `bin/`、`web/`、`config/`、`data/`、`logs/` 子目录。直接回车则保留下面列出的分散式 FHS 默认布局。除非显式设置 `CHEESEWAF_UNIT_DIR`，systemd 单元仍安装在 `/etc/systemd/system`。

自动化部署时，可在调用安装器前设置 `CHEESEWAF_INSTALL_DIR`。如果同时设置 `CHEESEWAF_PREFIX`、`CHEESEWAF_WEB_DIR`、`CHEESEWAF_CONFIG_DIR`、`CHEESEWAF_DATA_DIR` 或 `CHEESEWAF_LOG_DIR`，对应的单独目录会覆盖根目录派生值：

```bash
curl --proto '=https' --proto-redir '=https' -fsSL https://cheesesec.com/install.sh \
  | sudo env CHEESEWAF_INSTALL_DIR=/opt/cheesewaf bash
```

安装根目录必须是绝对路径的专用目录，并且每个路径段只能使用 ASCII 字母、数字、`.`、`_` 或 `-`；共享系统目录以及含 Shell 元字符的路径会被拒绝。

安装过程会依次完成：

1. 询问中文或 English，并检测 Linux、架构、磁盘空间、`curl`、`tar`、`sha256sum`、`awk` 和 `od` 等前置条件。
2. 优先从官方来源下载所选服务器发行包，仅在下载失败时尝试 GitHub，并校验唯一匹配的 `SHA256SUMS` 条目。启用签名验证时，还会按精确版本标签验证校验文件；验证失败会在安装或启动服务前停止。
3. 安装二进制、Web 控制台、运行时配置和 systemd 单元，并创建无登录权限的 `cheesewaf` 服务用户。
4. 生成 HTTPS 管理监听、一次性初始化 Token 和安全入口路径。入口只接受 ASCII 字母和数字；默认随机生成，自定义值必须通过同一校验。
5. 在可用时启动服务，检查监听和健康状态，并打印版本、架构、安装路径、服务状态、公网管理地址、检测到的内网管理地址、Token 有效期和后续操作。没有 systemd 时只安装文件，并明确报告服务未启动。

请保存终端输出的完整初始化地址。交互终端会打印公网初始化地址和安全入口，也会打印每个检测到的内网初始化地址。非交互运行不会向标准输出回显敏感信息，而是写入配置目录下仅 root 可读的 `install-secrets.txt` 回执；只有在输出环境受保护时才设置 `CHEESEWAF_SHOW_SECRETS=1`。初始化地址对应的 URL 回执有效 10 分钟。Token 本身没有定时过期，只在首次初始化成功或被显式重置后失效。不要把完整地址提交到工单、截图、Shell 历史或日志。

## 2. 首次初始化与公网入口 {#first-setup}

打开安装器输出的 `https://` 地址。初始化地址固定使用 `/setup` 路径：

```text
https://PUBLIC_IP:9443/setup#setup_token=ONE_TIME_TOKEN
```

`ONE_TIME_TOKEN` 是一次性初始化 Token。浏览器会从 URL fragment 读取它，随后清理地址栏，并通过 `X-CheeseWAF-Setup-Token` 请求头提交；Token 不会放在查询参数、Cookie 或 `localStorage` 中。

初始化完成后，访问 `https://PUBLIC_IP:9443/SECURITY_ENTRY`。安全入口只包含 ASCII 字母和数字，由安装器默认生成，也可以使用通过校验的自定义值。入口会签发访问 Cookie 并跳转到登录页；初始化路由与完成后的安全入口是两个独立路径。

该安装路径默认使用 HTTPS，并把管理监听绑定到所有网卡。安装器会将检测到的公网主机写入 `admin.env`；如果服务器位于 NAT 或反向代理之后、没有直接公网地址，请设置 `CHEESEWAF_ADMIN_PUBLIC_HOST`。开放 `9443` 之前，应通过安全组、防火墙和反向代理把来源限制在受信管理网络内。本机生成的证书会让浏览器首次访问出现警告；生产环境请替换为受信证书。

初始化完成后，一次性 Token 立即失效。如果管理员尚未创建就丢失了地址，可在服务器上重置：

```bash
sudo -u cheesewaf /usr/local/bin/cheesewaf \
  --config /etc/cheesewaf/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf \
  setup token reset --show
```

设置 `--show` 时命令会打印新的初始化地址；不设置时，地址写入数据目录下受保护的 `setup.url` 文件。服务使用自定义安装根目录时，请同步调整路径。旧地址无法恢复。

对已有配置再次运行安装器会执行升级：现有监听、TLS、站点、策略和安全入口路径都会保留。请使用同一安装根目录，或再次设置相同的 `CHEESEWAF_*_DIR` 覆盖项，确保升级的是预期实例。

## 3. 验证 {#verify}

```bash
systemctl is-enabled cheesewaf
systemctl is-active cheesewaf
ss -ltnp | grep ':9443'
curl -kfsS https://127.0.0.1:9443/health/ready
sudo journalctl -u cheesewaf -n 100 --no-pager
```

预期结果：服务已启用且处于 active，`9443` 由预期进程持有，就绪探针返回成功。确认版本和架构与目标主机匹配。完成初始化后，再到控制台接入第一个受保护站点并配置数据面监听。

## 标准路径 {#paths}

| 路径 | 用途 |
| --- | --- |
| `/usr/local/bin/cheesewaf` | 主程序二进制 |
| `/usr/local/bin/waf-cli` | CLI 符号链接 |
| `/usr/share/cheesewaf/web` | Web 控制台静态文件 |
| `/etc/cheesewaf/cheesewaf.yaml` | 运行时配置副本 |
| `/var/lib/cheesewaf` | 本地数据库、证书、初始化状态和运行时数据 |
| `/var/log/cheesewaf` | 访问日志与审计日志 |

当设置 `CHEESEWAF_INSTALL_DIR=/opt/cheesewaf` 时，对应的应用路径为 `/opt/cheesewaf/bin/cheesewaf`、`/opt/cheesewaf/web`、`/opt/cheesewaf/config/cheesewaf.yaml`、`/opt/cheesewaf/data` 和 `/opt/cheesewaf/logs`。

## 4. 离线或手动安装 {#offline}

在可联网机器上，优先从 [CheeseSec 官网](https://cheesesec.com/) 获取与服务器架构匹配的 `.tar.gz`、`SHA256SUMS` 和（发布时提供的）签名文件，[GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 用作备用下载来源。所有文件必须来自同一发行版本，再将它们传到目标服务器。在下载目录先校验并解压，然后从包根目录执行安装器：

```bash
sha256sum --check SHA256SUMS --ignore-missing &&
tar -xzf cheesewaf-*-linux-*.tar.gz &&
cd cheesewaf-*-linux-* &&
sudo ./install-linux.sh
```

包内安装器要求工作目录中存在匹配的 `cheesewaf`、`web/dist`、`configs/` 和 systemd 单元；它本身不会下载发行包。不要把任意未经校验的远程脚本管道给 `bash`，也不要在解压目录之外运行包内安装器。

离线脚本仍会在本地询问语言和入口、生成初始化 Token 并启动服务。若系统没有 systemd，请把二进制和 `web/dist` 交给现有进程管理器启动。必须保留运行时配置副本和专用数据目录，不能直接修改仓库中的 `configs/cheesewaf.yaml` 模板。

不要使用未经校验的二进制、第三方镜像或旧版安装脚本。完整的 Linux 压缩包包含 `cheesewaf`、Web 资源、配置模板、systemd 单元和安装器；缺少任一项时应停止并重新下载。

## 故障排查 {#troubleshooting}

| 症状 | 检查 | 处理 |
| --- | --- | --- |
| 提示 `cheesewaf binary not found` | 在解压目录执行 `pwd` 和 `ls` | 从包根目录运行包内安装器，不要只解压二进制。 |
| 提示 `web/dist/index.html missing` | `find web -maxdepth 2 -type f` | 重新下载完整发行包。 |
| 校验和或签名验证失败 | 检查所选版本与匹配的校验、签名文件 | 停止安装并排查不匹配的原因，不要切换到备用来源或关闭校验继续安装。 |
| 服务启动后立即退出 | `sudo journalctl -u cheesewaf -b --no-pager` | 先修复第一个配置校验错误；确认服务指向运行时配置副本，而不是仓库模板。 |
| 远程无法访问 `9443` | `ss -ltnp \| grep ':9443'` | 在防火墙或安全组中只允许受信管理网络访问 `9443`，并确认监听地址与 `CHEESEWAF_ADMIN_PUBLIC_HOST`。 |
| 初始化页能打开但提交失败 | `sudo ls -l /etc/cheesewaf/install-secrets.txt` | 使用回执中的初始化地址，或执行 `sudo -u cheesewaf /usr/local/bin/cheesewaf --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf setup token reset --show` 重置；不要把地址贴进日志或工单。 |
| 反向代理返回 `502` | 在控制台核对上游配置，并从 WAF 主机测试连通性 | 确认源站可达，且站点指向数据面监听而不是管理端口。 |
| 生产存储配置导致服务拒绝启动 | 查看 `journalctl` 中的存储错误 | 配置所需的生产存储；不要强行回退到本地 SQLite。 |

Docker 的端口和数据卷行为请参考 [Docker 指南](../docker/)。备份与升级请继续阅读[运维](../operations/)。
