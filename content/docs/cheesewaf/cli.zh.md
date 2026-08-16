---
title: 命令行与 TUI 交互
linkTitle: 命令行
weight: 150
description: cheesewaf 与 waf-cli 统一二进制分发命令、全局参数、子命令集及 TUI 终端界面使用说明。
---

CheeseWAF 采用单一二进制设计，通过调用文件名自动识别运行模式：

| 可执行文件名 | 默认行为与说明 |
| --- | --- |
| `cheesewaf` | 默认执行 `serve` 命令，启动 WAF 数据平面与管理服务 |
| `waf-cli` | 默认启动交互式终端图形面板（TUI，即 `panel` 命令） |

## 全局命令行参数 {#global-flags}

```text
-c, --config string     指定配置文件路径（默认 ./data/cheesewaf.yaml）
    --data-dir string   指定运行数据目录（默认 ./data）
    --lang string       界面语言偏好（en 或 zh-CN）
```

界面多语言匹配优先级为：命令行 `--lang` 参数 > 环境变量 `CHEESEWAF_LANG` > 数据目录已保存配置 > 操作系统系统区域设置。

## 子命令参考列表 {#commands}

| 子命令 | 功能说明 |
| --- | --- |
| `serve` | 启动 WAF 服务（数据平面转发 + 控制平面 API 与 Web 控制台） |
| `panel` | 启动交互式 TUI 终端控制台 |
| `status` | 查询本地服务进程运行状态与 PID |
| `healthcheck` | 执行健康检查探测（不健康时返回非 0 退出码，常用于 Docker 容器探针） |
| `stop` | 安全终止正在运行的本地服务进程 |
| `restart` | 重启本地服务进程 |
| `user` | 本地管理员账号增删改查及密码重置 |
| `cluster` | 集群节点加入、证书管理与运行时协同指令 |
| `version` | 打印当前软件版本、构建 Git Commit、发布通道与编译时间 |
| `lang` | 设置并持久化 CLI 默认语言 |
| `logs` | 实时查看或打包导出服务日志 |

## 常用操作示例 {#examples}

```bash
# 指定自定义配置文件与数据目录启动
cheesewaf serve --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf

# 检查运行状态
cheesewaf status

# 启动交互式 TUI 终端面板
waf-cli

# 管理用户与集群
cheesewaf user list
cheesewaf cluster status
```

{{% pageinfo color="info" %}}
在 Windows 环境下若需直接使用 `waf-cli` 命令名称，可将 `cheesewaf.exe` 复制或创建别名为 `waf-cli.exe`。
{{% /pageinfo %}}
