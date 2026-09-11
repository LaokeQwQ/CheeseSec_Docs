---
title: Windows 部署
linkTitle: Windows
weight: 30
description: Windows 环境下的三种运行方式：单文件 CLI、便携 Zip 包与 NSIS 图形安装器，以及原生系统服务与本地控制器说明。
---

在 Windows 操作系统中，CheeseWAF 提供三种运行分发形态，底层核心功能与防护引擎完全一致：

初始化向导会根据本机资源推荐档位。逻辑核数不超过 2 或内存不超过 2 GB 时使用 `low`；探测失败或超时也会回退到 `low`。管理面默认只监听 `127.0.0.1:9443`，本地辅助控制器另监听 `127.0.0.1:17943`。

## 1. 单文件 CLI 与原生 Windows 服务 {#cli}

适用于快速调试、脚本调用或注册为 Windows 系统服务：

```powershell
# 前台交互式启动 WAF 转发与管理服务
.\cheesewaf.exe serve --config .\data\config\cheesewaf.yaml --data-dir .\data

# 查询服务运行状态与 PID 租约
.\cheesewaf.exe status

# 安全终止运行中的服务
.\cheesewaf.exe stop
```

### 原生 Windows 系统服务感知

`cheesewaf serve` 内置了原生 Windows 服务状态机（基于 `golang.org/x/sys/windows/svc`）：
- 当被 Windows 服务控制管理器（SCM）拉起时，程序会自动识别为服务运行模式，无缝响应 SCM 的停止（`Stop`）与关机（`Shutdown`）信号并执行优雅退出。
- 服务名称默认注册为 `CheeseWAF`，无需借助第三方包装工具（如 NSSM 或 WinSW）。

## 2. 便携 Zip 压缩包 {#zip}

便携包内包含预设的配置文件模板与编译好的 Web 控制台静态资源：

1. 将 `cheesewaf-amd64-windows-*.zip` 解压至指定目录（如 `D:\CheeseWAF`）。
2. 在该目录下通过 PowerShell 执行初始化与启动：

```powershell
# 首次运行推荐通过交互式向导配置凭证
.\cheesewaf.exe setup

# 启动 WAF 守护进程
.\cheesewaf.exe serve --config .\data\config\cheesewaf.yaml --data-dir .\data
```

首次初始化尚未完成时，进程日志只显示基础 `/setup` 地址、受保护的 `data\setup.url` 路径和不含秘密的随机回执。请在 10 分钟有效期内从权限为 `0600` 的文件读取完整地址。初始化完成后，Token 会被撤销；过期的 `setup.url` 文件会被清理。

## 3. NSIS 图形安装向导 (推荐) {#nsis}

适用于需要图形化引导、注册 Windows 服务与创建系统快捷方式的生产或办公桌面环境：

1. 下载并运行 `cheesewaf-amd64-windows-*-setup.exe` 安装包（Windows ARM64 请使用 `arm64` 版本）。
2. 按照向导提示选择安装路径。安装程序会注册 `CheeseWAF` Windows 服务，并设置为手动启动（`start= demand`）；需要时可通过服务管理器或 `sc.exe` 显式启动/停止。
3. 卸载程序时，系统将默认保留 `data\` 目录中的业务数据库与配置文件，防止误删历史数据。

## 本地辅助控制器（GUI） {#gui}

`cheesewaf-gui` 是面向桌面环境的轻量级浏览器本地控制器，用于便捷管理主服务进程的生命周期：

- **网络边界**：严格限制仅监听本地回环地址 `127.0.0.1:17943`，杜绝局域网未授权探测。
- **核心功能**：启动/停止/重启服务、显示运行状态与 PID、直达 Web 管理控制台及快捷打开配置目录。
- **运行模型**：按需调用本地 `cheesewaf serve` 进程，不是第二套管理后台；控制器仅监听本机回环地址。

```powershell
.\cheesewaf-gui.exe --config .\data\config\cheesewaf.yaml --data-dir .\data
```

启动后可在浏览器中直接打开 `http://127.0.0.1:17943/` 进入桌面控制器界面。
