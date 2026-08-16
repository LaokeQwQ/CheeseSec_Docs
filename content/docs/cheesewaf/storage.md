---
title: Storage and scheduler
linkTitle: Storage
weight: 130
description: SQLite, optional PostgreSQL and log sinks, backups, cleanup, and scheduled reports.
---

Config: `storage`, `setup.data_dir`, `scheduler`.
Console: **Operations**, **System**.
REST: `/api/storage`, `/api/backup/*`, `/api/scheduler/*`.

## Default store {#sqlite}

```yaml
setup:
  data_dir: "./data"
storage:
  sqlite:
    path: "./data/cheesewaf.db"
```

SQLite holds users, review items, promote deadlines, and operational state.
It uses `modernc.org/sqlite` (no CGO).

## Extra sinks {#sinks}

| Sink | When to enable |
| --- | --- |
| `storage.postgresql` | Share logs with an existing Postgres |
| `storage.clickhouse` | High-volume log analytics |
| `storage.victorialogs` | VictoriaLogs HTTP ingest |
| `storage.redis` | Optional cache / coordination. Off in the sample |

Private endpoints stay blocked unless `allow_private_endpoint` is true.
`POST /api/system/storage/test` checks a backend before you switch.

## Scheduler {#scheduler}

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

`GET /api/scheduler/tasks` and `PUT /api/scheduler/tasks` edit the list.
`GET /api/scheduler/history` shows runs.

## Backup {#backup}

`POST /api/backup/export` downloads a backup.
`POST /api/backup/restore` applies one.
`POST /api/storage/cleanup` and `POST /api/system/reclaim` free disk after you have a backup.
