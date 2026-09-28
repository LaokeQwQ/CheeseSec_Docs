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

## Why CheeseWAF {#why-cheesewaf}

Modern Web security solutions usually force teams into painful tradeoffs:
1. **Traditional Regex WAFs (e.g., ModSecurity / CRS)**: Maintaining thousands of regular expressions is tedious. Attackers bypass signatures using character case variations, malformed encodings, or SQL comments. False positives are frequent, forcing operators to constantly tune exception lists.
2. **Synchronous LLM WAFs**: Routing every HTTP request to an LLM adds 500 ms to 2 s of latency to each response, burns API token budgets, and risks full outages whenever external endpoints experience latency spikes.
3. **Heavy Container Stacks (e.g., SafeLine / 雷池)**: Requiring 5 to 10 Docker containers (Tengine, Postgres, Redis, management daemons) consuming 1 to 2 GB+ of RAM, which quickly overburdens budget cloud instances and small VPSs.
4. **Commercial Cloud WAFs (e.g., Cloudflare / Cloud Provider WAFs)**: All traffic must route through third-party infrastructure, raising privacy, data residency, and compliance concerns. Bandwidth billing is unpredictable, and air-gapped operation is impossible.

CheeseWAF takes a balanced approach: **an in-process AST semantic parser provides sub-millisecond inline blocking, while an out-of-band LLM auto-pilot (ALAP) reviews ambiguous samples in the background and synthesizes persistent custom rules without adding latency to live requests.**

### Comparison Overview

| Dimension | Regex WAF (e.g., ModSecurity) | Synchronous LLM WAF | Heavy Container Stack | Commercial Cloud WAF | CheeseWAF |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Detection Engine** | Regex pattern matching | Synchronous LLM per request | Regex + statistical analysis | Signature sets + threat feed | **AST syntax analysis + Async LLM Auto-Pilot (ALAP)** |
| **Inline Latency Added** | 1–10 ms | **500–2000 ms** (high) | 2–15 ms | Dependent on CDN routing | **< 1 ms** (sub-millisecond, zero model wait) |
| **API / Token Cost** | None | Extremely high (all traffic) | None | Bandwidth & tier billing | **Low** (reviews only ambiguous samples out-of-band) |
| **Evasion & False Positives** | Easily bypassed by encodings | Prone to hallucinations | Complex rule maintenance | Vendor-dependent updates | **Parses syntax trees; immune to obfuscation; FPR < 0.8%** |
| **Footprint & Deployment** | Requires custom Nginx build | External API dependency | 5–10 containers, 1–2 GB+ RAM | Cloud-only | **Single binary / single container, embedded SQLite, tens of MB RAM** |
| **Architectural Disruption** | Bound to web server | Modifies primary traffic path | Replaces primary gateway | DNS / reverse proxy takeover | **Runs as standalone reverse proxy or sidecar via `adapterd`** |
| **Data Privacy & Compliance** | Local | Full traffic sent to external API | Local | Traffic traverses public cloud | **100% on-premises; optional private self-hosted LLM** |
| **Air-gapped Environments** | Supported | Not supported (requires cloud API) | Partially supported | Not supported | **Fully supported with offline Ed25519 CRP verification** |

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
