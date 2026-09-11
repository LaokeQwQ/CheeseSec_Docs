---
title: RESTful Management API Reference
linkTitle: REST API
weight: 160
description: Management API authentication mechanics, public and bootstrap endpoint inventory, granular RBAC permission matrix, and standard error formats.
---

CheeseWAF's management API is hosted on the process's dedicated **Management Plane** listener (default port `9443`) under the `/api` route prefix, maintaining physical listener separation from business traffic on the Data Plane. This listener is not the future standalone commercial control-plane service.

## Authentication & Authorization Schemes {#auth}

The system supports two primary authentication models:

1. **Session-Based Authentication**: Call `POST /api/auth/login` to authenticate; clients must include the returned Session Cookie in subsequent requests. All non-idempotent state-changing requests (POST, PUT, DELETE, PATCH) are verified by double-submit CSRF protection middleware.
2. **Bearer Management Tokens**: Enable `apisec.management_api.enabled`, then invoke `POST /api/system/api-tokens` (requiring `manage:api_tokens` privileges) to generate a scoped API Token. Pass the token via the standard HTTP header: `Authorization: Bearer <TOKEN>`. The secret is returned only once in the creation response; list/read endpoints return metadata, not the secret.

### Usernames and roles

Human account endpoints (`POST /api/users`, `PUT /api/users/{id}`), setup, login, storage, human JWT claims, and CAPTCHA receipts share one exact username rule: 3–32 ASCII characters, ASCII letter first, ASCII letter or digit last, and only ASCII letters, digits, `.`, `_`, and `-`. Non-ASCII characters, Unicode whitespace, control characters (`Cc`), and format/invisible characters (`Cf`) are rejected. The server never trims, lowercases, or otherwise normalizes the value.

When a request creates or updates a user, `role` must exactly match a configured key in `apisec.permissions` (normally `admin` or `readonly`). Empty or unknown roles, `*`/`:` permission expressions, and roles containing leading, trailing, or embedded Unicode whitespace, controls (`Cc`), or format/invisible characters (`Cf`) are rejected. Invalid fields return `USERNAME_INVALID` or `ROLE_INVALID`. An existing historical non-canonical username cannot be repaired through ordinary API update; inspect its immutable ID and run the local CLI command `cheesewaf user repair-username USER_ID NEW_USERNAME --reason '...'`.

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

### First-install setup URL delivery {#setup-url}

The service never prints the setup token or complete setup URL in its startup log. The log shows only the base setup URL (for example, `http://127.0.0.1:9443/setup`), the protected runtime file path (`setup.url`), and an opaque receipt.

The complete setup URL is stored in `setup.url` with mode `0600` and a 10-minute validity period. After setup completes, the setup token is revoked; expired `setup.url` files are cleaned up. The normal installation flow does not expose `ReadURLOnce` as a user-facing command.

The setup token remains required in `X-CheeseWAF-Setup-Token` until setup completes, when it is revoked. The browser reads the token from the URL fragment, clears the fragment from the address bar, and sends it only in that header. A token supplied through `CHEESEWAF_SETUP_TOKEN` before startup follows the same API validation rules and must stay out of logs and shell history.

`GET /api/setup/status` reports only whether setup is still needed. It never returns the setup URL or setup token.

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
| `read:system` / `write:system` | Software version queries and NTP time synchronization; backup/restore routes are registered but currently return 501 |
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

Management API Tokens currently support scoped permissions, notes, optional TTL/expiry, revocation, last-used metadata, and one-time secret display. The platform default lifetime is 90 days; the maximum explicit lifetime is 365 days. The service runs one coalesced cleanup worker: new tokens slide the cleanup deadline by 10 minutes, bounded by the first creation plus 60 minutes, and expired or inactive tokens (180 days without activity) are removed; audit-entry and administrator-notification attempts are made after the configuration commit.

The Web form contains an administrator-session second-confirmation flow for a non-expiring token and can send a one-time confirmation ID, but the no-expiry option remains disabled until the security confirmation verifier is configured. The current runtime has not yet wired the `ApprovalGate`, current-password/TOTP verification, or the required 10-second warning delay; without that verifier, non-expiring creation returns `API_TOKEN_CONFIRMATION_UNAVAILABLE`. This is the current compatibility boundary, not the final production TokenService.

The backup routes are not a working restore workflow yet: `POST /api/backup/export` and `POST /api/backup/restore` return HTTP 501 (`BACKUP_EXPORT_NOT_IMPLEMENTED` / `BACKUP_RESTORE_NOT_IMPLEMENTED`).

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
