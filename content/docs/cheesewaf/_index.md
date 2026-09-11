---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: Commercial-grade self-hosted Web Application Firewall. Complete documentation for deployment, security policies, configuration, and operations.
---

CheeseWAF is a self-hosted Web Application Firewall (WAF) distributed as a Go core. The current runtime uses embedded SQLite for management state. PostgreSQL is an optional asynchronous access-log sink; Redis is not wired as the Bot challenge backend. Cluster coordination currently runs only through builtin for single-node deployments; selecting etcd records the shared-cluster requirement but the current binary has no etcd-backed coordinator and remains fail-closed. The commercial control-plane, native-raft, CWEDP, and Socket Lease services are not wired into startup yet. CRP now has a local verified-import and staged-slot layer (`crp verify` / `crp stage`), but promotion, plugin execution, cluster distribution, and OTA remain unavailable.

Architecturally, CheeseWAF keeps the **Data Plane** request path separate from the **Management Plane** listener and its asynchronous ALAP work. The same `cheesewaf` process starts both listeners: the Data Plane performs bounded synchronous inspection and reverse proxying, while the Management Plane hosts the API, console, and background review workers without waiting on remote LLMs in the request path. A separate commercial control-plane service remains a future, unwired component.

{{% pageinfo color="info" %}}
Official releases are available on [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases). The project is open-source under the [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE).
{{% /pageinfo %}}

## Core Mechanisms {#how-it-works}

1. **High-Performance Data Plane Inspection**: Incoming requests undergo multi-layer recursive decoding before entering the Abstract Syntax Tree (AST) semantic engine. Identified SQL injection, Cross-Site Scripting (XSS), Remote Code Execution (RCE), and malicious payloads are blocked in sub-millisecond to microsecond timeframes.
2. **Asynchronous ALAP Threat Review**: After the client receives its response, ambiguous samples or payloads embedded in large text blocks are enqueued into a background review pipeline. Configured LLMs (compatible with OpenAI and Anthropic APIs) perform in-depth semantic reasoning.
3. **Closed-Loop Rule Synthesis**: Samples evaluated as high (`high`) or critical (`critical`) threats can be approved manually or via auto-agreement. Site-level auto-agreement persists a site-scoped custom payload rule; global IP denylists and client soft-fingerprint actions remain explicit operator decisions.

## Default Network Listeners {#default-listeners}

CheeseWAF exposes services on the following default listener endpoints:

| Plane / Service | Default Address | Description |
| --- | --- | --- |
| **Data Plane** | `http://127.0.0.1:8080` | Ingests business traffic, performs synchronous security inspection, and proxies upstream |
| **Management Plane** | `http://127.0.0.1:9443` | Hosts the Web console, REST API, and `/setup` initialization wizard (defaults to HTTPS in Docker) |
| **Cluster Plane** | `https://127.0.0.1:9444` | Optional TLS/mTLS interconnect when `cluster.enabled: true`; it handles node identity, health/heartbeat, topology, and orchestration hooks but is not a general site/policy replication channel |
| **Local Controller** | `http://127.0.0.1:17943` | Local loopback auxiliary controller port for Windows and macOS desktop environments |

## Documentation Roadmap {#start-here}

{{< nav-cards cols="2" >}}
{{< nav-card title="Deployment & Installation" link="/docs/cheesewaf/install/" icon="fa-solid fa-download" desc="Step-by-step guides for Linux (systemd), Docker Compose, Windows, and macOS environments." />}}
{{< nav-card title="Quick Start" link="/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="Initial system setup, reverse proxy site onboarding, and connecting LLM review providers." />}}
{{< nav-card title="Core Concepts" link="/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="In-depth breakdown of the request lifecycle, paranoia levels, payload isolation, and unified RBAC." />}}
{{< nav-card title="Security Policies" link="/docs/cheesewaf/protection/" icon="fa-solid fa-shield" desc="AST semantic engine, custom regex rules, IP/GeoIP filtering, bot challenges, sharded sliding-window counter rate limiting, and ACLs." />}}
{{< nav-card title="Air-gapped Operations" link="/docs/cheesewaf/operations/" icon="fa-solid fa-lock" desc="Current offline verification and storage maintenance; full plugin egress, upload, and recovery workflows remain design-stage contracts." />}}
{{< nav-card title="Standalone Control Runtime" link="/docs/cheesewaf/control-plane-runtime/" icon="fa-solid fa-server" desc="Current cheesewaf-control flags, fail-closed startup checks, local probes, and join-mode limits." />}}
{{< /nav-cards >}}
