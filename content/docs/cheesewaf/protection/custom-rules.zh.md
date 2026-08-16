---
title: 自定义规则
linkTitle: 自定义规则
weight: 20
description: 在 URI 等位置上写正则规则，带优先级和严重级别。
---

自定义规则和语义引擎并列。
适合拦管理入口探测、扫描器路径，以及个别业务拒绝。

控制台：**规则**。
REST：`/api/rules`，以及 `sites[].waf.custom_rules`。

示例自带这条规则：

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

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定编号 |
| `pattern` | 正则 |
| `location` | 匹配位置。示例用 `uri` |
| `action` | 一般是 `block` |
| `severity` | 出现在日志和审查里 |
| `priority` | 引擎排序时数字更小的更靠前。id 不要重复 |

不要在这里重写一整套 ModSecurity 规则。
自定义规则只放短、能审阅的模式。
