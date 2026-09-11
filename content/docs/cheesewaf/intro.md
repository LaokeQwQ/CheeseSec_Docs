---
title: Architecture & Working Principles
linkTitle: Introduction
weight: 10
description: Understand the division of labor between the Data Plane and asynchronous ALAP review, the out-of-band analysis model, and single-binary packaging.
---

Traditional signature-based Web Application Firewalls rely heavily on expansive regular expression libraries. These approaches incur high rule maintenance costs and remain susceptible to bypasses via multi-layer encoding, nested syntax, and character obfuscation. Conversely, invoking Large Language Models (LLMs) synchronously within the real-time request path introduces unacceptable network latency and availability bottlenecks.

To address these challenges, CheeseWAF adopts a **decoupled dual-plane architecture with asynchronous out-of-band threat review**, combining deterministic, sub-millisecond blocking with deep semantic intelligence.

## Dual-Plane Architecture {#two-planes}

### Data Plane {#data-plane}

The Data Plane processes incoming HTTP/1.1, HTTPS, and HTTP/3 traffic through an ordered, high-performance pipeline:

1. **Network & Identity Filtering**: Evaluates IP access control lists, GeoIP country bans, and client soft-fingerprints.
2. **Access Control & Anti-Scraping**: Enforces bot challenges, sharded sliding-window counter rate limits, and waiting room scheduling.
3. **AST Semantic Analysis**: Parses recursively decoded parameters into language syntax trees for attack detection.
4. **Reverse Proxying**: Dispatches validated requests to the configured backend upstream servers.

The Data Plane operates strictly within the critical request path, adhering to deterministic execution and never blocking on external LLM calls.

### Management Plane {#management-plane}

The same `cheesewaf` process starts a dedicated management listener for administration and observability; this is a management plane boundary, not the future standalone commercial control-plane service:

- **`/setup` Initialization Wizard**: Guides initial deployment and provisions administrator credentials.
- **Web Management Console**: Serves a modern, responsive React-based single-page application.
- **RESTful Management API**: Powers automation scripts and third-party operational integrations under the `/api` namespace.
- **Metrics & Observability**: Exports Prometheus metrics and provides health check probes.

{{% pageinfo color="warning" %}}
For security reasons, keep `server.admin_public` set to `false` unless TLS encryption is enabled and strict network-level access controls (such as IP whitelisting or private networks) are in place.
{{% /pageinfo %}}

### Asynchronous ALAP Threat Review {#alap}

After the Data Plane completes response delivery to the client, CheeseWAF enqueues selected samples into the background ALAP (AI Large-Language-Model Auto Pilot) review pipeline:

- **High-Severity Blocked Samples**: Deterministic standalone attack payloads blocked at paranoia level 5.
- **Embedded Feature Samples**: Mixed-context requests allowed at paranoia levels 2–4 that contain suspicious patterns within larger text blocks.
- **Borderline Samples**: Traffic marked by the semantic engine as low-confidence or near decision thresholds.

Background workers asynchronously query the configured LLM for deep contextual analysis. Security operators can review decisions in the console or enable auto-agreement to persist confirmed threats as long-term defensive rules. See [ALAP and Review Queue](../alap/).

## Delivery Components & Single-Binary Distribution {#what-ships}

CheeseWAF keeps the request path self-contained. The runnable management-storage profile is `storage.profile: temporary`, which stores management state in embedded SQLite. `storage.profile: production` is reserved for a future durable path and currently fails closed with `ErrProductionStorageUnavailable`; PostgreSQL is an optional asynchronous access-log sink, and Redis is not wired as the Bot challenge backend. The internal CRP RuntimeStore can verify and persist a local package in a staged slot, and the CLI exposes `crp verify`/`crp stage`; it does not activate or execute plugins. The separate commercial control plane, native-raft, CWEDP distribution, and Socket Lease services are not connected to startup:

| Component | Role & Functionality |
| --- | --- |
| `cheesewaf` | Primary server process; default command is `serve` to launch the data and management listeners in one process |
| `waf-cli` | Same binary (or symbolic link); default command launches the interactive TUI management panel |
| `cheesewaf-gui` | Browser-based local service controller for Windows and macOS (binds exclusively to loopback) |
| Web Console | Modern React application embedded within the binary and hosted by the process's management listener |
| Storage profiles | Current: `temporary` with embedded SQLite; reserved `production` profile currently rejected at startup; optional PostgreSQL log sink; builtin single-node cluster path, with configured etcd/native-raft coordinators not wired |
| CRP local state | `crp verify` and `crp stage` verify/persist local packages only; promotion, execution, cluster distribution, and OTA are unavailable |

## Related Documentation {#related}

- [Request Processing Pipeline](../concepts/pipeline/)
- [Paranoia Levels & False-Positive Mitigation](../concepts/paranoia/)
- [Standalone Control Runtime](../control-plane-runtime/)
- [System Installation & Deployment](../install/)
