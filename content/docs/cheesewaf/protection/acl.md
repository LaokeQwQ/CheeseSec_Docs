---
title: ACL
linkTitle: ACL
weight: 60
description: Deny or allow by HTTP method, path prefix, and header.
---

Config: `protection.acl`.
REST: `PUT /api/protection/acl`.

The sample denies `/debug`:

```yaml
protection:
  acl:
    enabled: true
    rules:
      - id: "deny-debug"
        name: "Deny debug endpoints"
        method: ""
        path_prefix: "/debug"
        header: ""
        header_value: ""
        action: "block"
        severity: "high"
        enabled: true
```

Empty `method` means any method.
Set `header` + `header_value` to require or reject a header.

ACL runs early.
Use it for operator-known junk paths.
Use [custom rules](../custom-rules/) when you need a regex, not a prefix.
