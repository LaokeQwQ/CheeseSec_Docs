---
title: Semantic engine
linkTitle: Semantic engine
weight: 10
description: Multi-stage decoding and AST checks. Toggle engines per site.
---

The semantic engine does **not** ship a huge regex corpus as the primary detector.
It decodes the parameter, then walks an abstract syntax tree for the enabled families.

## Enable engines {#engines}

Under `sites[].waf.semantic_engines`:

| Key | Looks for |
| --- | --- |
| `sql` | SQL injection |
| `xss` | Cross-site scripting |
| `rce` | Command / RCE |
| `lfi` | Local file include |
| `xxe` | XML external entity |
| `ssrf` | Server-side request forgery |
| `nosql` | NoSQL injection |
| `ssti` | Server-side template injection |

Turn an engine off when that family cannot appear on the site.
Do not turn them all off and expect CheeseWAF to still catch web attacks.

## Budget and allow lists {#budget}

`sites[].waf.semantic_policy`:

- `budget_exhausted_policy`: `auto` follows the `web_attack` policy when the analysis budget is spent
- `path_allowlist`: skip semantic analysis on these paths
- `param_allowlist`: skip these parameter names

`sites[].waf.performance` caps `max_body_bytes`, `max_header_bytes`, and `proxy_timeout`.

## Response inspection {#response}

`sites[].waf.response` can scan the origin body for leaked secrets (AWS key pattern, password assignments, and similar).
Keep `max_body_bytes` modest.

How isolated vs embedded hits are treated: [Isolated vs embedded](../../concepts/isolated-embedded/).
