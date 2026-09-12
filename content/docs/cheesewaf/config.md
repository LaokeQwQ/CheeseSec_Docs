---
title: Configuration File Reference
linkTitle: Configuration
weight: 170
description: Complete structure navigation for cheesewaf.yaml, top-level key index, timeout controls, and hot-reload scopes.
---

CheeseWAF automatically generates a default `cheesewaf.yaml` configuration file within its runtime data directory under `config/` upon first launch (default `./data/config/cheesewaf.yaml`). A baseline template is maintained in the source repository at [`configs/cheesewaf.yaml`](https://github.com/LaokeQwQ/CheeseWAF/blob/dev/configs/cheesewaf.yaml).

`configs/cheesewaf.yaml` is a source template, not a runtime state file. Setup, site management, and console saves write to the runtime configuration. For source builds, copy it first to `./data/config/cheesewaf.yaml` or another dedicated data directory so database paths, certificates, secrets, and site changes never modify the Git working tree.

## Top-Level Configuration Index {#top-level-keys}

| Top-Level Key | Functional Area & Role | Documentation Reference |
| --- | --- | --- |
| `server` | Network listener sockets, management endpoints, and connection timeouts | [Architecture & Overview](../intro/) · [TLS & Certificates](../tls/) |
| `tls` | Data Plane TLS/HTTPS certificates and HSTS enforcement | [TLS & Certificates](../tls/) |
| `setup` | Initialization state tracking and runtime data directory path | [System Initialization](../tutorial/setup/) · [Storage & Scheduling](../storage/) |
| `deployment` / `cluster` | Deployment topology (standalone vs. HA cluster) and interconnects | [High Availability Clustering](../cluster/) |
| `console` | Web console UI preferences and administrative login security | [Bot & CAPTCHA](../protection/bot-captcha/) · [Monitoring & Logs](../monitor/) |
| `sites` | Reverse proxy sites, domain bindings, and upstream origin pools | [Site Management](../sites/) |
| `protection` | Global security baseline (AST engines, IP, Bot, rate limiting, ACL) | [Security Protection Policies](../protection/) |
| `block_page` | Block response templates and custom HTML branding sanitization | [Block Response Pages](../protection/block-page/) |
| `storage` | `temporary` SQLite management profile; reserved, currently rejected `production` profile; optional external log sinks | [Storage & Scheduling](../storage/) |
| `logging` | Access log verbosity, structured JSON formats, and log rotation | [Monitoring & Logs](../monitor/) |
| `ai` | ALAP LLM provider endpoints and asynchronous review parameters | [ALAP Review & Self-Learning](../alap/) |
| `update` | Reserved OTA settings; updater worker is not implemented in the current runtime | [System Operations](../operations/) |
| `scheduler` | Automated log cleanup, configuration snapshots, and daily security reports; snapshots are not complete database exports | [Storage & Scheduling](../storage/) |
| `edge` | Edge response header manipulation, static caching, and Brotli compression | [Edge Features](../edge/) |
| `monitor` | Prometheus metrics export, Remote Write, and alert notifiers | [Monitoring & Logs](../monitor/) |
| `apisec` | API asset discovery, request schema contracts, and RBAC matrix | [API Security & Governance](../api-security/) |
| `performance` | Go runtime Garbage Collection (GC) adaptive tuning (`memory_limit_ratio` / `min_gogc`) | [Architecture & Overview](../intro/) |
| `time_sync` | NTP sources, synchronization intervals, and clock-offset consensus limits | [Monitoring & Logs](../monitor/) |
| `captcha_assets` | Local or S3 CAPTCHA image/font assets and resource limits | [Bot & CAPTCHA](../protection/bot-captcha/) |
| `acme` | ACME certificate issuance and DNS challenge provider settings | [TLS & Certificates](../tls/) |
| `vulnerability` | Vulnerability CVE feed subscription configurations | [System Operations](../operations/) |

## Network Timeout Controls {#timeouts}

- **Ingress Connection Timeouts**: `server.read_timeout`, `server.write_timeout`, and `server.idle_timeout` govern the lifecycle of HTTP connections between clients and the WAF.
- **Reverse Proxy Timeouts**: `sites[].waf.performance.proxy_timeout` defines the maximum allowable duration when connecting and streaming responses to/from backend origin servers.

## Protection Modes & Request Body Limits {#modes-and-limits}

- **WAF Modes (`waf.mode`)**: Supports `block` (actively drops and mitigates attacks), `monitor` (logs alerts without blocking), and `off` (disables inspection). The legacy alias `log` is automatically recognized and normalized to `monitor`.
- **Request Body Size Guard (`max_body_bytes`)**: If an incoming request body exceeds the configured `max_body_bytes` limit, the data plane immediately responds with HTTP `413 Request Entity Too Large`, preventing memory exhaustion and partial-body evasion.

## Gateway Adapter Authentication & Proxy Ingress {#adapter-auth}

- **Dedicated Adapter Token (`CHEESEWAF_ADAPTER_TOKEN`)**: When integrating with external reverse proxy adapters ([CheeseWAF-Adapters](../adapters/)), callers must supply the token via the dedicated `X-CheeseWAF-Adapter-Token` HTTP header. It is not a Bearer token and must never be placed in the `Authorization` header.
- **Trusted CIDR Blocks (`trusted_cidrs`)**: By default, the trusted CIDR list is empty. When running behind an upstream proxy (such as a CDN or cloud load balancer), configure `sites[].waf.access_control.trusted_cidrs` (e.g., `127.0.0.1/32` or `::1/128`) to securely parse client IP addresses from `X-Forwarded-For`.

## Dynamic Hot-Reload Scopes {#reload}

- **Atomic In-Memory Hot Reload**: Modifying site definitions, custom regex rules, IP access lists, bot challenge policies, or ACL rules via the Web console or REST API takes effect immediately in memory without process restarts.
- **Restart Required**: Alterations to physical socket listeners (such as `server.listen` or `server.admin_listen`) require restarting the daemon process via `cheesewaf restart` or systemd.
