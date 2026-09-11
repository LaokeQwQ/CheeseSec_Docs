---
title: Unified Management Surfaces & Authorization
linkTitle: Management Surfaces
weight: 40
description: Understand the shared RBAC authorization model, unified user identity, session management, and audit pipeline across the Web console, TUI, and REST API.
---

CheeseWAF provides three dedicated management surfaces tailored for visual operations, headless terminal maintenance, and automated CI/CD workflows:

| Management Surface | Role & Intended Scenarios | Access & Invocation |
| --- | --- | --- |
| **Web Console** | Visual operations, security policy management, real-time log querying, and attack map visualization | Access the configured HTTP/HTTPS management URL after setup. Docker Compose uses HTTPS at `https://127.0.0.1:9443/` on the Docker host loopback (use an SSH tunnel for remote access). |
| **CLI / TUI** | Headless server administration, jump boxes, and rapid interactive terminal troubleshooting | Execute `waf-cli` or `cheesewaf cli` to launch the interactive terminal interface |
| **RESTful API** | CI/CD automation, external monitoring integration, and orchestration pipelines | Invoke `/api/...` endpoints using Session Cookie or Bearer API token authentication |

## Unified Identity & RBAC Matrix {#unified-auth}

When `setup.three_end_unified: true` is configured, CheeseWAF synchronizes identity and authorization across all three surfaces:

- **Universal User Credentials**: Administrator and operator accounts provisioned in the Web console can be used directly for TUI login and API authentication.
- **Consistent RBAC Enforcement**: API Tokens created in the console's System Management section inherit the exact RBAC permission matrix defined in `apisec.permissions`.
- **Granular Roles**: Built-in default roles include `admin` (holding full `["*"]` permissions) and `readonly` (scoped to `["read:*", "read:cluster"]`).
- **Exact identity fields**: Usernames use the canonical 3–32 ASCII-character form documented in the CLI reference. Roles must exactly match configured `apisec.permissions` keys; leading/trailing/embedded Unicode whitespace, control characters (`Cc`), format/invisible characters (`Cf`), and permission expressions such as `*` or `:` are rejected. The server never trims or case-normalizes identity fields.

## Operational Audit Trail {#audit}

When `apisec.audit.enabled: true` is active, all configuration mutations, policy changes, and user management operations initiated via the Web Console, TUI, or REST API are written to the structured audit log specified by `apisec.audit.path`, ensuring enterprise-grade auditability.

## Related Documentation {#references}

- [Web Console Guide](../../console/)
- [CLI & TUI Operations Manual](../../cli/)
- [REST API Reference & Permission Matrix](../../api/)
