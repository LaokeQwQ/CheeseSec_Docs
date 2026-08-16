---
title: 存储与调度管理
linkTitle: 存储
weight: 130
description: 内置纯 Go SQLite 存储、外部日志外发 Sink、自动化定时任务调度器与数据备份恢复。
---

CheeseWAF 采用轻量化的嵌入式存储与外部可扩展 Sink 架构，既保障单机开箱即用的极简体验，又支持企业级大规模日志归档与离线分析需求。

在 Web 管理控制台中进入 **运维调度** 与 **系统管理** 模块，底层配置项对应 `storage`、`setup.data_dir` 与 `scheduler`。

## 1. 默认存储引擎（SQLite） {#sqlite}

```yaml
setup:
  data_dir: "./data"
storage:
  sqlite:
    path: "./data/cheesewaf.db"
```

系统默认采用纯 Go 实现的 SQLite（基于 `modernc.org/sqlite`，无 CGO 依赖），用于持久化存储管理员账号、站点配置、ALAP 威胁审查样本、临时升档截止时间戳及集群节点状态。

## 2. 外部日志外发与存储 Sink {#sinks}

针对大规模高并发访问日志，CheeseWAF 支持将日志异步外发至外部存储引擎：

| 存储 Sink | 适用场景与接入说明 |
| --- | --- |
| `storage.postgresql` | 写入现有的 PostgreSQL 关系型数据库，便于与其他业务系统联动 |
| `storage.clickhouse` | 适用于海量访问日志的高性能列式存储与 OLAP 聚合分析 |
| `storage.victorialogs` | 对接 VictoriaLogs，实现轻量级日志采集与检索 |
| `storage.redis` | 用于分布式缓存或跨节点状态协调（默认处于关闭状态） |

{{% pageinfo color="info" %}}
出于防 SSRF 安全考量，外部存储地址若指向内网私有网段，需显式声明 `allow_private_endpoint: true`。在正式切换前，建议调用 `POST /api/system/storage/test` 验证后端连通性与权限。
{{% /pageinfo %}}

## 3. 定时任务调度器（Scheduler） {#scheduler}

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

## 4. 数据备份与空间回收 {#backup}

- **导出与还原**：调用 `POST /api/backup/export` 导出完整的配置与 SQLite 数据库快照；调用 `POST /api/backup/restore` 从快照文件中快速恢复系统状态。
- **磁盘清理**：在完成安全备份后，可调用 `POST /api/storage/cleanup` 与 `POST /api/system/reclaim` 清理过期的临时日志并执行 SQLite `VACUUM` 空间碎片整理。
