---
title: Request Processing Pipeline
linkTitle: Pipeline
weight: 10
description: Detailed breakdown of the synchronous traffic forwarding path and the post-response asynchronous ALAP review pipeline.
---

CheeseWAF structures traffic evaluation into two distinct lifecycles: the **Synchronous Inline Inspection Path** and the **Asynchronous Out-of-Band Review Path**. The diagram below illustrates the end-to-end flow of an incoming HTTP/HTTPS/HTTP3 request:

```mermaid
flowchart TB
  Client[Client Request] --> Ingress[Ingress Layer HTTP / HTTPS / HTTP3]
  Ingress --> IP{IP / GeoIP / Soft-Fingerprint}
  IP -->|Blacklisted| Block[Render Block Page]
  IP -->|Passed| Bot{Bot Challenge / Rate Limit / Waiting Room}
  Bot -->|Challenge Triggered| Challenge[Solve CAPTCHA / Queue in Room]
  Challenge -->|Passed| Sem
  Bot -->|Clean/Bypassed| Sem[AST Semantic Engine]
  Sem --> Shape{Payload Morphology}
  Shape -->|Isolated Levels 2~5| Block
  Shape -->|Embedded Level 5| Block
  Shape -->|Embedded Levels 2~4| Pass[Allow & Enqueue Async]
  Shape -->|Clean| Origin[Proxy to Upstream Origin]
  Pass --> Origin
  Pass -.-> Queue[ALAP Async Review Queue]
  Sem -.->|Level 5 Blocked Sample| Queue
  Queue --> LLM[Query Configured LLM]
  LLM --> Review{AI Decision}
  Review -->|High / Critical| Rule[Persist Long-Term Rule]
  Review -->|Low / False Positive| Dismiss[Archive / Allowlist]
  Rule -.-> IP
```

## Pipeline Lifecycle Breakdown {#pipeline-details}

### 1. Synchronous Forwarding Path (Solid Lines) {#sync-path}

The synchronous path handles real-time client-to-origin communication, prioritized for high throughput and sub-millisecond latency:

- **Ingress & Network Layer Filtering**: Evaluates IP whitelists/blacklists, GeoIP country bans, and client TLS soft-fingerprints. Requests matching blacklists are rejected immediately with a block page.
- **Access Control & Anti-Scraping**: Evaluates bot challenges, token bucket rate limits, and waiting room capacity. Suspicious clients must complete JavaScript challenges or solve CAPTCHAs before proceeding.
- **Semantic Analysis & Policy Evaluation**: Performs parameter decoding and builds AST representations to detect attack syntax, executing an immediate block or pass decision based on the configured Paranoia Level.
- **Origin Reverse Proxying**: Clean requests are dispatched to healthy backend upstream servers according to configured load balancing policies.

### 2. Asynchronous Review Path (Dashed Lines) {#async-path}

The asynchronous path operates out-of-band after the client has already received its response:

- **Sample Enqueuing**: Embedded payloads allowed under paranoia levels 2–4 and high-severity attacks blocked at level 5 are placed into the ALAP review queue.
- **LLM Reasoning**: Background workers query the configured LLM API to extract malicious intent and calculate confidence scores.
- **Closed-Loop Rule Persistence**: Threats confirmed as high (`high`) or critical (`critical`) can be automatically or manually committed as long-term IP blacklists or custom signature rules.

{{% pageinfo color="info" %}}
When `waf.mode` is set to `block`, paranoia levels 2–5 enforce blocking rules. Under level 0 (log only) and level 1 (monitoring), the system records alerts without terminating requests. For filter configuration details, see [Security Policies](../../protection/).
{{% /pageinfo %}}
