---
title: 存储与调度管理
linkTitle: 存储
weight: 130
description: 内置纯 Go SQLite 版本化迁移引擎、Redis 状态驱动、外部日志外发 Sink 与自动化调度器。
---

CheeseWAF 采用轻量化的嵌入式存储与外部可扩展 Sink 架构，既保障单机开箱即用的极简体验，又支持企业级分布式集群与大规模日志离线分析需求。

在 Web 管理控制台中可进入 **运维调度** 与 **系统管理** 模块，底层配置项对应 `storage`、`setup.data_dir` 与 `scheduler`。

## 1. 默认存储引擎与 SQLite 版本化迁移 {#sqlite}

```yaml
setup:
  data_dir: "./data"
storage:
  sqlite:
    path: "./data/cheesewaf.db"
```

系统默认采用纯 Go 实现的 SQLite（基于 `modernc.org/sqlite`，无需任何 CGO 依赖），用于持久化存储系统用户凭证、站点配置、ALAP 威胁审查样本、临时升档截止时间戳及集群拓扑。

### 自动化版本迁移（Versioned Schema Migrations）

为了确保系统平滑升级，CheeseWAF 内置了自动模式迁移器（当前版本号 `sqliteSchemaVersion = 3`）：

- **v1 (Initial Schema)**：初始化站点、用户、凭证与审查队列基础表结构。
- **v2 (Review Decision Claims)**：引入威胁审查处置决策索赔与操作者元数据追踪，防并发重复处置。
- **v3 (Legacy Rules to Site Custom Rules)**：将早期版本的旧式全局规则表平滑迁移并转换为标准化的站点专属自定义规则结构。

### 数据库性能与完整性保障

- **WAL 模式（Write-Ahead Logging）**：数据库连接建立时自动执行 `PRAGMA journal_mode = WAL`，读写操作互不阻塞，支持高并发审计写入。
- **外键约束（Foreign Keys）**：强制开启 `PRAGMA foreign_keys = ON`，保障多表关联的引用完整性。
- **向前兼容安全锁（`ErrSQLiteSchemaTooNew`）**：当数据库文件曾被更高版本的 CheeseWAF 写入时，低版本二进制将主动拒绝打开并报错退出，防止老程序破坏新版数据库架构。

## 2. 分布式 Redis 状态驱动（Bot 挑战后端） {#redis-challenge}

在多节点集群或高并发防 CC 场景下，系统支持通过 Redis 托管分布式 Bot 挑战与人机验证码状态（`storage.redis`）：

- **分布式租约与并发预占**：挑战签发采用严格的事务性容量扣减机制（`ReserveScoped` -> `Start` -> `Commit` / `Rollback`），防止恶意攻击者并发刷取挑战题目耗尽服务器熵池与计算资源。
- **天然防重放**：验证码 Token（JTI）在消费后立即原子标记销毁，跨集群节点毫秒级同步失效。

## 3. 外部日志外发与存储 Sink {#sinks}

针对大规模高并发访问日志，CheeseWAF 支持将日志异步外发至外部存储引擎：

| 存储 Sink | 适用场景与接入说明 |
| --- | --- |
| `storage.clickhouse` | 适用于海量访问日志的高性能列式存储与 OLAP 聚合秒级检索分析 |
| `storage.victorialogs` | 对接 VictoriaLogs，实现极致压缩比的轻量级日志采集与检索 |
| `storage.postgresql` | 写入现有的 PostgreSQL 关系型数据库，便于与外部业务系统联动 |
| `storage.elasticsearch` | 写入 Elasticsearch / OpenSearch 索引，结合 Kibana 进行日志检索与分析 |
| `storage.redis` | 用于分布式状态协调与跨节点会话同步 |

{{% pageinfo color="info" %}}
出于防 SSRF 安全考量，外部存储地址若指向内网私有网段，需显式声明 `allow_private_endpoint: true`。在正式切换前，建议调用 `POST /api/system/storage/test` 验证后端连通性与权限。
{{% /pageinfo %}}

## 4. 定时任务调度器（Scheduler） {#scheduler}

内置调度器支持执行日志轮转清理、配置备份与安全日报生成：

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

- **导出与还原**：调用 `POST /api/backup/export` 导出完整的配置与 SQLite 数据库快照；调用 `POST /api/backup/restore` 从快照文件中快速恢复系统状态。
- **磁盘碎片整理**：在完成日志清理后，可调用 `POST /api/system/reclaim` 清理过期的临时缓存并执行 SQLite `VACUUM` 回收物理磁盘空间。
