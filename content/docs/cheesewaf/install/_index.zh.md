---
title: 系统安装
linkTitle: 安装
weight: 20
description: 选择适用于 Linux、Docker、Windows 或 macOS 的 CheeseWAF 安装包。
---

CheeseWAF 支持以系统服务、容器编排或单二进制运行于各类主流操作系统。根据生产或测试环境的实际架构，选择对应的安装方式：

{{< nav-cards cols="2" >}}
{{< nav-card title="Linux" link="/zh/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="配置 systemd 守护进程、独立运行用户与 /etc/cheesewaf 目录。" />}}
{{< nav-card title="Docker" link="/zh/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="使用 Docker Compose 部署，支持只读根文件系统与非 root 安全运行。" />}}
{{< nav-card title="Windows" link="/zh/docs/cheesewaf/install/windows/" icon="fa-brands fa-windows" desc="支持单文件 CLI、便携 Zip 包及 NSIS 安装程序，附带本地控制器。" />}}
{{< nav-card title="macOS" link="/zh/docs/cheesewaf/install/macos/" icon="fa-brands fa-apple" desc="提供 DMG 图形应用与 tar.gz 命令行分发包。" />}}
{{< /nav-cards >}}

## 发行包列表 {#release-files}

可前往 GitHub Releases 下载官方发布的预编译包：

| 发行文件名 | 目标平台与架构 |
| --- | --- |
| `cheesewaf-*-linux-amd64.tar.gz` | Linux x86_64 架构 |
| `cheesewaf-*-linux-arm64.tar.gz` | Linux ARM64 架构 |
| `cheesewaf-*-linux-loong64.tar.gz` | Linux LoongArch（龙芯）架构 |
| `cheesewaf-*-darwin-amd64.tar.gz` / `.dmg` | macOS Intel 架构 |
| `cheesewaf-*-darwin-arm64.tar.gz` / `.dmg` | macOS Apple Silicon 架构 |
| `cheesewaf-*-windows-amd64.exe` | Windows x86_64 单文件可执行程序 |
| `cheesewaf-*-windows-arm64.exe` | Windows ARM64 单文件可执行程序 |
| `cheesewaf-*-windows-amd64.zip` | Windows x86_64 便携压缩包 |
| `cheesewaf-*-windows-arm64.zip` | Windows ARM64 便携压缩包 |
| `CheeseWAF-*-windows-*-setup.exe` | Windows NSIS 图形安装向导 |

安装完成后，请继续参考 [快速上手](../tutorial/) 完成系统初始化与站点接入。
