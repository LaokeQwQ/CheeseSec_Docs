---
title: Observability, Logging & Threat Attack Map
linkTitle: Monitoring
weight: 110
description: Access log rotation, Prometheus metrics and Remote Write protobuf streaming, alerts, and 100% offline air-gapped threat attack maps.
---

CheeseWAF provides end-to-end observability, including structured JSON access logs, standard Prometheus metrics, multi-channel alerting, and an interactive real-time threat attack map.

Configured under `logging` and `monitor`, these capabilities are visualized across the **Dashboard**, **Logs**, **Monitor**, and **Attack Map** modules in the Web Console.

## 1. Structured Access Logs {#logs}

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

- **Rotation & Retention**: Automatically rotates files based on size (`max_size`) and retains a configurable number of historical backups (`max_backups`).
- **Trace ID Correlation**: Every request receives a globally unique `traceId` for end-to-end tracing across all processing stages.
- **Log Support Bundles**: Execute `cheesewaf logs pack` to immediately generate a timestamped ZIP archive containing all runtime logs.
- **External Sinks**: Asynchronously stream logs to ClickHouse, PostgreSQL, VictoriaLogs, or Elasticsearch. See [Storage & Scheduler Architecture](../storage/).

## 2. Prometheus Metrics & Remote Write {#prometheus}

```yaml
monitor:
  prometheus:
    enabled: true
    path: "/metrics"
    public: false
  remote_write:
    enabled: false
    endpoint: "https://prometheus-push.internal/api/v1/write"
    interval: 1m
    timeout: 10s
```

- **Scrape Endpoint**: When `public: false`, scraping `/api/metrics` requires an administrative Bearer token. Setting `public: true` exposes `/metrics` directly at the root path.
- **Remote Write (Protobuf Streaming)**: Periodically pushes metrics directly to compatible collectors using the official Prometheus Remote Write protocol format.

## 3. Alerts & Notification Channels {#alerts}

Configure alert thresholds for anomalous drop surges (`high-block-rate`) or storage exhaustion (`disk-usage`):

- **Notifiers**: Deliver notifications via standard HTTP Webhooks (enterprise platforms like Slack, DingTalk, WeChat Work, and Lark connect via their incoming bot webhook URLs).
- **In-App Notifications**: Event alerts are mirrored to the system notification bus and retrievable via `/api/notifications`.

## 4. Threat Attack Map (100% Offline & Compliance Ready) {#map}

Navigate to `/attack-map` or fullscreen `/attack-map/screen` to monitor inbound attack geolocations and threat distributions in real time.

The attack map is engineered for air-gapped security and compliance:
- **Certified National Boundaries**: Integrates officially approved China border geometries and the South China Sea ten-dash line.
- **Licensed Gaode World Polygons**: Uses licensed country and regional polygon datasets.
- **3D Offline Earth Canvas**: Eliminates all external dependencies on public OpenStreetMap (OSM) raster tile servers. The 3D globe operates completely offline, preventing external DNS leakage and guaranteeing 100% availability in air-gapped, isolated networks.
