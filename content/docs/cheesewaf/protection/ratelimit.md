---
title: Rate Limiting & Traffic Shaping
linkTitle: Rate Limiting
weight: 50
description: High-performance token bucket rate limiting on the Data Plane with queueing and rejection handling.
---

CheeseWAF integrates a high-performance token bucket rate limiting algorithm on the Data Plane to smooth out traffic spikes and mitigate HTTP flood / CC attacks. Configuration is located under `protection.ratelimit`, and can be updated dynamically via `PUT /api/protection/ratelimit`.

## Base Configuration Example {#config}

```yaml
protection:
  ratelimit:
    enabled: true
    default:
      requests: 100
      window: 60s
      burst: 20
```

| Parameter | Type | Description |
| --- | --- | --- |
| `enabled` | Boolean | Master switch for Data Plane rate limiting |
| `requests` | Integer | Baseline request quota permitted within the rolling window |
| `window` | Duration | Calculation time window (e.g., `60s`, `1m`) |
| `burst` | Integer | Extra burst capacity accommodating temporary traffic surges |

{{% pageinfo color="info" %}}
This module enforces **global/client-level traffic shaping on the Data Plane**. For fine-grained rate limits targeting specific API endpoints (HTTP method + path), see [API Security Rate Limits](../../api-security/#rate).
{{% /pageinfo %}}

## Limit Exceeded Actions {#actions}

When a client's request rate exceeds the token bucket capacity, the system executes one of the following actions:

1. **HTTP 429 Block Page**: Responds immediately with HTTP 429 Too Many Requests and a customized error page.
2. **Waiting Room Scheduling**: If [Waiting Room Mechanism](../bot-captcha/#waiting-room) is active, excess requests are smoothly queued rather than dropped.

During initial rollout, use generous limits and observe 1–2 weeks of production traffic before tightening `requests` and `burst` thresholds.
