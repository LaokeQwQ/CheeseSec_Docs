---
title: Custom Regex Rules
linkTitle: Custom Rules
weight: 20
description: High-performance Go RE2 regular expression rules with priority ordering, target location matching, strict validation limits, and batch import/export.
---

The Custom Rule Engine operates as a **Phase 1 Pre-Filter** in the request pipeline (engine priority **250**). It executes prior to the AST Semantic Analysis Engine (priority 290+). Custom rules are designed to intercept high-frequency reconnaissance, scanner headers, and custom application path blocks. When a rule triggers with a `block` action, execution short-circuits immediately, eliminating unnecessary AST parsing overhead.

You can manage custom rules visually in the **Rules** section of the Web Console (`sites[].waf.custom_rules`), via the `cheesewaf rules` CLI utility, or using REST APIs.

## Configuration Example {#example}

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
  - id: "challenge-bot-header"
    name: "Challenge suspicious scraper header"
    pattern: "(?i)(headlesschrome|phantomjs)"
    location: "header"
    action: "challenge"
    severity: "high"
    enabled: true
    priority: 200
```

## Field Reference & Valid Enumerations {#fields}

| Field | Type | Description & Validation Constraints |
| --- | --- | --- |
| `id` | String | Globally unique rule ID within the site. If omitted during import, the engine generates one automatically |
| `name` | String | Human-readable rule title for logging and UI display |
| `pattern` | String | Regular expression pattern (Go RE2 syntax; max 16KB per pattern, max 8192 compiled instructions) |
| `location` | String | Target inspection location. Strictly limited to: `uri`, `query`, `header`, `body`, `cookie` (default `uri`) |
| `action` | String | Action on match. Strictly limited to: `block`, `log`, `challenge` (default `block`) |
| `severity` | String | Threat level: `low`, `medium`, `high`, `critical` (default `medium`) |
| `priority` | Integer | Rule execution priority (-1,000,000 to 1,000,000). **Lower numbers execute first** |
| `enabled` | Boolean | Rule enable flag (default `true`) |

## Security Constraints & Quota Limits {#validation-limits}

To prevent malformed or unbounded rules from causing performance degradation, the configuration validator enforces strict boundaries:

- **Resource Limits**: A single site supports up to **256** custom rules (`maxCustomRulesCount = 256`). Import document size must not exceed **1MB**, and total pattern length across all rules cannot exceed **256KB**.
- **ReDoS Immunity**: Backed by Go's `regexp` (RE2 guarantees linear-time execution, eliminating catastrophic backtracking ReDoS). Expressions exceeding 8192 compiled program instructions are rejected.
- **Deduplication Check**: Rule IDs must be unique within each site. Duplicate `location + pattern` combinations are strictly rejected.

## Batch Import, Export & Template Generation {#import-export}

CheeseWAF provides seamless CLI and Web UI workflows for importing and exporting rules in YAML and JSON:

### 1. CLI Management

```bash
# Generate official custom rule YAML template
cheesewaf rules example --format yaml --file template.yaml

# Validate and replace custom rules for a target site (triggers smooth daemon hot-reload)
cheesewaf rules import --site site-prod-01 --file new-rules.yaml

# Export custom rules of a site to JSON
cheesewaf rules export --site site-prod-01 --format json --file rules-backup.json
```

### 2. Web Management Console

In the **Rules** page of the Web Console, click the **Import / Export** button in the header:
- Drag and drop or upload local `.yaml` or `.json` rule definition files.
- Inspect syntax validation and preview differences prior to committing.
- Download a full JSON or YAML rule backup with a single click.

## Operational Best Practices {#best-practices}

- **Focus on Definitive Signatures**: Use custom rules for known static probes (admin interfaces, sensitive files, scanner fingerprints). Defer complex application injection patterns (SQL injection, XSS) to the AST semantic engine.
- **Leverage Short-Circuiting**: Order high-confidence malicious signatures with lower `priority` numbers to drop bad traffic early, minimizing server CPU load.
