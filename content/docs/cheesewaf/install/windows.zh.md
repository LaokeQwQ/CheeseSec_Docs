---
title: Windows
linkTitle: Windows
weight: 30
description: 单文件 CLI、便携 zip 或 NSIS 安装器。图形控制器只监听回环地址。
---

Windows 有三种形态。
它们不是三套不同的 WAF。

## A. 单文件 CLI {#cli}

1. 下载 `cheesewaf-*-windows-amd64.exe` 或 `arm64` 文件。
2. 运行：

```powershell
.\cheesewaf-*-windows-amd64.exe serve --config .\cheesewaf.yaml --data-dir .\data
.\cheesewaf-*-windows-amd64.exe status
.\cheesewaf-*-windows-amd64.exe stop
```

转发进程不依赖安装器。
zip / DMG / tar 包里的管理界面在可执行文件旁边的 `web/dist`。

## B. 便携 zip {#zip}

1. 把 `cheesewaf-*-windows-amd64.zip` 解压到目录，例如 `D:\CheeseWAF`。
2. 运行：

```powershell
.\cheesewaf.exe serve --config .\configs\cheesewaf.yaml --data-dir .\data
.\cheesewaf.exe status
.\cheesewaf.exe stop
```

## C. NSIS 安装器 {#nsis}

1. 运行 `CheeseWAF-*-windows-amd64-setup.exe` 或 `arm64` 安装包。
2. 按向导安装。
3. 卸载时默认保留 `data\`。

安装器可能会注册 Windows 服务（`sc.exe create CheeseWAF …`）。
把它当成尽力而为，不要假设每台机器都注册成功。

## 本地控制器 {#gui}

`cheesewaf-gui` **不是**第二套管理后台。
它只负责启动、停止，并打开真正的管理界面。

- 监听地址：`127.0.0.1:17943`
- 显示 PID 和运行状态
- 打开 Web 控制台和配置文件夹
- 可选：当前用户登录时自动启动（`HKCU\Run`）

```powershell
.\cheesewaf-gui.exe --config .\configs\cheesewaf.yaml --data-dir .\data
```

浏览器会打开 `http://127.0.0.1:17943/`。
