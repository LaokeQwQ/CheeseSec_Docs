---
title: REST API
linkTitle: REST API
weight: 160
description: Health endpoints, session login, management tokens, CSRF, and the permission map.
---

The management API lives under `/api` on the **admin listener**, not on the data plane.

## Auth {#auth}

Two ways in after setup:

1. **Session.** `POST /api/auth/login`, then send the session cookie. State-changing calls need the CSRF middleware.
2. **Management token.** Create one at `POST /api/system/api-tokens` (`manage:api_tokens`). Send it as a bearer token on later calls.

Public before login:

| Method | Path |
| --- | --- |
| GET | `/health`, `/health/live`, `/health/ready`, `/health/cluster` |
| GET | `/api/auth/login-options` |
| POST | `/api/auth/captcha`, `/api/auth/captcha/verify`, `/api/auth/login` |
| POST | `/api/setup`, `/api/setup/probe` |
| GET/PATCH | `/api/setup/draft` |
| POST | `/api/cluster/join` |
| POST | `/api/cluster/nodes/{id}/heartbeat` |

## Permission map {#permissions}

Common `require("…")` names from the router:

| Prefix | Examples |
| --- | --- |
| `read:` / `write:` `sites` | List and edit sites, ACME issue |
| `read:` / `write:` `rules` | Custom rules |
| `read:` / `write:` `protection` | IP, ACL, bot, rate limit, review decide |
| `read:` / `write:` `threat_intel` | Import, sync, lookup |
| `read:` / `write:` `edge` | Header / cache / compression policy |
| `read:` / `write:` `ai`, `use:ai`, `approve:ai` | Config, analyze, assistant, approvals |
| `read:` / `write:` `cluster` | Nodes, join tokens, rolling upgrade |
| `read:` / `write:` `system` | Version, time sync, backup |
| `manage:api_tokens` | Create and revoke tokens |
| `read:` / `write:` `users` | Local users and 2FA |
| `read:` `logs` | Access logs and review list |
| `read:` `monitor` | Stats, metrics, notifications |
| `read:` `audit` | Audit log |
| `read:` `realtime` | SSE `/api/realtime/events`, WebSocket `/api/realtime/ws` |
| `read:` / `write:` `ops` | Scheduler |
| `read:` / `write:` `storage` | Stats and cleanup |
| `read:` `apisec` | Discovered endpoints |

`admin: ["*"]` in the sample bypasses individual checks.

## Errors {#errors}

Failed calls return JSON with an error field and an HTTP status.
Do not retry login blindly after a CAPTCHA failure — request a new challenge.
