---
title: Sites and reverse proxy
linkTitle: Sites
weight: 50
description: Domains, upstreams, load balancing, health checks, and per-site WAF switches.
---

A **site** is one public hostname set plus one or more origins.
CheeseWAF is the reverse proxy in front of those origins.

## Create and edit {#create}

Console: **Sites**.
REST: `GET/POST /api/sites`, `GET/PUT/DELETE /api/sites/{id}`.
You can also import an Nginx server block with `POST /api/nginx/import`.

## Fields that matter {#fields}

| Field | Config key | Notes |
| --- | --- | --- |
| Site id | `sites[].id` | Stable id, used in URLs |
| Name | `sites[].name` | Display name |
| Domains | `sites[].domains` | Host header match |
| Upstreams | `sites[].upstreams[].address` | `host:port`, optional `weight` |
| Listen port | `sites[].listen_port` | Optional extra listener |
| Load balance | `sites[].loadbalance` | Default `round_robin` |
| Enabled | `sites[].enabled` | Off = skip this site |
| WAF on | `sites[].waf.enabled` | |
| Mode | `sites[].waf.mode` | Usually `block` |
| Paranoia | `sites[].waf.paranoia_level` | 0–5 |
| Engines | `sites[].waf.semantic_engines` | `sql`, `xss`, `rce`, `lfi`, `xxe`, `ssrf`, `nosql`, `ssti` |
| Custom rules | `sites[].waf.custom_rules` | Regex on URI or other locations |
| Rewrite | `sites[].waf.rewrite` | Path rewrite or redirect |
| Health check | `sites[].waf.health_check` | Path, interval, thresholds |
| Trusted CIDRs | `sites[].waf.access_control.trusted_cidrs` | Real client IP behind another proxy |

## Health checks {#health}

When `health_check.enabled` is true, CheeseWAF probes `health_check.path` on each upstream.
Unhealthy origins leave the pool after `unhealthy_threshold` failures.

## Rewrites {#rewrites}

A rewrite rule has `pattern`, `replacement`, and optional `redirect_code`.
`redirect_code: 0` rewrites internally.
A 3xx code sends the client to the new path.

## Per-site policy overlay {#policy}

`sites[].waf.protection_policy` can override the global `protection.policy` keys:

- `web_attack`
- `api_security`
- `bot_cc`
- `threat_intel`

Empty strings inherit the global value (`smart` in the sample).
