---
title: 命令行和 TUI
linkTitle: 命令行
weight: 150
description: cheesewaf 和 waf-cli 是同一个二进制。默认命令取决于文件名。
---

同一个二进制认两个名字。

| 调用名 | 默认命令 |
| --- | --- |
| `cheesewaf` | `serve` |
| `waf-cli` | 交互式 TUI（`panel`） |

全局参数：

```text
-c, --config     cheesewaf.yaml 路径（默认 ./data/cheesewaf.yaml）
    --data-dir   运行数据目录（默认 ./data）
    --lang       en 或 zh-CN
```

语言顺序：命令行参数，然后环境变量，然后数据目录，然后操作系统区域。

## 子命令 {#commands}

| 命令 | 作用 |
| --- | --- |
| `serve` | 启动 WAF |
| `panel` | TUI |
| `status` | 进程在不在 |
| `healthcheck` | 不健康时非 0 退出（Compose 用这个） |
| `stop` | 停掉正在跑的进程 |
| `restart` | 先停再 serve |
| `user` | 管理本地用户 |
| `cluster` | 加入、证书、运行时 |
| `version` | 版本、通道、构建时间 |
| `lang` | 记住 CLI 语言 |
| `logs` | 打包或查看日志 |

例子：

```bash
cheesewaf serve --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf
cheesewaf status
waf-cli
cheesewaf user
cheesewaf cluster
```

在 Windows 上，如果要用 TUI 这个名字，把 `cheesewaf.exe` 复制成 `waf-cli.exe`。
桌面控制器是 **另一个** 二进制：见 [Windows 安装](../install/windows/#gui)。
