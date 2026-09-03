---
title: RESTful 管理接口
linkTitle: REST API
weight: 160
description: 管理 API 鉴权机制、公开与引导流程端点清单、RBAC 细粒度权限对照表与错误响应格式。
---

CheeseWAF 的管理 API 统一部署于 **管理平面**（默认端口 `9443`）的 `/api` 路径下，与承载业务流量的数据平面完全隔离。

## 认证与鉴权方式 {#auth}

系统支持两种鉴权模式：

1. **Session 会话认证**：调用 `POST /api/auth/login` 完成登录后，客户端携带返回的 Session Cookie 进行后续请求。所有引发状态变更的非幂等请求（POST/PUT/DELETE/PATCH）均须通过 CSRF 中间件防御校验。
2. **Bearer 管理令牌**：调用 `POST /api/system/api-tokens` 创建具有指定权限范围的长期或临时 API Token（需要具备 `manage:api_tokens` 权限），在 HTTP 请求头中以 `Authorization: Bearer <TOKEN>` 发起调用。

### 公开免密端点清单

以下只读、登录或挑战接口无需已有会话或 Bearer 令牌即可访问。若配置 `monitor.prometheus.public: true`，对应的 Prometheus 路径也会免密开放（路径由部署配置决定）。

| HTTP 方法 | 接口路径 | 用途说明 |
| --- | --- | --- |
| `GET` | `/health`、`/health/live`、`/health/ready`、`/health/cluster` | 探针健康检查端点 |
| `GET` | `/api/auth/login-options` | 获取登录配置（如是否启用验证码、2FA 等） |
| `POST` | `/api/auth/captcha`、`/api/auth/captcha/verify` | 登录人机验证码获取与预校验 |
| `POST` | `/api/auth/login` | 管理员登录接口 |
| `GET` | `/api/setup/status` | 查询是否仍需首次初始化；该接口不修改状态 |

### 引导流程与节点鉴权接口

这些路由虽然不经过常规管理令牌中间件，但**并非匿名操作**：

- `POST /api/setup` 与 `POST /api/setup/probe` 必须在请求头 `X-CheeseWAF-Setup-Token` 中提供初始化令牌，且仅在系统尚未完成初始化时接受。
- `GET /api/setup/draft` 必须携带探测阶段下发的初始化会话 Cookie；`PATCH /api/setup/draft` 同时需要该 Cookie 与初始化令牌。
- `POST /api/cluster/join` 必须提供一次性加入令牌与节点 CSR；控制器会校验令牌并完成节点注册，并非公开的集群成员接口。
- `POST /api/cluster/nodes/{id}/heartbeat` 仅接受已注册且未吊销节点的已验证 mTLS 客户端证书（证书身份/序列号必须与注册信息一致）。

## RBAC 细粒度权限对照表 {#permissions}

后端路由中间件通过权限标识符对 API 调用进行细粒度鉴权：

| 权限标识前缀 | 覆盖功能模块与操作范围 |
| --- | --- |
| `read:sites` / `write:sites` | 站点列表查询、站点增删改查及 ACME 证书申请 |
| `read:rules` / `write:rules` | 自定义正则表达式防护规则管理 |
| `read:protection` / `write:protection` | IP 黑白名单、ACL 访问控制、Bot 挑战策略及威胁审查研判 |
| `read:threat_intel` / `write:threat_intel` | 威胁情报库导入、自动化同步与 IP 威胁查询 |
| `read:edge` / `write:edge` | 边缘响应头改写、静态缓存与内容压缩策略 |
| `read:ai` / `write:ai` / `use:ai` / `approve:ai` | AI 大模型连接配置、智能助手对话发起与高危工具审批 |
| `read:cluster` / `write:cluster` | 集群节点监控、加入令牌签发与滚动升级编排 |
| `read:system` / `write:system` | 系统版本查询、NTP 时间同步与数据备份还原 |
| `manage:api_tokens` | 管理 API Token 的创建、查询与吊销 |
| `read:users` / `write:users` | 管理员账号增删改查及 TOTP 双因素认证配置 |
| `read:logs` | 访问日志查询与威胁审查列表拉取 |
| `read:monitor` | 监控指标查询、Prometheus Metrics 导出与通知渠道配置 |
| `read:audit` | 系统操作审计日志检索 |
| `read:realtime` | SSE 实时事件流（`/api/realtime/events`）与 WebSocket 连接 |
| `read:ops` / `write:ops` | 定时任务调度器与日常维护任务管理 |
| `read:storage` / `write:storage` | 存储状态查询、日志 Sink 配置与磁盘空间清理 |
| `read:apisec` | API 资产发现列表与 Schema 结构定义查询 |

拥有 `admin: ["*"]` 权限的角色具备全量接口调用权限。

## 错误响应规范 {#errors}

API 调用失败时，将返回对应的 HTTP 状态码与标准 JSON 错误响应体：

```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid request parameter",
    "trace_id": "1a2b3c4d5e6f",
    "event_id": "1a2b3c4d5e6f"
  }
}
```

在遇到登录验证码校验失败（401/403）时，请先调用 `/api/auth/captcha` 刷新挑战上下文，再重新提交登录凭据。
