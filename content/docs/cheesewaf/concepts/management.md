---
title: Three management surfaces
linkTitle: Management
weight: 40
description: Web console, CLI / TUI, and REST share one user, session, and audit model.
---

| Surface | When to use | How to reach it |
| --- | --- | --- |
| Web console | Daily ops, rules, logs, attack map | `http://127.0.0.1:9443/` after setup |
| CLI / TUI | Headless hosts, scripts | `waf-cli` or `cheesewaf panel` |
| REST | Automation, CI | `/api/...` with a session cookie or a management API token |

`setup.three_end_unified` is on in the sample config.
A user created in the console can use the CLI.
A token created under **System** can call REST with the same RBAC permissions.

Permissions live under `apisec.permissions`.
The sample grants `admin: ["*"]` and `readonly: ["read:*", "read:cluster"]`.

Audit events write to `apisec.audit.path` when `apisec.audit.enabled` is true.

See [Console](../../console/), [CLI](../../cli/), and [REST API](../../api/).
