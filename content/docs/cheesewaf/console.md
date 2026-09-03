---
title: Web Management Console
linkTitle: Console
weight: 140
description: Modern React-based single-page management console navigation, module routing matrix, and security mechanisms.
---

CheeseWAF includes a modern single-page visual management console built with React and hosted directly by the control plane daemon. After completing [System Setup](../tutorial/setup/), navigate to the configured management endpoint. Standalone deployments may use the configured HTTP/HTTPS scheme; the official Docker Compose file publishes the admin listener as HTTPS on the Docker host loopback, so use `https://127.0.0.1:9443/` there (or an SSH tunnel), not a remote host URL unless you explicitly change the bind address.

The console enforces session cookie statefulness with strict double-submit CSRF defenses (dynamically adjusting `Secure` flags when running on unencrypted local loops and enforcing them under HTTPS), and supports enabling [CAPTCHA challenges on login](../protection/bot-captcha/#login).

## Console Routing Matrix {#pages}

| Frontend Route | Module Scope & Capabilities | Documentation Reference |
| --- | --- | --- |
| `/` | Dashboard: Real-time QPS, drop statistics, and security summaries | [Monitoring & Logs](../monitor/) |
| `/sites` | Sites: Domain mappings, upstream origins, 4 load balancing algorithms, and health checks | [Site Management](../sites/) |
| `/ssl` | SSL Certificates: Certificate upload and automated ACME renewals | [TLS & Certificates](../tls/) |
| `/rules` | Rules: Site custom regex rules, YAML/JSON batch import/export, and live RE2 validation | [Custom Rules](../protection/custom-rules/) |
| `/review` | Threat Review: ALAP offline threat triage, decision claims, and rule promotion | [ALAP Review](../alap/) |
| `/logs` | Log Explorer: Trace ID lookups and multi-dimensional query filters | [Monitoring & Logs](../monitor/) |
| `/ip` | IP Management: IP allow/denylists, GeoIP restrictions, and threat feeds | [IP, Geo & Fingerprints](../protection/ip-geo-fingerprint/) |
| `/protection` | Protection: AST semantic engine toggles and paranoia levels | [Security Policies](../protection/) |
| `/bot-challenge` | Bot Protection: JS challenges, slider CAPTCHAs, and waiting room policies | [Bot & CAPTCHA](../protection/bot-captcha/) |
| `/edge` | Edge: Header rewriting, static caching, and Gzip/Brotli compression | [Edge Features](../edge/) |
| `/ai` | AI Settings: Model connectivity, self-learning jobs, and automated adoption | [ALAP Review](../alap/) |
| `/monitor` | Monitoring & Alerts: Prometheus metrics, Remote Write, and Webhook alerts | [Monitoring & Logs](../monitor/) |
| `/apisec` | API Security: Endpoint discovery, schema validation, and rate limiting | [API Security](../api-security/) |
| `/users` | User Management: Administrator accounts, role scopes, and 2FA credentials | [Operations](../operations/) |
| `/ops` | Operations & Cron: Automated task scheduler and log maintenance | [Storage & Scheduling](../storage/) |
| `/updates` | Updates: Version checks and signed OTA release updates | [Operations](../operations/) |
| `/block-pages` | Block Pages: Response templates, HTML sanitization, and sandboxed preview | [Block Pages](../protection/block-page/) |
| `/attack-map` | Threat Map: Global attack visualization with official borders and 100% offline 3D Earth | [Monitoring & Logs](../monitor/) |
| `/cluster` | Cluster: Node health, token issuance, certificate rotation, Ansible playbooks, and rolling upgrades | [Cluster HA](../cluster/) |
| `/system` | System: Runtime configurations, NTP synchronization, and backup/restore | [Operations](../operations/) |
| `/captcha-lab` | CAPTCHA Lab: Interactive puzzle testing and asset debugging | [Bot & CAPTCHA](../protection/bot-captcha/) |

The console provides light, dark, and custom color accents. Visual preferences are stored locally in the browser and do not impact data plane operations.
