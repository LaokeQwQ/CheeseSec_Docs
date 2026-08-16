---
title: 安装
linkTitle: 安装
weight: 20
description: 按 Linux、Docker、Windows、macOS 选择 CheeseWAF 安装包。
---

只选一条安装路径。
不要在同一台机器上把 NSIS 安装和手拷的 Linux 目录混在一起，除非你清楚谁占用端口。

{{< nav-cards cols="2" >}}
{{< nav-card title="Linux" link="/zh/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="systemd 单元、系统用户、/etc/cheesewaf。" />}}
{{< nav-card title="Docker" link="/zh/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="Compose、只读根文件系统、非 root UID 10001。" />}}
{{< nav-card title="Windows" link="/zh/docs/cheesewaf/install/windows/" icon="fa-brands fa-windows" desc="单文件 exe、zip 或 NSIS。本地控制器只听回环。" />}}
{{< nav-card title="macOS" link="/zh/docs/cheesewaf/install/macos/" icon="fa-brands fa-apple" desc="DMG 应用或 tar.gz 命令行。" />}}
{{< /nav-cards >}}

## 发行文件 {#release-files}

下载 **Alpha** 预发布包，或从 Actions 产物里取同一套文件。

| 文件 | 平台 |
| --- | --- |
| `cheesewaf-*-linux-amd64.tar.gz` | Linux x86_64 |
| `cheesewaf-*-linux-arm64.tar.gz` | Linux ARM64 |
| `cheesewaf-*-linux-loong64.tar.gz` | Linux 龙芯 |
| `cheesewaf-*-darwin-amd64.tar.gz` / `.dmg` | macOS Intel |
| `cheesewaf-*-darwin-arm64.tar.gz` / `.dmg` | macOS Apple Silicon |
| `cheesewaf-*-windows-amd64.exe` | Windows x86_64 单文件 CLI |
| `cheesewaf-*-windows-arm64.exe` | Windows ARM64 单文件 CLI |
| `cheesewaf-*-windows-amd64.zip` | Windows x86_64 便携目录 |
| `cheesewaf-*-windows-arm64.zip` | Windows ARM64 便携目录 |
| `CheeseWAF-*-windows-*-setup.exe` | Windows NSIS 安装器 |

装完后继续看 [快速上手](../tutorial/)。
