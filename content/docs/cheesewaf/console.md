---
title: Web Management Console
linkTitle: Web Console
weight: 140
description: Modern React single-page console navigation, functional route mappings, and secure operational mechanisms.
---

CheeseWAF embeds a modern single-page Web management console built with React and hosted directly by the Control Plane. After completing [System Initialization](../tutorial/setup/), navigate to the management address (default `http://127.0.0.1:9443/`) to access the dashboard.

The console enforces secure session cookie management alongside strict double-submit CSRF mitigation, with optional [Login CAPTCHA Protection](../protection/bot-captcha/#login) on the authentication screen.

## Console Route Mapping Reference {#pages}

| Frontend Route | Functional Module & Role | Documentation Reference |
| --- | --- | --- |
| `/` | Dashboard: Real-time QPS, block counts, and threat status cards | [Monitoring & Logs](../monitor/) |
| `/sites` | Site Management: Domain bindings, upstreams, and load balancing | [Site Management](../sites/) |
| `/ssl` | SSL Certificates: Manual certificate uploads and ACME automation | [TLS & Certificates](../tls/) |
| `/rules` | Custom Rules: Regular expression matching rule management | [Custom Regex Rules](../protection/custom-rules/) |
| `/review` | Threat Review: ALAP out-of-band sample analysis and rule commitment | [ALAP Review & Self-Learning](../alap/) |
| `/logs` | Log Explorer: Trace ID lookups and multi-dimensional query filters | [Monitoring & Logs](../monitor/) |
| `/ip` | IP Management: IP access lists, GeoIP country bans, and threat feeds | [IP, GeoIP & Fingerprints](../protection/ip-geo-fingerprint/) |
| `/protection` | Protection: AST semantic engines and policy baseline configuration | [Security Protection Policies](../protection/) |
| `/bot-challenge` | Bot Challenge: JS challenges, slider puzzles, and waiting rooms | [Bot & CAPTCHA](../protection/bot-captcha/) |
| `/edge` | Edge Optimization: Header rewrites, static caching, and compression | [Edge Features](../edge/) |
| `/ai` | AI Settings: LLM connectivity parameters and auto-agreement | [ALAP Review & Self-Learning](../alap/) |
| `/monitor` | Monitoring & Alerts: Prometheus metrics export and Webhooks | [Monitoring & Logs](../monitor/) |
| `/apisec` | API Security: Asset discovery, schema contracts, and rate limiting | [API Security & Governance](../api-security/) |
| `/users` | User Management: Administrative credentials, RBAC roles, and 2FA | [System Operations](../operations/) |
| `/ops` | Operations & Scheduling: Automated tasks, cleanup, and maintenance | [Storage & Scheduling](../storage/) |
| `/updates` | Updates: Software version checks and OTA rule updates | [System Operations](../operations/) |
| `/block-pages` | Block Pages: Template customization and sandbox live previews | [Block Response Pages](../protection/block-page/) |
| `/attack-map` | Threat Map: Global geographic threat visualization and metrics | [Monitoring & Logs](../monitor/) |
| `/cluster` | Cluster Management: Node status, certificate rotation, and upgrades | [High Availability Clustering](../cluster/) |
| `/system` | System Configuration: Runtime settings, NTP, and backup/restore | [System Operations](../operations/) |
| `/captcha-lab` | CAPTCHA Lab: Interactive puzzle debugging and custom branding | [Bot & CAPTCHA](../protection/bot-captcha/) |

UI themes (Light, Dark, and custom accent palettes) are persisted in local browser storage and have no effect on Data Plane request inspection.
