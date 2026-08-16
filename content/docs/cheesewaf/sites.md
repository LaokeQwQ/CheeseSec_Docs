---
title: Site Management & Reverse Proxying
linkTitle: Sites
weight: 50
description: Configure public domain bindings, upstream server load balancing, health check probes, URL rewrites, and per-site security policies.
---

In CheeseWAF, a **Site** represents the primary organizational unit for reverse proxying and security enforcement. Each site associates a set of public domain hostnames (`Host` headers) with one or more backend upstream servers.

## Management & Import Interfaces {#create}

- **Web Console**: Navigate to **Sites** to visually create, edit, and tune reverse proxy definitions.
- **RESTful API**: Manage sites programmatically via `GET/POST /api/sites` and `GET/PUT/DELETE /api/sites/{id}`.
- **Nginx Configuration Import**: Automatically parse and import existing Nginx `server` configuration blocks via `POST /api/nginx/import`.

## Site Configuration Schema {#fields}

| Attribute | Configuration Key | Type & Description |
| --- | --- | --- |
| **Site ID** | `sites[].id` | Globally unique identifier string for the site |
| **Site Name** | `sites[].name` | Human-readable site label for console and log identification |
| **Domains** | `sites[].domains` | Array of strings matched against incoming HTTP `Host` headers |
| **Upstreams** | `sites[].upstreams[].address` | Upstream origin address (`host:port`), supporting optional `weight` values |
| **Dedicated Port** | `sites[].listen_port` | Optional dedicated listening port for this site |
| **Load Balancing** | `sites[].loadbalance` | Upstream distribution algorithm; defaults to `round_robin` |
| **Site Status** | `sites[].enabled` | Boolean toggle; setting to `false` disables traffic forwarding for this site |
| **WAF Protection** | `sites[].waf.enabled` | Enables active security inspection for incoming traffic |
| **Action Mode** | `sites[].waf.mode` | Enforcement mode: `block` (blocking) or `log` (monitoring only) |
| **Paranoia Level** | `sites[].waf.paranoia_level` | Paranoia level (0–5); defaults to 3 |
| **Semantic Engines** | `sites[].waf.semantic_engines` | Toggles for `sql`, `xss`, `rce`, `lfi`, `xxe`, `ssrf`, `nosql`, and `ssti` |
| **Custom Rules** | `sites[].waf.custom_rules` | Site-scoped custom regex matching rules |
| **URL Rewrites** | `sites[].waf.rewrite` | URI path internal rewrites or HTTP 3xx redirects |
| **Health Checks** | `sites[].waf.health_check` | Probe paths, intervals, and health/unhealthy thresholds |
| **Trusted CIDRs** | `sites[].waf.access_control.trusted_cidrs` | CIDR blocks of upstream load balancers/CDNs for extracting real client IPs |

## Upstream Health Checking {#health}

When `health_check.enabled: true` is active, CheeseWAF periodically sends HTTP health probes to `health_check.path` across all upstream servers:

- Origins that fail consecutive probes exceeding `unhealthy_threshold` are automatically evicted from the load balancing pool.
- Once an unhealthy node recovers and passes consecutive probes, it is dynamically restored to the active pool.

## URL Rewrites & Redirects {#rewrites}

Rewrite rules support defining `pattern` (matching regex), `replacement` (target substitution), and `redirect_code`:

- **Internal Silent Rewrite**: When `redirect_code: 0`, CheeseWAF rewrites the URI path internally in memory before forwarding upstream; the client is unaware of the transformation.
- **External Redirect**: When `redirect_code` is set to `301` or `302`, the WAF responds directly with an HTTP redirect.

## Granular Policy Overrides {#policy}

Use `sites[].waf.protection_policy` to override baseline policies defined in global `protection.policy`:

- `web_attack`: Web application vulnerability defense baseline
- `api_security`: API security and schema validation profile
- `bot_cc`: Bot mitigation and anti-scraping policy
- `threat_intel`: Threat intelligence lookup profile

Empty strings automatically inherit the global profile baseline (`smart` in default configurations).
