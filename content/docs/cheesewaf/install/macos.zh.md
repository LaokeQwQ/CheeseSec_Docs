---
title: macOS
linkTitle: macOS
weight: 40
description: 用 DMG 安装 CheeseWAF，或直接跑 tar.gz 命令行。
---

## DMG {#dmg}

1. 下载 `cheesewaf-*-darwin-arm64.dmg`（Apple Silicon）或 `cheesewaf-*-darwin-amd64.dmg`（Intel）。
2. 打开镜像，把 **CheeseWAF** 拖进 **应用程序**。
3. 从启动台或「应用程序」打开 CheeseWAF。

应用会启动本地控制器。
用它启动、停止，并打开 Web 控制台。

运行数据在 `~/Library/Application Support/CheeseWAF`。

## 命令行包 {#tarball}

只要命令行时：

```bash
tar -xzf cheesewaf-*-darwin-arm64.tar.gz
cd cheesewaf-*
./cheesewaf serve --config ./configs/cheesewaf.yaml --data-dir ./data
```

然后打开 `http://127.0.0.1:9443/setup`。
