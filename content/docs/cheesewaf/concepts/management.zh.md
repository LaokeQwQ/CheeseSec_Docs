---
title: 三种管理入口
linkTitle: 管理入口
weight: 40
description: Web 控制台、命令行 / TUI 和 REST 共用同一套用户、会话和审计。
---

| 入口 | 适用场合 | 怎么进 |
| --- | --- | --- |
| Web 控制台 | 日常运维、规则、日志、攻击地图 | 初始化后打开 `http://127.0.0.1:9443/` |
| 命令行 / TUI | 无图形主机、脚本 | `waf-cli` 或 `cheesewaf panel` |
| REST | 自动化、CI | `/api/...`，用会话 Cookie 或管理 API 令牌 |

示例配置里 `setup.three_end_unified` 是打开的。
控制台创建的用户可以用命令行。
在 **系统** 里创建的令牌，可以按同一套 RBAC 调 REST。

权限在 `apisec.permissions`。
示例给 `admin: ["*"]`，给 `readonly: ["read:*", "read:cluster"]`。

`apisec.audit.enabled` 为真时，审计写到 `apisec.audit.path`。

见 [控制台](../../console/)、[命令行](../../cli/) 和 [REST API](../../api/)。
