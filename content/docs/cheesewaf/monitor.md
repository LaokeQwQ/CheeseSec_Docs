---
title: "Observability: Logs, Prometheus & Threat Map"
linkTitle: Monitoring
weight: 110
description: Access log rotation, Prometheus metrics exporter, custom alert notifications, and real-time geographic threat visualizer.
---

CheeseWAF delivers end-to-end observability out of the box, including structured access logs, standard Prometheus metric outputs, multi-channel alert dispatching, and a real-time global threat visualizer.

Access these tools visually under **Dashboard**, **Logs**, **Monitor**, and **Attack Map** in the Web console, or configure them under `logging` and `monitor`.

## 1. Structured Access Logging {#logs}

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

- **Log Rotation & Retention**: Automatically rotates log files based on size (`max_size`) and retains a configurable number of historical backups (`max_backups`).
- **Trace ID End-to-End Tracking**: Every request log entry contains a globally unique `traceId`. Accessing `/logs/{traceId}` in the console displays the complete rule evaluation and AST assertion chain for that transaction.
- **Log Sinks**: Stream logs to ClickHouse, PostgreSQL, or VictoriaLogs for long-term retention. See [Storage Sinks & Task Scheduling](../storage/).

## 2. Prometheus Metrics Export {#prometheus}

```yaml
monitor:
  prometheus:
    enabled: true
    path: "/metrics"
    public: false
```

- **Metric Scrape Endpoints**: When `public: false`, scrape `/api/metrics` using an authorized Bearer token. When set to `public: true`, metrics are exposed on the root router path without authentication (recommended only on isolated internal monitoring networks).
- **Prometheus Remote Write**: Use `monitor.remote_write` to actively push time-series metrics to Prometheus Remote Write-compatible backends.

## 3. Alerting Rules & Notification Channels {#alerts}

CheeseWAF includes built-in alert definitions for blocking rate anomalies (`high-block-rate`) and disk space limits (`disk-usage`):

- **Notification Channels**: Configure Webhook endpoints, emails, or enterprise chat bots (DingTalk, WeChat Work, Lark) under `monitor.notifiers`.
- **In-App Notifications**: Internal operational alerts are stored in the system and queryable via `/api/notifications`.

## 4. Real-Time Geographic Threat Map {#map}

Navigate to `/attack-map` or the fullscreen visualizer at `/attack-map/screen` in the Web console to view real-time geographic attack origin maps, blocking frequencies, and threat classification charts.

{{% pageinfo color="info" %}}
Set `console.map.china_boundary` to load official national boundary data files. When configuring external map source URLs, maintain `allow_insecure: false` and `allow_private: false` to prevent SSRF security issues.
{{% /pageinfo %}}
