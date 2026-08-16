---
title: 监控、日志与攻击态势大屏
linkTitle: 监控
weight: 110
description: 访问日志轮转、Prometheus 指标导出、自定义告警通知及实时攻击态势大屏。
---

CheeseWAF 提供了全链路的可观测性支持，包括结构化访问日志、Prometheus 标准指标输出、多渠道告警推送及可视化攻击态势大屏。

在 Web 管理控制台中对应 **仪表盘**、**日志检索**、**监控告警** 与 **攻击态势大屏** 模块，底层配置项对应 `logging` 与 `monitor`。

## 1. 结构化访问日志 {#logs}

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

- **日志轮转与切割**：支持按文件大小（`max_size`）与保留备份数量（`max_backups`）自动执行安全轮转。
- **Trace ID 全链路定位**：每条日志均包含全局唯一的 `traceId`。在控制台访问 `/logs/{traceId}` 可直达该请求的完整命中断言详情。
- **日志外发**：支持将日志外发至 ClickHouse、PostgreSQL 或 VictoriaLogs 等外部存储，详见 [存储与调度管理](../storage/)。

## 2. Prometheus 指标导出 {#prometheus}

```yaml
monitor:
  prometheus:
    enabled: true
    path: "/metrics"
    public: false
```

- **指标采集端点**：当 `public: false` 时，需携带具备权限的管理令牌请求 `/api/metrics` 抓取指标；若设为 `public: true`，指标端点直接挂载于路由根路径（建议结合网络 ACL 限制内网监控系统访问）。
- **Prometheus Remote Write**：支持通过 `monitor.remote_write` 将时序指标主动推送到兼容 Prometheus Remote Write 协议的监控中心。

## 3. 告警规则与通知渠道 {#alerts}

系统支持配置拦截率突增（`high-block-rate`）与磁盘空间预警（`disk-usage`）等规则：

- **通知渠道（Notifiers）**：在 `monitor.notifiers` 中可配置 Webhook、邮件或企业即时通讯机器人（如钉钉、企业微信、飞书等）。
- **站内消息中心**：所有告警事件同时写入站内通知系统，可通过 `/api/notifications` 端点拉取。

## 4. 实时攻击态势大屏 {#map}

访问控制台的 `/attack-map` 或全屏模式 `/attack-map/screen`，可实时渲染全球威胁攻击来源、拦截频次与攻击类型分布。

{{% pageinfo color="info" %}}
通过配置 `console.map.china_boundary` 可加载规范审阅的中国国界线地图数据文件。引用外部地图源时，建议保持 `allow_insecure: false` 与 `allow_private: false`，避免潜在的未授权网络探测。
{{% /pageinfo %}}
