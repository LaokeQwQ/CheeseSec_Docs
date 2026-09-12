---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: Commercial-grade self-hosted Web Application Firewall. Complete documentation for deployment, security policies, configuration, and operations.
---

CheeseWAF is a commercial-grade self-hosted Web Application Firewall (WAF) distributed as a single Go core binary. The system utilizes a decoupled dual-plane architecture with an embedded lightweight persistent store for management state and supports external PostgreSQL as an asynchronous access-log sink.

Architecturally, CheeseWAF separates the **Data Plane** request forwarding path from the **Management Plane** and the asynchronous ALAP review pipeline. The `cheesewaf` process orchestrates both planes concurrently: the Data Plane executes bounded, low-latency synchronous inspection and reverse proxying, while the Management Plane hosts the management API, Web console, and background review workers—ensuring synchronous HTTP request paths are never blocked by remote LLM inference.

{{% pageinfo color="info" %}}
Official releases are available on [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases). The project is open-source under the [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE).
{{% /pageinfo %}}

## Core Mechanisms {#how-it-works}

1. **High-Performance Data Plane Inspection**: Incoming requests undergo multi-layer recursive decoding before entering the Abstract Syntax Tree (AST) semantic engine. Identified SQL injection, Cross-Site Scripting (XSS), Remote Code Execution (RCE), and malicious payloads are blocked in sub-millisecond to microsecond timeframes.
2. **Asynchronous ALAP Threat Review**: After the client receives its response, ambiguous samples or payloads embedded in large text blocks are enqueued into a background review pipeline. Configured LLMs (compatible with the OpenAI Response / Chat Completions APIs and Anthropic Messages API) perform in-depth semantic reasoning.
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
{{< nav-card title="Gateway Adapters" link="/docs/cheesewaf/adapters/" icon="fa-solid fa-network-wired" desc="Self-hosted Go adapter (adapterd) for NGINX and Envoy, enabling low-coupling traffic inspection and fail-closed defense." />}}
{{< nav-card title="Plugins & CRP" link="/docs/cheesewaf/plugins/" icon="fa-solid fa-puzzle-piece" desc="CRP v1 offline package format, Ed25519 threshold verification, content-addressed staging, and temporary egress auditing." />}}
{{< nav-card title="Air-gapped Operations" link="/docs/cheesewaf/operations/" icon="fa-solid fa-lock" desc="Offline package integrity verification, local storage maintenance, and operational management under air-gapped constraints." />}}
{{< nav-card title="Standalone Control Runtime" link="/docs/cheesewaf/control-plane-runtime/" icon="fa-solid fa-server" desc="Operational guidance for cheesewaf-control startup flags, security validation checks, local probes, and cluster join modes." />}}
{{< nav-card title="Developer's Words" link="/docs/cheesewaf/developer-words/" icon="fa-solid fa-heart" desc="Design motivations, engineering philosophy, and personal reflections from the creator." />}}
{{< /nav-cards >}}
