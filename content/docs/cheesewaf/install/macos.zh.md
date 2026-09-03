---
title: macOS 部署
linkTitle: macOS
weight: 40
description: 使用 DMG 镜像安装 CheeseWAF 桌面应用，或使用 tar.gz 压缩包以命令行方式运行。
---

在 macOS 系统下，CheeseWAF 支持桌面图形包与命令行压缩包两种运行方式：

## 1. DMG 桌面安装包 {#dmg}

适用于本地开发调试与桌面工作站环境：

1. 根据芯片架构下载安装包：Apple Silicon（M 系列芯片）选择 `cheesewaf-arm64-darwin-*.dmg`，Intel 芯片选择 `cheesewaf-amd64-darwin-*.dmg`。
2. 双击打开 DMG 镜像，将 **CheeseWAF** 拖拽至 **Applications（应用程序）** 文件夹。
3. 从启动台或应用程序文件夹中启动 CheeseWAF。

{{% pageinfo color="info" %}}
**Gatekeeper 安全验证说明**：官方正式发布的 DMG 均带有 Apple 开发者签名与公证。若使用未签名的本地开发包（Ad-hoc build）或遇到系统提示拦截，请对应用图标点按右键选择「打开」并在提示框中确认。
{{% /pageinfo %}}

程序启动后将拉起基于浏览器的本地控制器服务（监听回环地址 `http://127.0.0.1:17943/`），支持一键启动/停止主服务、查看运行状态及快速直达 Web 管理控制台。默认运行时数据目录为 `~/Library/Application Support/CheeseWAF`。

## 2. 命令行压缩包（tar.gz） {#tarball}

适用于纯终端操作或无图形界面环境：

```bash
# 解压对应架构的压缩包
tar -xzf cheesewaf-arm64-darwin-*.tar.gz
cd cheesewaf-*

# 运行终端初始化向导
./cheesewaf setup

# 启动 WAF 守护服务
./cheesewaf serve --config ./data/config/cheesewaf.yaml --data-dir ./data
```

服务启动后，使用浏览器访问 `http://127.0.0.1:9443/` 进入 Web 管理控制台登录页。
