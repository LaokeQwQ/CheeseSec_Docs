---
title: REST API
linkTitle: REST API
weight: 160
description: 健康检查、会话登录、管理令牌、CSRF，以及权限对照。
---

管理 API 在 **管理监听** 的 `/api` 下，不在数据平面上。

## 认证 {#auth}

初始化之后有两种进法：

1. **会话。** `POST /api/auth/login`，然后带上会话 Cookie。改状态的请求要过 CSRF 中间件。
2. **管理令牌。** 用 `POST /api/system/api-tokens` 创建（需要 `manage:api_tokens`）。之后用 Bearer 发送。

登录前公开的接口：

| 方法 | 路径 |
| --- | --- |
| GET | `/health`、`/health/live`、`/health/ready`、`/health/cluster` |
| GET | `/api/auth/login-options` |
| POST | `/api/auth/captcha`、`/api/auth/captcha/verify`、`/api/auth/login` |
| POST | `/api/setup`、`/api/setup/probe` |
| GET/PATCH | `/api/setup/draft` |
| POST | `/api/cluster/join` |
| POST | `/api/cluster/nodes/{id}/heartbeat` |

## 权限对照 {#permissions}

路由里常见的 `require("…")` 名字：

| 前缀 | 例子 |
| --- | --- |
| `read:` / `write:` `sites` | 列出和修改站点、签发 ACME |
| `read:` / `write:` `rules` | 自定义规则 |
| `read:` / `write:` `protection` | IP、ACL、Bot、限流、审查决定 |
| `read:` / `write:` `threat_intel` | 导入、同步、查询 |
| `read:` / `write:` `edge` | 响应头 / 缓存 / 压缩策略 |
| `read:` / `write:` `ai`、`use:ai`、`approve:ai` | 配置、分析、助手、审批 |
| `read:` / `write:` `cluster` | 节点、加入令牌、滚动升级 |
| `read:` / `write:` `system` | 版本、时间同步、备份 |
| `manage:api_tokens` | 创建和吊销令牌 |
| `read:` / `write:` `users` | 本地用户和 2FA |
| `read:` `logs` | 访问日志和审查列表 |
| `read:` `monitor` | 统计、指标、通知 |
| `read:` `audit` | 审计日志 |
| `read:` `realtime` | SSE `/api/realtime/events`、WebSocket `/api/realtime/ws` |
| `read:` / `write:` `ops` | 调度器 |
| `read:` / `write:` `storage` | 统计和清理 |
| `read:` `apisec` | 已发现的接口 |

示例里的 `admin: ["*"]` 会跳过单项检查。

## 错误 {#errors}

失败时返回带错误字段的 JSON 和对应 HTTP 状态。
验证码失败后不要盲目重试登录，先重新申请挑战。
