---
title: 存储与调度管理
linkTitle: 存储
weight: 130
description: 内置 SQLite 管理存储、可选外部日志 Sink、加密诊断队列与自动化调度器。
---

CheeseWAF 使用轻量化内置存储，并支持可选的外部日志 Sink。当前管理主存储是 SQLite，外部 Sink 不会替代它。

在 Web 管理控制台中可进入 **运维调度** 与 **系统管理** 模块，底层配置项对应 `storage`、`setup.data_dir` 与 `scheduler`。

## 1. 存储配置分层 {#profiles}

```yaml
setup:
  data_dir: "./data"
storage:
  profile: temporary
  management_postgresql:
    dsn: ""
    timeout: 10s
  sqlite:
    path: "./data/cheesewaf.db"
```

当前只有 `storage.profile: temporary` 可以运行。SQLite 表保存用户、管理端 Session、站点、站点规则、审查队列、通知、临时升档截止时间、TOTP 防重放标记，以及只追加的历史用户名修复审计。运行时配置（包括管理 API Token 的哈希和元数据）仍保存在 YAML 文件中；HTTP/API 审计记录写入配置的审计日志，AI 审批状态使用独立的审批存储。

`storage.profile: production` 预留给未来的持久管理路径。它必须填写独立的 `storage.management_postgresql.dsn`，不能复用 `storage.postgresql.dsn`。但由于 PostgreSQL、Coordinator 和 native-raft 尚未作为一个启动单元接线，当前启动会以 `ErrProductionStorageUnavailable` 失败。请不要把这个配置写成可部署方案。

`storage.postgresql` 只是可选的异步访问日志 Sink，不是管理数据库。Redis 尚未接入 Bot 挑战后端；配置校验会拒绝 `protection.bot.challenge_backend: redis`。

### 配置迁移说明

旧配置如果没有 `storage.profile`，当前仍会按 `temporary` 处理。复制模板时建议显式写出该键。不要把访问日志 DSN 从 `storage.postgresql.dsn` 移到 `storage.management_postgresql.dsn`，这两个配置承担不同职责。现在不能通过添加 `storage.profile: production` 完成迁移；即使填写 DSN，启动仍会因 `ErrProductionStorageUnavailable` 停止。

### 自动化版本迁移（Versioned Schema Migrations）

CheeseWAF 内置了自动事务迁移器。当前支持的 SQLite Schema 版本为 5：

- **v1 (Initial Schema)**：初始化站点、用户、凭证与审查队列基础表结构。
- **v2 (Review Decision Claims)**：引入威胁审查处置决策索赔与操作者元数据追踪，防并发重复处置。
- **v3 (Legacy Rules to Site Custom Rules)**：将早期版本的旧式全局规则表平滑迁移并转换为标准化的站点专属自定义规则结构。
- **v4 (Historical Username Repair Audit)**：新增只追加的 `user_username_repairs` 表，供按不可变用户 ID 执行的历史用户名修复命令记录；不会自动改写现有用户名。
- **v5 (User Credential Epochs)**：为 `users` 和 `admin_sessions` 增加 `credential_epoch`。账号安全信息变化时会递增用户 epoch；Session 只有在 epoch 与当前用户一致时才有效，因此旧 Session 不会在凭据变化后继续使用。

### 数据库性能与完整性保障

- **WAL 模式（Write-Ahead Logging）**：数据库连接建立时自动执行 `PRAGMA journal_mode = WAL`。写入期间读操作可以继续，但写操作仍由单一 SQLite 连接串行执行，并受有界 busy timeout 限制。
- **外键约束（Foreign Keys）**：强制开启 `PRAGMA foreign_keys = ON`，保障多表关联的引用完整性。
- **向前兼容安全锁（`ErrSQLiteSchemaTooNew`）**：当数据库文件曾被更高版本的 CheeseWAF 写入时，低版本二进制将主动拒绝打开并报错退出，防止老程序破坏新版数据库架构。

## 2. Redis 临时协调 {#redis-challenge}

Redis 配置为后续集成预留。当前运行时不会用 Redis 保存 Bot 挑战、会话、租约或重放状态。单独启用 `storage.redis` 不会改变当前管理主存储。

当前挑战功能使用已配置的非 Redis 后端。native-raft 和 PostgreSQL 管理主存储属于商业化规划，尚未接入实际存储路径。

## 3. 外部日志外发与存储 Sink {#sinks}

针对大规模高并发访问日志，CheeseWAF 支持将日志异步外发至外部存储引擎：

| 存储 Sink | 适用场景与接入说明 |
| --- | --- |
| `storage.clickhouse` | 适用于海量访问日志的高性能列式存储与 OLAP 聚合秒级检索分析 |
| `storage.victorialogs` | 对接 VictoriaLogs，实现极致压缩比的轻量级日志采集与检索 |
| `storage.postgresql` | 写入现有的 PostgreSQL 关系型数据库，便于与外部业务系统联动 |
| `storage.elasticsearch` | 写入 Elasticsearch / OpenSearch 索引，结合 Kibana 进行日志检索与分析 |
| `storage.redis` | 预留集成；当前不是 Bot 挑战后端 |

{{% pageinfo color="info" %}}
出于防 SSRF 安全考量，ClickHouse、VictoriaLogs 与 Elasticsearch 外部存储地址若指向内网私网地址，需显式声明 `allow_private_endpoint: true`（PostgreSQL 与 Redis 直连驱动无此限制）。在正式切换前，建议调用 `POST /api/system/storage/test` 验证后端连通性与权限。
{{% /pageinfo %}}

## 4. 定时任务调度器（Scheduler） {#scheduler}

内置调度器可以执行日志清理、配置快照和安全日报任务。配置快照不是完整数据库导出，而且源码模板默认关闭该任务：

```yaml
scheduler:
  enabled: true
  tasks:
    - id: "log-cleanup"
      type: "cleanup"
      every: 24h
      target: "./logs"
      keep: 14
      enabled: true
    - id: "config-backup"
      type: "backup"
      every: 24h
      target: "./data/backups"
      keep: 7
      enabled: false
    - id: "security-daily-report"
      type: "security_report"
      frequency: "daily"
      at: "08:00"
      enabled: false
```

- **任务管理**：调用 `GET /api/scheduler/tasks` 与 `PUT /api/scheduler/tasks` 查询和修改调度任务列表。
- **执行历史**：调用 `GET /api/scheduler/history` 查看历史任务执行耗时与执行状态。

## 5. 数据备份与空间回收 {#backup}

- **备份 API 状态**：`POST /api/backup/export` 和 `POST /api/backup/restore` 已注册路由，但当前处理器固定返回 HTTP 501（`BACKUP_EXPORT_NOT_IMPLEMENTED` / `BACKUP_RESTORE_NOT_IMPLEMENTED`），不能当作可恢复备份流程。正式归档/恢复格式交付前，请使用[系统运维与安全加固](../operations/#sqlite-maintenance)中的 SQLite 在线备份步骤，或使用调度器的配置快照任务。
- **磁盘回收**：回收操作按当前存储模式执行；SQLite `VACUUM` 仅适用于临时模式。

## 6. 加密诊断队列 {#diagnostics}

诊断 broker、信封和队列类型定义了目标安全 contract（有界本地队列、应用侧信封加密、TTL 与异步投递），但当前尚未接入 CheeseWAF 服务启动路径，也没有公开上传 API。对象存储复制、PostgreSQL 元数据、Redis 锁和离线暂停外发都属于后续集成，不能写成当前运行时行为。
