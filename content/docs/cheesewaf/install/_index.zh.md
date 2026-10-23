---
title: 部署与安装
linkTitle: 部署与安装
weight: 20
description: 选择 CheeseWAF 部署路径，准备主机，并验证首个运行中的服务。
---

本页用于选择部署方式。全新 Linux 服务器可从一键安装或校验后的发行包开始；systemd 仍是快速上手采用的路径。

{{< nav-cards cols="2" >}}
{{< nav-card title="Linux（推荐）" link="/zh/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="一键脚本或校验后的发行包，可选择集中式应用根目录或标准 FHS 布局，并以 systemd 服务运行。" />}}
{{< nav-card title="Docker" link="/zh/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="使用 Compose 部署，适用于测试或已有 Docker 管理体系的环境。" />}}
{{< nav-card title="Windows" link="/zh/docs/cheesewaf/install/windows/" icon="fa-brands fa-windows" desc="支持 CLI、便携压缩包或带本地控制器的 NSIS 安装程序。" />}}
{{< nav-card title="macOS" link="/zh/docs/cheesewaf/install/macos/" icon="fa-brands fa-apple" desc="支持 DMG 桌面应用或便携命令行发行包。" />}}
{{< /nav-cards >}}

## 准备工作 {#prepare}

| 项目 | 最低或默认要求 | 作用 |
| --- | --- | --- |
| 操作系统 | 推荐路径使用受支持的 64 位 Linux | 发行包和 systemd 安装器面向 Linux 主机。 |
| CPU 与内存 | 1～2 核、2 GB 内存可运行轻量档 | 小型主机上初始化向导会推荐保守档位。 |
| 磁盘 | 足够保存发行包、Web 资源、运行时数据和日志 | 运行时数据应放在源码/模板目录之外。 |
| 权限 | `root` 或具备 `sudo` 权限的管理员 | 安装器需要创建 `cheesewaf` 服务用户和 systemd 单元。 |
| 网络 | 能访问 `9443` 管理面，并规划 `8080` 数据面 | 管理流量与业务流量应使用不同的访问策略。 |
| 浏览器 | 能访问管理监听器的浏览器 | Web 初始化向导和控制台都需要浏览器。 |
| 发行包完整性 | 从官方来源获取匹配发行包和 `SHA256SUMS`，GitHub 用作备用下载来源 | 解压或执行前先完成校验；校验和或签名错误时停止安装。 |

一键安装器会启用 HTTPS，将管理监听绑定到所有网卡，并用一次性 Token 和生成的安全入口保护首次初始化。开放端口前，应把 `9443` 限制在受信管理网络内。发布模板和初始化向导默认使用 `0.0.0.0:9443`，并启用 `server.admin_public: true`；完全省略 `server` 相关键时，才回退到加载器的兜底值 `127.0.0.1:9443`。公开管理面仍必须启用管理 TLS、配置有效证书，并限制来源网络。

小型主机建议使用轻量档：逻辑核数不超过 2 或内存不超过 2 GB 时，初始化向导会推荐 `low`。探测超时、取消或请求失败也会回退到 `low`。`storage.profile: production` 在完整生产接线完成前会拒绝启动，不会静默回退到 SQLite。

## 选择安装模式 {#modes}

- **Setup / 单机：** 一键安装、校验后的发行包配合 systemd，或 Docker。适合首次部署、试用和小型自托管服务。
- **Deploy / 生产：** 以 Linux 或 Docker 指南为起点，再补充受信证书、外部访问控制、备份、日志保留和经过演练的升级流程。请参考[运维](../operations/)。
- **离线 / 隔离网络：** 在联网机器下载发行包、校验文件和签名资源包，通过批准的介质传输后，按 Linux 指南的离线章节安装。

## 发行文件 {#release-files}

发行下载优先使用 [CheeseSec 官网](https://cheesesec.com/) 入口。[Linux 安装器](linux/) 优先获取官方发行信息和文件，仅在下载失败时才使用 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 备用来源。校验和或签名验证失败会停止安装，不能因此切换来源继续。请根据目标平台和架构选择文件：

| 文件名模式 | 目标平台 |
| --- | --- |
| `cheesewaf-amd64-linux-*.tar.gz` | Linux x86_64 |
| `cheesewaf-arm64-linux-*.tar.gz` | Linux ARM64 |
| `cheesewaf-loong64-linux-*.tar.gz` | Linux LoongArch |
| `cheesewaf-amd64-darwin-*` / `cheesewaf-arm64-darwin-*` | macOS Intel / Apple Silicon |
| `cheesewaf-*-windows-*` | Windows 可执行文件、ZIP 或安装程序 |

每个 Linux 压缩包都应包含 `cheesewaf`、`web/dist`、`configs/`、systemd 单元和 `install-linux.sh`。缺少任何一项时，停止操作并重新下载完整压缩包。

## 安装后 {#after-install}

1. 启动服务，并确认预期进程监听正确端口。
2. 打开安装器输出的 HTTPS 初始化地址，完成 `/setup` 并创建首个管理员。
3. 接入一个测试站点，经数据面监听器发送测试流量。
4. 在 TLS、访问控制、备份和升级流程验证完成前，把管理端口限制在受信管理网络内。

继续阅读[快速上手](../tutorial/)。
