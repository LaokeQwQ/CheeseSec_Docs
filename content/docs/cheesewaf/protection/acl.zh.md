---
title: 访问控制列表（ACL）
linkTitle: ACL
weight: 60
description: 基于 HTTP 请求方法、URI 路径前缀及请求头的快速放行与阻断控制。
---

访问控制列表（ACL）位于流量处理流水线的前端，用于以极低的计算开销快速拦截已知无用的调试路由、探测路径或强制校验指定请求头。配置位于 `protection.acl`，支持通过 REST API `PUT /api/protection/acl` 进行热更新。

## 配置示例 {#config}

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

## 匹配字段说明 {#fields}

| 字段 | 说明 |
| --- | --- |
| `method` | 目标 HTTP 方法（如 `GET`、`POST`）；留空表示匹配任意方法 |
| `path_prefix` | 匹配的 URI 路径前缀（如 `/debug`、`/actuator`） |
| `header` | 待检查的 HTTP 请求头名称；留空表示不限制 |
| `header_value` | 对应请求头的期望值或排斥值 |
| `action` | 命中后的处置动作，支持 `block`（拦截）、`log`（记录）或 `challenge`（人机挑战） |
| `severity` | 记录在告警日志与审计事件中的威胁等级 |

{{% pageinfo color="info" %}}
ACL 按配置顺序线性遍历启用的规则，对 HTTP 方法做大小写归一化匹配，对 URI 做字面路径前缀比较，并对请求头值做不区分大小写的精确比较。若匹配规则需要复杂的正则表达式支持，请使用 [自定义正则规则](../custom-rules/)。
{{% /pageinfo %}}
