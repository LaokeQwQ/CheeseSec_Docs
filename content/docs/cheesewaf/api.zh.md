---
title: RESTful 管理接口
linkTitle: REST API
weight: 160
description: 管理 API 鉴权机制、公开与引导流程端点清单、RBAC 细粒度权限对照表与错误响应格式。
---

CheeseWAF 的管理 API 由同一进程的**管理平面**监听器（默认端口 `9443`）承载，路径统一为 `/api`；它与承载业务流量的数据平面使用不同监听器。这里的管理平面不是未来独立的商业化控制面服务。

## 认证与鉴权方式 {#auth}

系统支持两种鉴权模式：

1. **Session 会话认证**：调用 `POST /api/auth/login` 完成登录后，客户端携带返回的 Session Cookie 进行后续请求。所有引发状态变更的非幂等请求（POST/PUT/DELETE/PATCH）均须通过 CSRF 中间件防御校验。
2. **Bearer 管理令牌**：先启用 `apisec.management_api.enabled`，再调用 `POST /api/system/api-tokens`（需要具备 `manage:api_tokens` 权限）创建具有指定范围的 API Token。在 HTTP 请求头中以 `Authorization: Bearer <TOKEN>` 发起调用。创建响应只返回一次明文；列表/查询接口只返回元数据，不返回密钥。

### 用户名与角色校验

人类账号端点（`POST /api/users`、`PUT /api/users/{id}`）、初始化、登录、存储层、人类用户 JWT claims 和 CAPTCHA receipt 使用同一套精确用户名规则：3–32 个 ASCII 字符，以 ASCII 字母开头、以 ASCII 字母或数字结尾，只允许 ASCII 字母、数字、`.`、`_` 和 `-`。非 ASCII 字符、Unicode 空白字符、控制字符（`Cc`）和格式/不可见字符（`Cf`）都会被拒绝。服务端不会去空格、转小写或以其他方式静默改写输入。

创建或更新用户时，`role` 必须精确匹配 `apisec.permissions` 中的已配置角色键（通常为 `admin` 或 `readonly`）。空值、未知角色、`*`/`:` 权限表达式，以及包含首尾或嵌入 Unicode 空白、控制字符（`Cc`）或格式/不可见字符（`Cf`）的角色都会被拒绝。字段不合法时分别返回 `USERNAME_INVALID` 或 `ROLE_INVALID`。历史上已经存在的非法用户名不能通过普通 API 更新悄悄修复；请先查询不可变用户 ID，再在本机执行 `cheesewaf user repair-username USER_ID NEW_USERNAME --reason '...'`。

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

### 首次初始化地址的安全传递 {#setup-url}

服务启动日志不会打印初始化 Token 或完整初始化地址。日志只显示基础初始化 URL（例如 `http://127.0.0.1:9443/setup`）、受保护的运行时文件路径（`setup.url`）和不含秘密的随机回执。

完整 URL 保存在 `setup.url` 中。文件权限为 `0600`，有效期为 10 分钟。初始化完成后，Token 会被撤销；过期的 `setup.url` 文件会被清理。正常安装流程不会向用户提供 `ReadURLOnce` 命令。

初始化完成前，API 仍要求在 `X-CheeseWAF-Setup-Token` Header 中提供 Token；初始化完成后，Token 会失效。浏览器从 URL fragment 读取 Token，清除地址栏中的 fragment，并且只通过该 Header 发送。启动前通过 `CHEESEWAF_SETUP_TOKEN` 提供的 Token 也遵循相同的 API 校验规则，不得写入日志或 Shell 历史。

`GET /api/setup/status` 只返回是否仍需初始化，不会返回初始化地址或初始化 Token。

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
| `read:system` / `write:system` | 系统版本查询与 NTP 时间同步；备份/还原路由已注册但当前返回 501 |
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

当前管理 API Token 支持按权限范围授权、备注、可选 TTL/失效时间、吊销、最近使用时间和一次性明文展示。平台默认有效期为 90 天，显式有效期最长 365 天。服务使用单个合并清理 worker：新建 Token 会把清理截止时间推迟 10 分钟，但不会超过本批首次创建时间加 60 分钟；已过期或连续 180 天无活动的 Token 会被删除，提交配置后会尝试写入审计记录并通知管理员。

Web 表单包含管理员 Session 下的不过期 Token 二次确认流程，并可发送一次性的 confirmation ID，但安全确认适配器接入前，不过期选项保持禁用。当前运行时尚未接入 `ApprovalGate`、当前密码/TOTP 校验和 10 秒警告阅读等待；缺少这些确认适配器时，创建不过期 Token 会返回 `API_TOKEN_CONFIRMATION_UNAVAILABLE`。这属于当前兼容边界，还不是最终的生产 TokenService。

备份路由当前不是可恢复的完整流程：`POST /api/backup/export` 与 `POST /api/backup/restore` 会返回 HTTP 501（`BACKUP_EXPORT_NOT_IMPLEMENTED` / `BACKUP_RESTORE_NOT_IMPLEMENTED`）。

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
