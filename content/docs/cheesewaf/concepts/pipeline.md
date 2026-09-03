---
title: Traffic Pipeline & Two-Phase Execution
linkTitle: Pipeline
weight: 10
description: Deep dive into the synchronous Two-Phase detection pipeline (Pre-Filters + Semantic Worker Pool) and the asynchronous ALAP offline review loop.
---

CheeseWAF separates traffic processing into two distinct flows: the **Synchronous Detection Pipeline** and the **Asynchronous Out-of-Band Review Loop**. Within the synchronous path, CheeseWAF employs a high-performance **Two-Phase Pipeline** architecture to achieve microsecond-level short-circuit drops while preserving high throughput for deep AST parsing:

```mermaid
flowchart TB
  Client[Client Request] --> Ingress[Ingress HTTP / HTTPS / HTTP3]
  subgraph Phase1 [Phase 1: Pre-Filters (Sequential / Short-Circuit / Priority < 290)]
    IP{IP / Geo / Fingerprint} -->|Pass| Bot{Bot Challenge / RateLimit}
    Bot -->|Pass| Rules{Custom Rules Priority 250}
  end
  Ingress --> IP
  IP -->|Blacklisted| Block[Render Block Page]
  Bot -->|Trigger Challenge| Challenge[Solve Challenge / Waiting Room]
  Challenge -->|Verified| Rules
  Rules -->|Match Block| Block

  subgraph Phase2 [Phase 2: Semantic Group (Parallel Worker Pool / Deterministic Merge / Priority >= 290)]
    Sem[AST Semantic Analyzers: SQL / XSS / RCE / LFI / NoSQL / SSTI etc.]
  end
  Rules -->|Clean| Sem

  Sem --> Shape{Payload Context}
  Shape -->|Isolated Attack Level 2~5| Block
  Shape -->|Embedded Attack Level 5| Block
  Shape -->|Embedded Attack Level 2~4| Pass[Pass & Enqueue Asynchronously]
  Shape -->|Clean| Origin[Forward to Backend Upstream]
  Pass --> Origin
  Pass -.-> Queue[ALAP Review Queue]
  Sem -.->|Level 5 Blocked Sample| Queue
  Queue --> LLM[LLM Reasoning & Attribution]
  LLM --> Review{Decision}
  Review -->|High / Critical| Rule[Generate Protective Rules]
  Review -->|Low / False Positive| Dismiss[Dismiss / Allowlist]
  Rule -.-> IP
```

## Two-Phase Pipeline Architecture {#two-phase-pipeline}

To ensure deterministic latency guarantees under high concurrent load, the detection pipeline partitions all registered detectors by `Priority` into two separate execution phases:

### 1. Phase 1: Pre-Filters (Priority < 290)

- **Components**: IP Access Control, GeoIP, Soft Client Fingerprinting, Bot Challenges, Rate Limiting, and the **Custom Regex Rule Engine (Priority 250)**.
- **Execution Model**: Strictly sequential single-threaded execution.
- **Fast Short-Circuiting**: If any pre-filter returns `ActionBlock`, the request is immediately dropped and the pipeline terminates. The request **never reaches the AST semantic parsing stage**, allowing reconnaissance probes and known signatures to be discarded within microseconds.

### 2. Phase 2: Semantic Group (Priority >= 290)

- **Components**: Deep syntax analyzers for SQL injection, Cross-Site Scripting (XSS), Remote Code Execution (RCE), Local File Inclusion (LFI), NoSQL injection, Server-Side Template Injection (SSTI), SSRF, and XXE.
- **Execution Model**:
  - **Shared Worker Pool**: Dispatched across a shared worker pool (bounded at 8 workers) to maximize multi-core CPU efficiency without unbounded goroutine proliferation.
  - **Context Forking**: Each detector executes with a forked `RequestContext`, guaranteeing data race immunity for `Metadata` and `Results` writes.
  - **Deterministic Merge**: Once parallel evaluations conclude, results are merged in strict priority order, ensuring 100% deterministic decision-making and logging.

## Pipeline Timeout & Budget Protection {#budget-protection}

- **100ms Hard Timeout**: A global 100ms pipeline deadline guarantees that adversarial payloads cannot cause request processing hangs.
- **Analysis Budget Depletion Policy (`budget_exhausted_policy`)**: If deep parsing cannot finish within the deadline, the fallback policy takes effect:
  - `auto`: Follows the global `web_attack` policy level.
  - `open`: Fails open to preserve application availability while recording metrics.
  - `observe`: Logs observation details without a hard drop.
  - `closed`: Security-first challenge or strict block.
- **Overload Guarding**: Built-in guard monitors detect backpressure and return `ErrDetectionOverload`, protecting the primary service from cascading degradation.

## Asynchronous Review Loop (ALAP) {#async-path}

The asynchronous path runs completely decoupled from real-time reverse proxying:

- **Sample Dispatch**: Embedded samples passed under Paranoia Levels 2–4 and blocked samples under Level 5 are delivered to the review queue after response delivery.
- **LLM Intent Extraction**: Background workers issue inference requests to extract threat semantics and confidence scores.
- **Closed-Loop Rule Derivation**: Manual review decisions can promote a verified sample to the selected payload, URI, IP, or fingerprint rule. Site-level automated adoption is narrower: it writes a site-scoped custom payload rule only.

{{% pageinfo color="info" %}}
For detailed configuration options of individual detectors, see [Protection](../../protection/); for setting up AI models, see [ALAP Review](../../alap/).
{{% /pageinfo %}}
