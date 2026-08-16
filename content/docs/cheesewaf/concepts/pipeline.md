---
title: Request pipeline
linkTitle: Pipeline
weight: 10
description: Solid lines are the millisecond path. Dashed lines are ALAP after the response.
---

```mermaid
flowchart TB
  Client[Client] --> Ingress[HTTP / HTTPS / HTTP3]
  Ingress --> IP{IP / geo / fingerprint}
  IP -->|deny list| Block[Block page]
  IP -->|allow| Bot{Bot / rate limit / waiting room}
  Bot -->|challenge| Challenge[CAPTCHA or queue]
  Challenge -->|pass| Sem
  Bot -->|allow| Sem[Semantic engine]
  Sem --> Shape{Isolated or embedded}
  Shape -->|isolated 2-5| Block
  Shape -->|embedded 5| Block
  Shape -->|embedded 2-4| Pass[Allow and enqueue]
  Shape -->|clean| Origin[Upstream]
  Pass --> Origin
  Pass -.-> Queue[ALAP queue]
  Sem -.->|level 5 block| Queue
  Queue --> LLM[Configured model]
  LLM --> Review{Decision}
  Review -->|high / critical| Rule[Lasting rule]
  Review -->|low or false positive| Dismiss[Archive or allow list]
  Rule -.-> IP
```

Solid arrows stay on the request path.
Dashed arrows run after the client already has a response.

Site-level `waf.mode` can be `block` or a record-only style depending on paranoia.
Level 0 and 1 never block on semantic hits.

See [Protection](../../protection/) for each filter in this diagram.
