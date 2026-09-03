---
title: Storage & Scheduler Architecture
linkTitle: Storage
weight: 130
description: Pure-Go SQLite versioned migrations, Redis challenge store backend, external logging sinks, and automated scheduler maintenance.
---

CheeseWAF utilizes a lightweight embedded persistence layer alongside scalable external sinks. This combines single-node out-of-the-box convenience with distributed cluster support and high-throughput log aggregation.

Storage and task scheduling are managed via the **Operations** and **System** views in the Web Console (`storage`, `setup.data_dir`, and `scheduler`).

## 1. Embedded SQLite & Versioned Schema Migrations {#sqlite}

```yaml
setup:
  data_dir: "./data"
storage:
  sqlite:
    path: "./data/cheesewaf.db"
```

The primary metadata store is pure-Go SQLite (powered by `modernc.org/sqlite`, with zero CGO dependencies). It persists administrative accounts, site configurations, ALAP threat samples, temporary escalation deadlines, and cluster topology.

### Versioned Schema Migrations

To guarantee seamless upgrades across releases, CheeseWAF runs an automated transaction-safe migrator (`sqliteSchemaVersion = 3`):

- **v1 (Initial Schema)**: Base tables for sites, users, credentials, and review queue items.
- **v2 (Review Decision Claims)**: Introduces concurrency locks and operator metadata tracking for review triage.
- **v3 (Legacy Rules to Site Custom Rules)**: Smoothly converts legacy global rule tables into standardized site-scoped custom rule collections.

### Concurrency & Data Integrity Guarantees

- **WAL Mode (Write-Ahead Logging)**: Configured automatically via `PRAGMA journal_mode = WAL`. Concurrent reads and writes execute without database lock contention.
- **Foreign Key Constraints**: Enforced by default via `PRAGMA foreign_keys = ON` to protect referential integrity.
- **Forward-Compatibility Lock (`ErrSQLiteSchemaTooNew`)**: If a database file was written by a newer CheeseWAF binary, an older daemon refuses to open it, preventing accidental schema degradation or corruption.

## 2. Distributed Redis Backend (Bot Challenge Store) {#redis-challenge}

For distributed clusters fronting high-concurrency traffic, CheeseWAF supports storing bot challenge state in Redis (`storage.redis`):

- **Transactional Capacity Reservation**: Generating CAPTCHA puzzles follows a transactional contract (`ReserveScoped` -> `Start` -> `Commit` / `Rollback`) to prevent attackers from exhausting server entropy and CPU by flooding challenge requests.
- **Atomic Replay Prevention**: Challenge tokens (JTI) are marked consumed atomically, immediately invalidating them across all cluster nodes.

## 3. External Log Sinks {#sinks}

For enterprise-scale access logs, CheeseWAF streams events asynchronously to external backends:

| Storage Sink | Use Case & Integration |
| --- | --- |
| `storage.clickhouse` | High-throughput column-oriented OLAP storage for real-time aggregation across billions of records |
| `storage.victorialogs` | Lightweight log aggregation featuring high compression ratios |
| `storage.postgresql` | Standard relational database integration for corporate SIEM pipelines |
| `storage.elasticsearch` | Direct indexing into Elasticsearch or OpenSearch clusters for Kibana dashboards |
| `storage.redis` | Distributed state coordination and cross-node session lookups |

{{% pageinfo color="info" %}}
To prevent SSRF attacks, endpoints resolving to private IP ranges require setting `allow_private_endpoint: true`. Test connectivity via `POST /api/system/storage/test` prior to cutover.
{{% /pageinfo %}}

## 4. Automated Task Scheduler {#scheduler}

The built-in cron scheduler handles log rotation, backups, and security digest generation:

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

- **Task Management**: Query and adjust task schedules via `GET/PUT /api/scheduler/tasks`.
- **Execution History**: Inspect execution durations and exit statuses via `GET /api/scheduler/history`.

## 5. Backup & Space Recovery {#backup}

- **Export & Restore**: Call `POST /api/backup/export` to download full SQLite database and configuration archives; restore using `POST /api/backup/restore`.
- **Disk Space Defragmentation**: After pruning rotated logs, invoke `POST /api/system/reclaim` to trigger SQLite `VACUUM` and return unused disk pages to the host OS.
