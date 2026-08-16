---
title: Custom Regular Expression Rules
linkTitle: Custom Rules
weight: 20
description: Author high-performance regex matching rules with location targeting, priority ordering, and severity level assignments.
---

Custom rules operate in parallel with the AST semantic engine. They are primarily designed for blocking sensitive path probing, scanning tool signatures, and enforcing specific application business constraints.

Configure custom rules visually in the Web console under **Rules**, declare them in configuration files via `sites[].waf.custom_rules`, or manage them programmatically via `/api/rules`.

## Rule Configuration Example {#example}

```yaml
custom_rules:
  - id: "block-admin-probe"
    name: "Admin path probe"
    pattern: "(?i)/(wp-admin|phpmyadmin|\\.git)"
    location: "uri"
    action: "block"
    severity: "medium"
    enabled: true
    priority: 180
```

## Attribute Schema Reference {#fields}

| Field Name | Type | Description |
| --- | --- | --- |
| `id` | String | Globally unique rule identifier |
| `name` | String | Human-readable rule title for logs and dashboard display |
| `pattern` | String | Regular expression string (Go RE2 syntax) |
| `location` | String | Target evaluation location, such as `uri`, `header`, or `param` |
| `action` | String | Action to take upon match: `block` (terminate request) or `log` (record only) |
| `severity` | String | Severity rating: `low`, `medium`, `high`, or `critical` |
| `priority` | Integer | Evaluation priority; lower integers are evaluated earlier |
| `enabled` | Boolean | Rule activation toggle |

## Best Practices & Authoring Guidelines {#best-practices}

- **Focus on Known Signatures**: Custom rules are ideal for concise, verifiable patterns (such as `.git` probes or diagnostic endpoints). General web vulnerabilities (e.g., complex SQLi and XSS) should be handled by the AST semantic engine rather than bloated regex libraries.
- **Regex Performance**: Ensure regular expressions avoid catastrophic backtracking patterns to preserve high-concurrency throughput.
