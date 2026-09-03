---
title: 监控、日志与攻击态势大屏
linkTitle: 监控
weight: 110
description: 访问日志轮转、Prometheus 指标导出与 Remote Write、自定义告警通知及 100% 纯离线合规攻击态势大屏。
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
- **日志支持包一键导出**：可直接在终端执行 `cheesewaf logs pack` 一键生成包含所有运行日志的 ZIP 支持包。
- **日志外发**：支持将日志异步外发至 ClickHouse、PostgreSQL、VictoriaLogs 或 Elasticsearch，详见 [存储与调度管理](../storage/)。

## 2. Prometheus 指标与 Remote Write {#prometheus}

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

- **指标采集端点**：当 `public: false` 时，需携带管理员权限令牌访问 `/api/metrics` 抓取指标；若设为 `public: true`，端点直接挂载于路由根路径。
- **Prometheus Remote Write（Protobuf 支持）**：支持将 WAF 运行指标通过标准的 Prometheus Remote Write 协议（Protobuf 编码）定时主动推送到统一监控中心。

## 3. 告警规则与通知渠道 {#alerts}

系统支持配置拦截率突增（`high-block-rate`）与磁盘空间预警（`disk-usage`）等规则：

- **通知渠道（Notifiers）**：在 `monitor.notifiers` 中可配置标准 Webhook 通知器（钉钉、企业微信、飞书等企业即时通讯通过配置其自定义机器人 Webhook URL 即可接入）。
- **站内消息中心**：所有告警事件同时写入站内通知系统，可通过 `/api/notifications` 端点拉取。

## 4. 实时攻击态势大屏（100% 纯离线与合规支持） {#map}

访问控制台的 `/attack-map` 或全屏模式 `/attack-map/screen`，可实时渲染全球威胁攻击来源、拦截频次与攻击类型分布。

最新版本对大屏进行了全面的离线化与合规重构：
- **规范国界线与十段线**：内置规范审图标准的中国国界线与完整的南海十段线地理矢量数据。
- **授权高德世界边界**：采用合规授权的高德全球国家与地区多边形边界资产。
- **3D 纯离线地球渲染**：放弃传统依赖公网 OpenStreetMap（OSM）光栅瓦片图的方案，采用轻量级 3D 离线地球矢量渲染，彻底杜绝外网瓦片加载慢与请求外泄隐患，确保在完全隔离的涉密内网或离线专网环境中 100% 正常显示。
