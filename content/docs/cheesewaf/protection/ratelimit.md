---
title: Rate limit
linkTitle: Rate limit
weight: 50
description: Token-bucket limits on the data plane. API-specific limits live under apisec.
---

Config: `protection.ratelimit`.
REST: `PUT /api/protection/ratelimit`.

```yaml
protection:
  ratelimit:
    enabled: true
    default:
      requests: 100
      window: 60s
      burst: 20
```

This is a token bucket on the **data plane**.
It is not the same as `apisec.rate_limits`, which match one method + path on discovered APIs.

When the bucket is empty, CheeseWAF can:

- return a 429-style block page
- or send the client to the [waiting room](../bot-captcha/#waiting-room) when that is enabled

Start with the sample numbers.
Lower `requests` only after you have a week of logs.
