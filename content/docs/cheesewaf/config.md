---
title: Configuration File Reference
linkTitle: Configuration
weight: 170
description: Complete structure navigation for cheesewaf.yaml, top-level key index, timeout controls, and hot-reload scopes.
---

CheeseWAF automatically generates a default `cheesewaf.yaml` configuration file within its runtime data directory under `config/` upon first launch (default `./data/config/cheesewaf.yaml`). A baseline template is maintained in the source repository at [`configs/cheesewaf.yaml`](https://github.com/LaokeQwQ/CheeseWAF/blob/dev/configs/cheesewaf.yaml).

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
| `storage` | Embedded SQLite versioned migrations, external log sinks, and backups | [Storage & Scheduling](../storage/) |
| `logging` | Access log verbosity, structured JSON formats, and log rotation | [Monitoring & Logs](../monitor/) |
| `ai` | ALAP LLM provider endpoints and asynchronous review parameters | [ALAP Review & Self-Learning](../alap/) |
| `update` | OTA automated rule updates and cryptographic signature verification | [System Operations](../operations/) |
| `scheduler` | Automated log cleanup, database backups, and daily security reports | [Storage & Scheduling](../storage/) |
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

## Dynamic Hot-Reload Scopes {#reload}

- **Atomic In-Memory Hot Reload**: Modifying site definitions, custom regex rules, IP access lists, bot challenge policies, or ACL rules via the Web console or REST API takes effect immediately in memory without process restarts.
- **Restart Required**: Alterations to physical socket listeners (such as `server.listen` or `server.admin_listen`) require restarting the daemon process via `cheesewaf restart` or systemd.
