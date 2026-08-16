---
title: Monitor, logs, and attack map
linkTitle: Monitor
weight: 110
description: Dashboard stats, access logs, Prometheus, alerts, notifications, and the attack map.
---

Console: **Dashboard**, **Logs**, **Monitor**, **Attack map**.
Config: `logging`, `monitor`.
REST: `/api/stats`, `/api/logs`, `/api/monitor`, `/api/metrics`, `/api/notifications`, `/api/audit`.

## Logs {#logs}

```yaml
logging:
  level: "info"
  format: "json"
  output:
    type: "file"
    file:
      path: "./logs/access.log"
      max_size: "100MB"
      max_backups: 10
```

`GET /api/logs` lists events.
`/logs/{traceId}` in the console opens one request.

Optional sinks: PostgreSQL, ClickHouse, VictoriaLogs. See [Storage](../storage/).

## Prometheus {#prometheus}

```yaml
monitor:
  prometheus:
    enabled: true
    path: "/metrics"
    public: false
```

When `public` is false, scrape `/api/metrics` with a management token.
When `public` is true, the same path is exposed on the router root. Do not do that on the internet.

`monitor.remote_write` can push to a remote Prometheus-compatible endpoint.

## Alerts {#alerts}

The sample defines `high-block-rate` and `disk-usage` rules.
Notifiers support webhook endpoints (`monitor.notifiers`).
In-app notifications use `/api/notifications`.

## Attack map {#map}

`/attack-map` and `/attack-map/screen` plot recent blocks.
`console.map.china_boundary` can load a reviewed China boundary file.
Do not point `source` at an untrusted URL (`allow_insecure` / `allow_private` stay false unless you know why).
