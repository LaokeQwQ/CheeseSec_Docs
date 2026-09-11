---
title: Storage & Scheduler Architecture
linkTitle: Storage
weight: 130
description: Embedded SQLite management storage, optional external log sinks, encrypted diagnostics, and scheduler maintenance.
---

CheeseWAF uses lightweight embedded persistence alongside optional external log sinks. The current management store is SQLite; the external sinks do not replace it.

Storage and task scheduling are managed via the **Operations** and **System** views in the Web Console (`storage`, `setup.data_dir`, and `scheduler`).

## 1. Storage profiles {#profiles}

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

`storage.profile: temporary` is the only runnable management-storage profile today. The SQLite schema stores users, admin sessions, sites, site rules, review items, notifications, promotion deadlines, TOTP replay markers, and the append-only historical-username repair audit. The runtime configuration (including management API Token hashes/metadata) remains in the YAML file; HTTP/API audit entries use the configured audit log, and AI approval state uses its separate approval store.

`storage.profile: production` is reserved for the future durable management path. It requires an independent `storage.management_postgresql.dsn`, separate from `storage.postgresql.dsn`, but startup currently fails closed with `ErrProductionStorageUnavailable` because the PostgreSQL/Coordinator/native-raft unit is not wired. Do not describe this profile as deployable.

`storage.postgresql` is an optional asynchronous access-log sink, not the management database. Redis is not wired as the Bot challenge backend; `protection.bot.challenge_backend: redis` is rejected by configuration validation.

### Configuration migration

Older configurations that omit `storage.profile` continue to resolve to `temporary`. Add the key explicitly when copying a template. Do not move the access-log DSN from `storage.postgresql.dsn` into `storage.management_postgresql.dsn`: the keys serve different roles. Adding `storage.profile: production` is not a migration path today; with a DSN present, startup still stops with `ErrProductionStorageUnavailable`.

### Versioned Schema Migrations

CheeseWAF runs an automated transaction-safe migrator. The current supported SQLite schema is version 5:

- **v1 (Initial Schema)**: Base tables for sites, users, credentials, and review queue items.
- **v2 (Review Decision Claims)**: Introduces concurrency locks and operator metadata tracking for review triage.
- **v3 (Legacy Rules to Site Custom Rules)**: Smoothly converts legacy global rule tables into standardized site-scoped custom rule collections.
- **v4 (Historical Username Repair Audit)**: Adds the append-only `user_username_repairs` table used by the explicit immutable-ID repair command; existing usernames are not rewritten.
- **v5 (User Credential Epochs)**: Adds `credential_epoch` to `users` and `admin_sessions`. Security changes advance the user epoch, and session validity requires the session epoch to match the current user epoch, so old sessions cannot remain active after a credential change.

### Concurrency & Data Integrity Guarantees

- **WAL Mode (Write-Ahead Logging)**: Configured automatically via `PRAGMA journal_mode = WAL`. Readers can proceed while a writer is active, while writes remain serialized by the single SQLite connection and bounded by the configured busy timeout.
- **Foreign Key Constraints**: Enforced by default via `PRAGMA foreign_keys = ON` to protect referential integrity.
- **Forward-Compatibility Lock (`ErrSQLiteSchemaTooNew`)**: If a database file was written by a newer CheeseWAF binary, an older daemon refuses to open it, preventing accidental schema degradation or corruption.

## 2. Redis ephemeral coordination {#redis-challenge}

Redis configuration is present for planned integrations, but the current runtime does not use Redis for Bot challenges, sessions, leases, or replay state. Enabling `storage.redis` alone does not change the active management store.

The current challenge implementation uses the configured non-Redis backend. Native-raft and a PostgreSQL management source of truth are planned commercial architecture, not active storage paths.

## 3. External Log Sinks {#sinks}

For enterprise-scale access logs, CheeseWAF streams events asynchronously to external backends:

| Storage Sink | Use Case & Integration |
| --- | --- |
| `storage.clickhouse` | High-throughput column-oriented OLAP storage for real-time aggregation across billions of records |
| `storage.victorialogs` | Lightweight log aggregation featuring high compression ratios |
| `storage.postgresql` | Standard relational database integration for corporate SIEM pipelines |
| `storage.elasticsearch` | Direct indexing into Elasticsearch or OpenSearch clusters for Kibana dashboards |
| `storage.redis` | Reserved integration; not the current Bot challenge backend |

{{% pageinfo color="info" %}}
To prevent SSRF attacks, external storage endpoints for ClickHouse, VictoriaLogs, and Elasticsearch resolving to private IP ranges require setting `allow_private_endpoint: true` (PostgreSQL and Redis drivers do not carry this field). Test connectivity via `POST /api/system/storage/test` prior to cutover.
{{% /pageinfo %}}

## 4. Automated Task Scheduler {#scheduler}

The built-in scheduler can run log cleanup, configuration snapshot, and security-report tasks. A configuration snapshot is not a complete database export, and the task is disabled by default in the source template:

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

- **Backup API status**: `POST /api/backup/export` and `POST /api/backup/restore` are registered routes, but the current handlers return HTTP 501 (`BACKUP_EXPORT_NOT_IMPLEMENTED` / `BACKUP_RESTORE_NOT_IMPLEMENTED`). Do not treat them as a restorable backup workflow. Use the SQLite online-backup procedure in [Operations & Security Hardening](../operations/#sqlite-maintenance), or the scheduler's configuration snapshot task, until a verified archive/restore format is shipped.
- **Disk Space Defragmentation**: Reclaim operations apply to the active storage profile; SQLite `VACUUM` is only used by temporary mode.

## 6. Encrypted diagnostic queue {#diagnostics}

The diagnostics broker, envelope, and queue types define the target safety contract (bounded local queue, application-side envelope encryption, TTL, and asynchronous delivery), but they are not connected to the CheeseWAF server startup path or a public upload API yet. Object-storage replication, PostgreSQL metadata, Redis locks, and offline-mode delivery pausing are prospective integrations; do not describe them as active runtime behavior.
