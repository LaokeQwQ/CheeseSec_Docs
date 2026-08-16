---
title: Windows 部署
linkTitle: Windows
weight: 30
description: Windows 环境下的三种运行方式：单文件 CLI、便携 Zip 包与 NSIS 图形安装器，以及本地控制器使用说明。
---

在 Windows 操作系统中，CheeseWAF 提供三种运行分发形态，底层核心功能与防护引擎完全一致：

## 1. 单文件 CLI 模式 {#cli}

适用于快速调试或自动化脚本：

1. 下载对应架构的单文件程序（如 `cheesewaf-*-windows-amd64.exe`）。
2. 在 PowerShell 或命令提示符中执行：

```powershell
# 启动 WAF 转发与管理服务
.\cheesewaf-*-windows-amd64.exe serve --config .\cheesewaf.yaml --data-dir .\data

# 查询服务运行状态
.\cheesewaf-*-windows-amd64.exe status

# 停止正在运行的服务
.\cheesewaf-*-windows-amd64.exe stop
```

## 2. 便携 Zip 压缩包 {#zip}

便携包内包含预设的配置文件模板与静态资源：

1. 将 `cheesewaf-*-windows-amd64.zip` 解压至指定目录（如 `D:\CheeseWAF`）。
2. 在该目录下执行：

```powershell
.\cheesewaf.exe serve --config .\configs\cheesewaf.yaml --data-dir .\data
```

## 3. NSIS 图形安装向导 (推荐) {#nsis}

适用于需要图形化引导与自动创建系统快捷方式的场景：

1. 运行 `CheeseWAF-*-windows-*-setup.exe` 安装包。
2. 按照向导提示选择安装路径并完成安装。安装程序支持自动注册 Windows 系统服务（`CheeseWAF`）。
3. 卸载程序时，系统将默认保留 `data\` 目录中的业务数据与数据库文件。

## 本地辅助控制器（GUI） {#gui}

`cheesewaf-gui` 是面向桌面环境的本地辅助控制程序，用于管理主服务进程的生命周期：

- **网络边界**：严格限制仅监听本地回环地址 `127.0.0.1:17943`。
- **核心功能**：显示当前进程 PID、实时运行状态、快捷启动/停止服务、打开 Web 管理控制台及直达配置目录。
- **开机自启**：支持在当前用户注册表（`HKCU\Run`）中配置自启动项。

```powershell
.\cheesewaf-gui.exe --config .\configs\cheesewaf.yaml --data-dir .\data
```

启动后可在浏览器中直接打开 `http://127.0.0.1:17943/` 进入控制器界面。
