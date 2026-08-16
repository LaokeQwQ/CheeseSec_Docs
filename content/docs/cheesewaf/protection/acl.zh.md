---
title: ACL
linkTitle: ACL
weight: 60
description: 按 HTTP 方法、路径前缀和请求头允许或拒绝。
---

配置：`protection.acl`。
REST：`PUT /api/protection/acl`。

示例拒绝 `/debug`：

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

`method` 为空表示任意方法。
同时填 `header` 和 `header_value`，可以要求或拒绝某个请求头。

ACL 很靠前。
已知的垃圾路径用它。
需要正则而不是前缀时，用 [自定义规则](../custom-rules/)。
