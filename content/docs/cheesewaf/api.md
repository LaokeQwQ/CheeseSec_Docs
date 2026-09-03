---
title: RESTful Management API Reference
linkTitle: REST API
weight: 160
description: Management API authentication mechanics, public and bootstrap endpoint inventory, granular RBAC permission matrix, and standard error formats.
---

CheeseWAF's management API is hosted strictly on the **Control Plane** (default port `9443`) under the `/api` route prefix, maintaining complete physical and logical isolation from business traffic on the Data Plane.

## Authentication & Authorization Schemes {#auth}

The system supports two primary authentication models:

1. **Session-Based Authentication**: Call `POST /api/auth/login` to authenticate; clients must include the returned Session Cookie in subsequent requests. All non-idempotent state-changing requests (POST, PUT, DELETE, PATCH) are verified by double-submit CSRF protection middleware.
2. **Bearer Management Tokens**: Invoke `POST /api/system/api-tokens` (requiring `manage:api_tokens` privileges) to generate scoped API Tokens. Pass the token via the standard HTTP header: `Authorization: Bearer <TOKEN>`.

### Public Unauthenticated Endpoints

The following read-only, login, or challenge endpoints can be accessed without a prior session or bearer token. A configured public Prometheus path is also unauthenticated when `monitor.prometheus.public: true`; its path is deployment-specific.

| HTTP Method | Route Path | Description & Purpose |
| --- | --- | --- |
| `GET` | `/health`, `/health/live`, `/health/ready`, `/health/cluster` | System and cluster health diagnostic probes |
| `GET` | `/api/auth/login-options` | Retrieves login security settings (e.g., CAPTCHA/2FA requirements) |
| `POST` | `/api/auth/captcha`, `/api/auth/captcha/verify` | Generates and verifies login CAPTCHA challenges |
| `POST` | `/api/auth/login` | Administrator authentication endpoint |
| `GET` | `/api/setup/status` | Reports whether first-install setup is still required; does not mutate state |

### Bootstrap and Node-Authenticated Endpoints

These routes are mounted outside the normal management-token middleware, but they are **not anonymous operations**:

- `POST /api/setup` and `POST /api/setup/probe` require the setup token in `X-CheeseWAF-Setup-Token`, and are accepted only while setup is incomplete.
- `GET /api/setup/draft` requires the setup-session cookie issued by the probe; `PATCH /api/setup/draft` requires that cookie plus the setup token.
- `POST /api/cluster/join` requires a one-time join token and a node CSR. The controller validates the token and enrolls the node; it is not a public membership endpoint.
- `POST /api/cluster/nodes/{id}/heartbeat` requires a verified mTLS client certificate for an enrolled, non-revoked node (certificate identity/serial must match the registration).

## RBAC Permission Matrix Reference {#permissions}

Router middleware validates token permissions against the following identifiers:

| Permission Prefix | Functional Area & Covered Capabilities |
| --- | --- |
| `read:sites` / `write:sites` | Query, create, update, and delete site definitions; issue ACME certificates |
| `read:rules` / `write:rules` | Custom regex security rule management |
| `read:protection` / `write:protection` | IP access lists, ACL rules, bot challenge policies, and ALAP decisions |
| `read:threat_intel` / `write:threat_intel` | Threat intelligence feed management, synchronization, and IP lookups |
| `read:edge` / `write:edge` | Edge response headers, static caching rules, and compression profiles |
| `read:ai` / `write:ai` / `use:ai` / `approve:ai` | AI LLM configurations, assistant conversations, and high-risk tool approvals |
| `read:cluster` / `write:cluster` | Cluster node monitoring, join token issuance, and rolling upgrades |
| `read:system` / `write:system` | Software version queries, NTP time synchronization, and backup/restore |
| `manage:api_tokens` | Create, query, and revoke management API tokens |
| `read:users` / `write:users` | Administrator user accounts, roles, and TOTP 2FA configuration |
| `read:logs` | Query access logs and retrieve ALAP review queue items |
| `read:monitor` | System performance metrics, Prometheus scraping, and notification channels |
| `read:audit` | Query operational audit logs |
| `read:realtime` | Server-Sent Events stream (`/api/realtime/events`) and WebSocket feeds |
| `read:ops` / `write:ops` | Built-in task scheduler and automated maintenance routines |
| `read:storage` / `write:storage` | Storage status, external log sink configuration, and disk cleanup |
| `read:apisec` | Discovered API asset inventory and OpenAPI schema definitions |

Roles assigned `admin: ["*"]` possess unrestricted global API access.

## Standard Error Formats {#errors}

API failures return appropriate HTTP status codes accompanied by a structured JSON error response:

```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid request parameter",
    "trace_id": "1a2b3c4d5e6f",
    "event_id": "1a2b3c4d5e6f"
  }
}
```

If a login attempt fails due to CAPTCHA validation (HTTP 401/403), request a new challenge context via `/api/auth/captcha` before re-submitting credentials.
