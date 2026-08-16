---
title: AST Semantic Analysis Engine
linkTitle: Semantic Engine
weight: 10
description: Modern Web Application Firewall engine leveraging multi-stage recursive decoding and Abstract Syntax Tree (AST) grammar analysis.
---

CheeseWAF's core detector employs Abstract Syntax Tree (AST) grammar analysis rather than traditional static regular expression matching. When evaluating incoming requests, the engine first applies multi-layer recursive decoding across URL encoding, Unicode, hexadecimal notation, and nested Base64 strings. It then constructs language-specific syntax trees to accurately evaluate the semantic context of potential payloads.

## Semantic Engine Family Configuration {#engines}

Under `sites[].waf.semantic_engines`, specific semantic analysis modules can be enabled or disabled based on your application's technology stack:

| Engine Key | Target Attack Vector & Description |
| --- | --- |
| `sql` | SQL Injection attacks across major SQL dialect grammars |
| `xss` | Cross-Site Scripting (XSS) in HTML tag, attribute, and JavaScript contexts |
| `rce` | Operating system command injection and arbitrary code execution |
| `lfi` | Local File Inclusion (LFI) and path traversal exploits |
| `xxe` | XML External Entity (XXE) injection attacks |
| `ssrf` | Server-Side Request Forgery (SSRF) constructs |
| `nosql` | NoSQL injection payloads (e.g., MongoDB query operator manipulation) |
| `ssti` | Server-Side Template Injection (SSTI) across Jinja2, Twig, and related engines |

{{% pageinfo color="info" %}}
Maintaining all core engines enabled is recommended. If your application definitely does not use a specific technology stack (for example, a purely static site with no SQL backend), disabling that engine can optimize inspection latency.
{{% /pageinfo %}}

## Analysis Budget & Allowlist Controls {#budget}

Fine-tune execution timeouts and bypasses in `sites[].waf.semantic_policy`:

- **`budget_exhausted_policy`**: Fallback policy when AST parsing exhausts the allotted execution time budget. Setting to `auto` inherits the global `web_attack` policy.
- **`path_allowlist`**: Array of URI paths exempt from semantic inspection.
- **`param_allowlist`**: Array of query/body parameter keys exempt from AST parsing.

In `sites[].waf.performance`, you can further enforce `max_body_bytes` (maximum body bytes to parse), `max_header_bytes`, and `proxy_timeout`.

## Outbound Response Inspection (Credential Leak Prevention) {#response}

`sites[].waf.response` inspects responses returned by backend origin servers to prevent accidental leakage of sensitive credentials:

- **Detection Scope**: Identifies exposed AWS Access Keys, private key PEM headers, and common password assignment patterns.
- **Performance Advice**: For large file downloads or streaming media, restrict response inspection to JSON/HTML paths and configure appropriate `max_body_bytes` limits.

For details on how isolated vs. embedded attacks are evaluated, see [Isolated vs. Embedded Payloads](../../concepts/isolated-embedded/).
