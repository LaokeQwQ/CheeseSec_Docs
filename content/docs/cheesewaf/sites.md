---
title: Site Management & Reverse Proxy
linkTitle: Sites
weight: 50
description: Configure host domains, upstream load balancing algorithms (round_robin/weighted/ip_hash/least_conn), active health checks, and per-site protection policies.
---

In CheeseWAF, a **Site** is the fundamental administrative unit for reverse proxying and application security policies. A site binds inbound domain names (`Host`) to one or more backend origin upstreams (`Upstream`).

## Provisioning Methods {#create}

- **Web Console**: Visual configuration, upstream monitoring, and policy tuning under the **Sites** page.
- **RESTful API**: Programmatic lifecycle automation via `GET/POST /api/sites` and `GET/PUT/DELETE /api/sites/{id}`.
- **Nginx Config Importer**: Call `POST /api/nginx/import` to parse and import existing Nginx `server` blocks directly.

## Site Configuration Schema {#fields}

| Property | YAML Key Path | Type & Description |
| --- | --- | --- |
| **Site ID** | `sites[].id` | Unique alphanumeric string identifier |
| **Site Name** | `sites[].name` | Human-readable site label |
| **Bound Domains** | `sites[].domains` | String array matching the inbound HTTP `Host` header |
| **Origin Upstreams** | `sites[].upstreams[].address` | Backend destination (`host:port`), supporting `weight` proportions |
| **Dedicated Port** | `sites[].listen_port` | Optional dedicated physical listening port for this site |
| **Load Balancing** | `sites[].loadbalance` | Algorithm choice: `round_robin`, `weighted`, `ip_hash`, `least_conn` |
| **Enabled** | `sites[].enabled` | Boolean toggle; `false` halts reverse proxying for this site |
| **WAF Enabled** | `sites[].waf.enabled` | Whether request inspection is active |
| **WAF Mode** | `sites[].waf.mode` | `block` (drop malicious requests) or `log` (record only) |
| **Paranoia Level** | `sites[].waf.paranoia_level` | Inspection strictness from 0 (disabled) to 5 (maximum paranoia), default 3 |
| **Semantic Engines** | `sites[].waf.semantic_engines` | Independent engine toggles for `sql`, `xss`, `rce`, `lfi`, `xxe`, `ssrf`, `nosql`, `ssti` |
| **Custom Rules** | `sites[].waf.custom_rules` | Site-scoped RE2 rules (supports batch CLI and Web UI import/export) |
| **Path Rewriting** | `sites[].waf.rewrite` | Internal silent path rewrite or HTTP 3xx redirection rules |
| **Health Check** | `sites[].waf.health_check` | Active probe path, check interval, and healthy/unhealthy thresholds |
| **Trusted CIDRs** | `sites[].waf.access_control.trusted_cidrs` | Fronting CDN/LB CIDR subnets for trusted client IP extraction |

## Load Balancing Algorithms {#loadbalance}

For sites fronting multiple backend upstreams, `sites[].loadbalance` provides four distribution strategies:

1. **`round_robin` (Default)**: Inbound requests rotate sequentially through all healthy upstreams. Ideal for identical backend server instances.
2. **`weighted` (Weighted Round-Robin)**: Requests are apportioned according to `upstreams[].weight` (e.g., a 3:1 weight distributes 3 out of every 4 requests to the primary upstream).
3. **`ip_hash` (Source IP Hash)**: Consistent hashing based on the client's verified IP address keeps subsequent requests from the same user pinned to the same backend for session statefulness.
4. **`least_conn` (Least In-Flight Connections)**: Dynamically routes incoming traffic to the healthy upstream with the fewest active, incomplete requests, mitigating connection backlog on slow endpoints.

## Upstream Health Checking {#health}

When `health_check.enabled: true` is set, CheeseWAF periodically issues HTTP health probes to each configured upstream path (`health_check.path`):

- When probe failures reach `unhealthy_threshold`, the node is temporarily marked unhealthy and removed from the active routing pool.
- Once the node recovers and consecutive successes meet `healthy_threshold`, traffic dispatch automatically resumes.
- If all upstreams fail health probes, circuit breaker protection activates to prevent request storm loops.

## Path Rewriting & Redirects {#rewrites}

Rewriting rules define a matching regex `pattern`, a target `replacement`, and a `redirect_code`:

- **Silent Rewrite (`redirect_code: 0`)**: The URI path is modified transparently before reaching the backend upstream without altering the browser address bar.
- **External Redirect (`redirect_code: 301` or `302`)**: Directly responds with an HTTP redirection header to the client.

## Site Custom Rules Integration {#custom-rules-site}

Each site manages an isolated list of `custom_rules`:
- Visually configured or uploaded via the **Rules** page in the Web Console.
- Automated through CI/CD pipelines using `cheesewaf rules import --site <site-id> --file <rules.yaml>`.
- Evaluated in Phase 1 at Priority 250, short-circuiting malicious probes before syntax tree generation.
