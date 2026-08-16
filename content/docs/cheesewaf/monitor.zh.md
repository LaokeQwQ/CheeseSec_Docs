---
title: 监控、日志和攻击地图
linkTitle: 监控
weight: 110
description: 仪表盘统计、访问日志、Prometheus、告警、通知和攻击地图。
---

控制台：**仪表盘**、**日志**、**监控**、**攻击地图**。
配置：`logging`、`monitor`。
REST：`/api/stats`、`/api/logs`、`/api/monitor`、`/api/metrics`、`/api/notifications`、`/api/audit`。

## 日志 {#logs}

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

`GET /api/logs` 列出事件。
控制台的 `/logs/{traceId}` 打开单条请求。

可选外发：PostgreSQL、ClickHouse、VictoriaLogs。见 [存储](../storage/)。

## Prometheus {#prometheus}

```yaml
monitor:
  prometheus:
    enabled: true
    path: "/metrics"
    public: false
```

`public` 为假时，用管理令牌抓 `/api/metrics`。
`public` 为真时，同一路径挂在路由根上。不要把它暴露到公网。

`monitor.remote_write` 可以推到兼容 Prometheus 的远程地址。

## 告警 {#alerts}

示例定义了 `high-block-rate` 和 `disk-usage`。
通知器支持 webhook（`monitor.notifiers`）。
站内通知走 `/api/notifications`。

## 攻击地图 {#map}

`/attack-map` 和 `/attack-map/screen` 画出最近的阻断。
`console.map.china_boundary` 可以加载一份经过审阅的中国边界文件。
不要把 `source` 指到不可信的 URL（`allow_insecure` / `allow_private` 保持 false，除非你清楚原因）。
