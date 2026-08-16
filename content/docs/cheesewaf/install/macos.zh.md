---
title: macOS 部署
linkTitle: macOS
weight: 40
description: 使用 DMG 镜像安装 CheeseWAF 桌面应用，或使用 tar.gz 压缩包以命令行方式运行。
---

在 macOS 系统下，CheeseWAF 支持桌面图形包与命令行压缩包两种运行方式：

## 1. DMG 桌面安装包 {#dmg}

适用于本地开发调试与桌面环境：

1. 根据芯片架构下载安装包：Apple Silicon（M 系列芯片）选择 `cheesewaf-*-darwin-arm64.dmg`，Intel 芯片选择 `cheesewaf-*-darwin-amd64.dmg`。
2. 双击打开 DMG 镜像，将 **CheeseWAF** 拖拽至 **Applications（应用程序）** 文件夹。
3. 从启动台或应用程序文件夹中启动 CheeseWAF。

程序启动后将在系统托盘驻留本地控制器，支持一键启动/停止服务、查看运行状态及打开 Web 控制台。默认运行时数据目录为 `~/Library/Application Support/CheeseWAF`。

## 2. 命令行压缩包（tar.gz） {#tarball}

适用于纯终端操作或无图形界面环境：

```bash
# 解压对应架构的压缩包
tar -xzf cheesewaf-*-darwin-arm64.tar.gz
cd cheesewaf-*

# 启动服务
./cheesewaf serve --config ./configs/cheesewaf.yaml --data-dir ./data
```

服务启动后，使用浏览器访问 `http://127.0.0.1:9443/setup` 进入初始化向导。
