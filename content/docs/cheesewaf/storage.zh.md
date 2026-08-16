---
title: 存储与调度
linkTitle: 存储
weight: 130
description: SQLite、可选的 PostgreSQL 和日志外发、备份、清理和定时报告。
---

配置：`storage`、`setup.data_dir`、`scheduler`。
控制台：**运维**、**系统**。
REST：`/api/storage`、`/api/backup/*`、`/api/scheduler/*`。

## 默认库 {#sqlite}

```yaml
setup:
  data_dir: "./data"
storage:
  sqlite:
    path: "./data/cheesewaf.db"
```

SQLite 保存用户、审查条目、升档截止时间和运行状态。
它用 `modernc.org/sqlite`（无 CGO）。

## 额外外发 {#sinks}

| 目标 | 什么时候开 |
| --- | --- |
| `storage.postgresql` | 把日志写到已有的 Postgres |
| `storage.clickhouse` | 大量日志分析 |
| `storage.victorialogs` | VictoriaLogs HTTP 接入 |
| `storage.redis` | 可选缓存 / 协调。示例里是关的 |

除非 `allow_private_endpoint` 为真，否则私网地址会被拦住。
切换之前先用 `POST /api/system/storage/test` 测后端。

## 调度器 {#scheduler}

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

`GET /api/scheduler/tasks` 和 `PUT /api/scheduler/tasks` 改任务列表。
`GET /api/scheduler/history` 看执行记录。

## 备份 {#backup}

`POST /api/backup/export` 下载备份。
`POST /api/backup/restore` 恢复备份。
有备份之后，再用 `POST /api/storage/cleanup` 和 `POST /api/system/reclaim` 清磁盘。
