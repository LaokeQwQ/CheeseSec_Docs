---
title: Storage Sinks & Task Scheduling
linkTitle: Storage
weight: 130
description: Embedded CGO-free SQLite storage, external log sinks, automated task scheduler, and database backup/recovery.
---

CheeseWAF combines an embedded, zero-dependency storage layer for turnkey operations with an extensible sink architecture for enterprise-grade log streaming and offline security analytics.

Manage storage and task jobs visually in the Web console under **Operations** and **System**, or configure settings under `storage`, `setup.data_dir`, and `scheduler`.

## 1. Default Storage Engine (SQLite) {#sqlite}

```yaml
setup:
  data_dir: "./data"
storage:
  sqlite:
    path: "./data/cheesewaf.db"
```

The system utilizes a pure-Go embedded SQLite engine (via `modernc.org/sqlite`, with zero CGO dependencies) to persist administrator credentials, site definitions, ALAP threat review items, auto-promotion deadlines, and cluster consensus states.

## 2. External Log Sinks & Storage Integrations {#sinks}

To accommodate high-throughput log analytics, CheeseWAF supports streaming access and security logs asynchronously to external storage backends:

| Storage Sink | Best Suited For & Description |
| --- | --- |
| `storage.postgresql` | Streams structured logs to an existing PostgreSQL relational database |
| `storage.clickhouse` | High-performance columnar storage for petabyte-scale access log analytics |
| `storage.victorialogs` | Ingests logs into VictoriaLogs for lightweight log aggregation and querying |
| `storage.redis` | Optional distributed cache and state coordination backend (disabled by default) |

{{% pageinfo color="info" %}}
To prevent SSRF risks, external storage endpoints targeting private RFC1918 IP addresses require setting `allow_private_endpoint: true`. Test backend connectivity before switching by invoking `POST /api/system/storage/test`.
{{% /pageinfo %}}

## 3. Automated Task Scheduler {#scheduler}

The built-in task scheduler automates access log retention cleanup, database backups, and daily threat reports:

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

- **Task Management**: Query and update scheduled jobs via `GET /api/scheduler/tasks` and `PUT /api/scheduler/tasks`.
- **Execution History**: View job execution timestamps, durations, and exit statuses via `GET /api/scheduler/history`.

## 4. Data Backup & Storage Reclamation {#backup}

- **Export & Restore**: Call `POST /api/backup/export` to export an encrypted snapshot of configuration and SQLite databases; call `POST /api/backup/restore` to restore state from a snapshot.
- **Disk Reclamation**: After creating a backup, call `POST /api/storage/cleanup` and `POST /api/system/reclaim` to purge rotated logs and run SQLite `VACUUM` space reclamation.
