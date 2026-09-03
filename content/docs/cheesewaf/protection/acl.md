---
title: Access Control Lists (ACL)
linkTitle: ACL
weight: 60
description: Rapid request filtering and denial based on HTTP methods, URI path prefixes, and request headers.
---

Access Control Lists (ACL) execute at the front of the traffic processing pipeline, offering ultra-low overhead filtering to immediately reject known diagnostic endpoints, probe paths, or enforce mandatory request headers. Configure ACLs under `protection.acl`, or update them dynamically via `PUT /api/protection/acl`.

## Configuration Example {#config}

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

## Schema Attributes {#fields}

| Field | Description |
| --- | --- |
| `method` | Target HTTP method (e.g., `GET`, `POST`); leave empty to match any method |
| `path_prefix` | Matching URI path prefix (e.g., `/debug`, `/actuator`) |
| `header` | HTTP header key to evaluate; leave empty if unconstrained |
| `header_value` | Expected or rejected value for the specified header |
| `action` | Action on match: `block`, `log`, or `challenge` |
| `severity` | Threat severity recorded in security logs and audit events |

{{% pageinfo color="info" %}}
ACL evaluates enabled rules in declaration order, using case-normalized method checks, literal URI-prefix comparisons, and exact case-insensitive header-value comparisons. For complex regex-based pattern matching, use [Custom Regex Rules](../custom-rules/).
{{% /pageinfo %}}
