---
title: 自定义正则规则
linkTitle: 自定义规则
weight: 20
description: 编写基于正则表达式的高性能匹配规则，支持优先级排序、匹配位置定位与威胁等级标记。
---

自定义规则与 AST 语义引擎并列运行，主要用于拦截常见的敏感管理路径探测、扫描器指纹特征以及针对特定业务接口的定制化阻断需求。

在 Web 管理控制台中可进入 **规则管理** 模块进行可视化配置，底层对应配置项为 `sites[].waf.custom_rules`，或通过 REST API `/api/rules` 进行增删改查。

## 规则配置示例 {#example}

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

## 字段属性说明 {#fields}

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `id` | 字符串 | 规则全局唯一标识符，不可重复 |
| `name` | 字符串 | 规则名称，用于日志记录与可视化展示 |
| `pattern` | 字符串 | 正则表达式匹配模式（支持 Go RE2 正则语法） |
| `location` | 字符串 | 匹配目标位置，常用取值包括 `uri`、`header`、`param` 等 |
| `action` | 字符串 | 触发后的处置动作，通常为 `block`（阻断）或 `log`（仅记录） |
| `severity` | 字符串 | 威胁严重等级（如 `low`、`medium`、`high`、`critical`） |
| `priority` | 整数 | 规则执行优先级，数值越小优先级越高，优先执行评估 |
| `enabled` | 布尔值 | 规则启停开关 |

## 编写与运维建议 {#best-practices}

- **专注特征收敛**：自定义规则适用于高频已知的探测特征（如敏感路径、固化 Header），通用 Web 攻击（如复杂的 SQL 注入与 XSS）建议交由 AST 语义分析引擎处理，避免在自定义规则中维护冗长庞杂的正则表达式库。
- **验证正则效率**：编写正则时应避免出现灾难性回溯（Catastrophic Backtracking）模式，确保高并发下的匹配性能。
