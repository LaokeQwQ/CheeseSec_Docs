---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: Commercial-grade self-hosted Web Application Firewall. Complete documentation for deployment, security policies, configuration, and operations.
---

CheeseWAF is a commercial-grade, self-hosted Web Application Firewall (WAF) distributed as a single Go binary. It features an embedded, CGO-free SQLite database, a modern Web console, an interactive TUI command-line utility, and a comprehensive RESTful management API—delivering an out-of-the-box experience without external database or proxy dependencies.

Architecturally, CheeseWAF enforces a strict **separation between the Data Plane and Control Plane**. The Data Plane performs sub-millisecond synchronous traffic inspection and reverse proxying without blocking on remote LLMs. Concurrently, the Control Plane leverages an asynchronous ALAP (AI Large-Language-Model Auto Pilot) engine for out-of-band intelligent threat analysis and rule self-learning.

{{% pageinfo color="info" %}}
Official releases are available on [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases). The project is open-source under the [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE).
{{% /pageinfo %}}

## Core Mechanisms {#how-it-works}

1. **High-Performance Data Plane Inspection**: Incoming requests undergo multi-layer recursive decoding before entering the Abstract Syntax Tree (AST) semantic engine. Identified SQL injection, Cross-Site Scripting (XSS), Remote Code Execution (RCE), and malicious payloads are blocked in sub-millisecond to microsecond timeframes.
2. **Asynchronous ALAP Threat Review**: After the client receives its response, ambiguous samples or payloads embedded in large text blocks are enqueued into a background review pipeline. Configured LLMs (compatible with OpenAI and Anthropic APIs) perform in-depth semantic reasoning.
3. **Closed-Loop Rule Synthesis**: Samples evaluated as high (`high`) or critical (`critical`) threats can be approved manually or via auto-agreement, persisting into long-term IP blacklists, client soft-fingerprints, or custom signature rules.

## Default Network Listeners {#default-listeners}

CheeseWAF exposes services on the following default listener endpoints:

| Plane / Service | Default Address | Description |
| --- | --- | --- |
| **Data Plane** | `http://127.0.0.1:8080` | Ingests business traffic, performs synchronous security inspection, and proxies upstream |
| **Management Plane** | `http://127.0.0.1:9443` | Hosts the Web console, REST API, and `/setup` initialization wizard (defaults to HTTPS in Docker) |
| **Cluster Plane** | `http://127.0.0.1:9444` | Handles inter-node communication and state synchronization in High Availability (HA) cluster mode |
| **Local Controller** | `http://127.0.0.1:17943` | Local loopback auxiliary controller port for Windows and macOS desktop environments |

## Documentation Roadmap {#start-here}

{{< nav-cards cols="2" >}}
{{< nav-card title="Deployment & Installation" link="/docs/cheesewaf/install/" icon="fa-solid fa-download" desc="Step-by-step guides for Linux (systemd), Docker Compose, Windows, and macOS environments." />}}
{{< nav-card title="Quick Start" link="/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="Initial system setup, reverse proxy site onboarding, and connecting LLM review providers." />}}
{{< nav-card title="Core Concepts" link="/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="In-depth breakdown of the request lifecycle, paranoia levels, payload isolation, and unified RBAC." />}}
{{< nav-card title="Security Policies" link="/docs/cheesewaf/protection/" icon="fa-solid fa-shield" desc="AST semantic engine, custom regex rules, IP/GeoIP filtering, bot challenges, token bucket rate limiting, and ACLs." />}}
{{< /nav-cards >}}
