---
title: 限流
linkTitle: 限流
weight: 50
description: 数据平面上的令牌桶。接口级限流在 apisec 里。
---

配置：`protection.ratelimit`。
REST：`PUT /api/protection/ratelimit`。

```yaml
protection:
  ratelimit:
    enabled: true
    default:
      requests: 100
      window: 60s
      burst: 20
```

这是 **数据平面** 上的令牌桶。
它和 `apisec.rate_limits` 不是一回事。后者按「方法 + 路径」匹配已发现的接口。

桶空了之后，CheeseWAF 可以：

- 返回类似 429 的拦截页
- 或者在打开排队室时，把客户端送进 [排队室](../bot-captcha/#waiting-room)

先用示例里的数字。
看过一周日志之后，再降低 `requests`。
