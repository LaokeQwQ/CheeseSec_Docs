---
title: 统一管理入口与权限模型
linkTitle: 管理入口
weight: 40
description: 解析 Web 控制台、TUI 终端界面与 REST API 共享的 RBAC 鉴权模型、会话机制与审计链路。
---

CheeseWAF 提供了三种各司其职的管理入口，满足可视化运维、无图形终端交互及 CI/CD 自动化集成等多种场景：

| 管理入口 | 定位与适用场景 | 访问与调用方式 |
| --- | --- | --- |
| **Web 控制台** | 日常可视化运维、防护策略配置、实时日志检索与攻击态势大屏 | 完成系统初始化后，浏览器访问 `http://127.0.0.1:9443/` |
| **命令行 / TUI** | 纯命令行服务器、跳板机无图形环境下的快速状态排查与配置热修 | 执行 `waf-cli` 或 `cheesewaf panel` 启动终端交互界面 |
| **RESTful API** | CI/CD 自动化编排、监控告警对接及第三方运维平台集成 | 调用 `/api/...` 端点，支持会话 Cookie 或 Bearer 管理令牌鉴权 |

## 三端统一鉴权机制 {#unified-auth}

当配置文件中启用 `setup.three_end_unified: true` 时，CheeseWAF 实现了三大管理入口的用户体系与权限闭环：

- **用户身份通用**：在 Web 控制台创建的管理员或普通用户账号，可直接用于 TUI 命令行登录与 API 鉴权。
- **统一 RBAC 授权**：在控制台“系统管理”中生成的 API Token，遵从与用户角色相同的 RBAC 权限矩阵（定义于 `apisec.permissions`）。
- **细粒度角色划分**：系统默认预设 `admin`（拥有 `["*"]` 全量权限）与 `readonly`（拥有 `["read:*", "read:cluster"]` 等只读权限）等角色。

## 操作审计链路 {#audit}

当开启 `apisec.audit.enabled: true` 时，所有通过 Web 控制台、TUI 终端以及 REST API 执行的配置变更、策略启停及用户管理操作，均会结构化写入 `apisec.audit.path` 指定的审计日志文件中，确保生产环境运维操作的可追溯性。

## 相关模块参考 {#references}

- [Web 控制台使用指南](../../console/)
- [命令行与 TUI 交互手册](../../cli/)
- [REST API 接口与权限对照表](../../api/)
