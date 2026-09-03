---
title: 流量限流
linkTitle: 限流
weight: 50
description: 基于分片滑动窗口计数器的数据平面全局限流与排队削峰机制。
---

CheeseWAF 在数据平面内置了高性能的分片滑动窗口计数器限流算法（Sharded Sliding Window Counter），用于平抑瞬时流量高峰并防范 CC 攻击。配置位于 `protection.ratelimit`，支持通过 REST API `PUT /api/protection/ratelimit` 进行热更新。

## 基础配置示例 {#config}

```yaml
protection:
  ratelimit:
    enabled: true
    default:
      requests: 100
      window: 60s
      burst: 20
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | 布尔值 | 数据平面限流总开关 |
| `requests` | 整数 | 在时间窗口内允许通过的基础请求配额 |
| `window` | 时间段 | 限流计算的时间窗口（如 `60s`、`1m`） |
| `burst` | 整数 | 允许应对突发流量的额外突发容量 |

{{% pageinfo color="info" %}}
本模块作用于**数据平面全局/客户端维度**的流量整形。若需针对已发现的具体 API 路由（HTTP 方法 + 路径）设置细粒度限流，请参考 [API 安全中的接口限流](../../api-security/#rate)。
{{% /pageinfo %}}

## 超额处置策略 {#actions}

当客户端的请求速率超出设定配额时，系统支持以下处置动作：

1. **直接返回 429 拦截页**：向客户端响应 HTTP 429 Too Many Requests 状态码及定制的拦截提示。
2. **调度至排队室**：若同时启用了 [排队室机制](../bot-captcha/#waiting-room) 且全局 `protection.policy.bot_cc` 策略未关闭并映射为 `challenge`，超出限流配额的客户端将被引导至排队等待页面。

建议在上线初期采用较宽松的配额阈值，在观察 1～2 周的正常业务流量基线后，再逐步收紧 `requests` 与 `burst` 参数。
