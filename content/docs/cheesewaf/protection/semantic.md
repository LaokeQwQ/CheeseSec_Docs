---
title: AST Semantic Analysis Engine
linkTitle: Semantic Engine
weight: 10
description: Modern web attack detection engine based on multi-layer recursive decoding and Abstract Syntax Tree (AST) grammar analysis, achieving 97.08% TPR on external benchmark corpora.
---

CheeseWAF's primary detection capability is powered by an Abstract Syntax Tree (AST) grammar analysis architecture rather than traditional brittle regular expressions. Inbound payloads undergo multi-layer recursive decoding (URL encoding, Unicode normalization, hex, and nested Base64) before being parsed into domain-specific syntax trees to evaluate true payload semantics.

Through systematic evaluation and remediation against 7 external real-world corpora using an independent Corpus Fidelity Classifier, the semantic engine achieves an independently verified **97.08% True Positive Rate (TPR)**.

## Engine Configuration Matrix {#engines}

Individual specialized semantic engines can be toggled per site via `sites[].waf.semantic_engines`:

| Engine Key | Attack Scope & Deep Detection Capabilities |
| --- | --- |
| `sql` | **SQL Injection**: Major SQL dialect grammar parsing; integrated **XPath injection parser**; heavy time-blind injection detection (Cartesian product / `generate_series`); whitespace comment truncation resilience |
| `xss` | **Cross-Site Scripting**: HTML/SVG tag balance analysis; obfuscated `javascript:` URI concatenation regex; `dynsrc`/`lowsrc` attribute probes; JavaScript string escaping; malformed event handler inspection |
| `rce` | **Command & Code Injection**: Comprehensive command table alignment (including `id`, `ls`, `echo`, `netstat`, `lsof`); newline command chains; automatic basename extraction for absolute executable paths; `;` + system function calls |
| `lfi` | **File Inclusion & Path Traversal**: POSIX and **Windows absolute path traversal** (smart `Program Files` exclusion to eliminate false positives); deep UTF-8 folding; SSI server-side includes (`<!--#exec`) |
| `nosql` | **NoSQL Injection**: Deep HTTP request header analysis (e.g., `X-User-Filter`); MongoDB shell escaping; isolation of malicious operators from legitimate query filter operators |
| `ssti` | **Template Injection**: Jinja2, Twig, and common template grammar trees; quoted operand probes; direct expression detection when entire value is a template expression |
| `ssrf` | **Server-Side Request Forgery**: URI parameter schema inspection; full request body URL detection treating the whole body as a potential fetch sink |
| `xxe` | **XML External Entity**: DOCTYPE entity declarations, SYSTEM/PUBLIC external resource references, and parameter entity attacks |

{{% pageinfo color="tip" %}}
In production, keeping core engines enabled is recommended. If a service clearly lacks a specific stack (such as a static site without SQL backends), disabling that engine saves CPU cycles.
{{% /pageinfo %}}

## Latency Engineering & Pre-Filter Gating {#performance}

To deliver deep syntax parsing without sacrificing microsecond-level latency, CheeseWAF employs several algorithmic safeguards:

- **Cheap Substring Gating**: Prior to expensive AST generation or complex regular expressions, constant-time substring pre-filters discard benign traffic in microseconds.
- **Worker Pool & Request Context Forking**: In Phase 2, semantic analyzers run concurrently over bounded worker goroutines with isolated context copies, merging results deterministically by priority.
- **100ms Hard Budget Deadline**: If oversized adversarial inputs consume parsing time, the global deadline prevents request processing hangs and triggers the configured fallback policy.

## Analysis Budget & Allowlists {#budget}

Fine-grained controls in `sites[].waf.semantic_policy` allow tuning parsing behavior:

- **`budget_exhausted_policy`**: Fallback action when syntax analysis exhausts its budget: `auto` (derives from web_attack level), `open` (availability-first pass), `observe` (log only), or `closed` (challenge/strict block).
- **`path_allowlist`**: URI path prefixes that bypass semantic analysis entirely.
- **`param_allowlist`**: Parameter keys excluded from deep AST inspection.

**Migration note:** The canonical location is `sites[].waf.semantic_policy.budget_exhausted_policy`. Values left in older, non-canonical configuration locations are not read; move them manually under each site's `waf.semantic_policy` block. When migrating legacy values, map `pass` to `open`, and map `block` or `challenge` to `closed` (the current closed mode prefers a challenge when analysis cannot finish). Leave the field empty or set it to `auto` to derive the effective action from the site's `web_attack` level.

Global limits can be configured in `sites[].waf.performance`, including `max_body_bytes` (default 8MB), `max_header_bytes`, and `proxy_timeout`.

## Outbound Response Inspection (Data Leak Prevention) {#response}

`sites[].waf.response` inspects upstream HTTP response bodies to prevent sensitive credential exposure:

- **Detection Scope**: Discovers AWS Access Keys, generic leaked credential patterns, and any additional patterns configured for the site. The built-in default set includes password/secret-key patterns; PEM private-key detection is available when explicitly included in `sensitive_patterns` (the shipped site template does not enable it by default).
- **Pattern Precedence**: When `sites[].waf.response.sensitive_patterns` is non-empty, it replaces the built-in defaults rather than extending them; include every pattern you need in the site-level list.
- **Tuning Advice**: For large file downloads or streaming media, restrict response inspection to JSON/HTML content types via path patterns.

For classification semantics regarding isolated attacks vs embedded long-text inputs, see [Isolated vs. Embedded Payloads](../../concepts/isolated-embedded/).
