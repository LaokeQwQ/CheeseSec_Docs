---
title: Custom rules
linkTitle: Custom rules
weight: 20
description: Regular-expression rules on URI and other locations, with priority and severity.
---

Custom rules sit next to the semantic engine.
They are useful for admin probes, scanner paths, and one-off business denials.

Console: **Rules**.
REST: `/api/rules` and `sites[].waf.custom_rules`.

The sample ships this rule:

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

| Field | Meaning |
| --- | --- |
| `id` | Stable id |
| `pattern` | Regular expression |
| `location` | Where to match. Sample uses `uri` |
| `action` | Usually `block` |
| `severity` | Shown in logs and review |
| `priority` | Lower number runs earlier when the engine sorts that way — keep ids unique |

Do not try to rebuild a full ModSecurity ruleset here.
Use custom rules for short, reviewable patterns.
