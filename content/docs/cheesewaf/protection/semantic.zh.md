---
title: 语义引擎
linkTitle: 语义引擎
weight: 10
description: 多层解码和语法树检查。每个站点可以开关各类引擎。
---

语义引擎的主检测器 **不是** 一份巨大的正则库。
它先解码参数，再按打开的类型走抽象语法树。

## 打开引擎 {#engines}

配置在 `sites[].waf.semantic_engines`：

| 键 | 查找对象 |
| --- | --- |
| `sql` | SQL 注入 |
| `xss` | 跨站脚本 |
| `rce` | 命令执行 / RCE |
| `lfi` | 本地文件包含 |
| `xxe` | XML 外部实体 |
| `ssrf` | 服务端请求伪造 |
| `nosql` | NoSQL 注入 |
| `ssti` | 服务端模板注入 |

这个站点不可能出现某类攻击时，再关掉对应引擎。
不要把引擎全关了，还指望 CheeseWAF 挡住 Web 攻击。

## 预算和白名单 {#budget}

`sites[].waf.semantic_policy`：

- `budget_exhausted_policy`：分析预算用尽时，`auto` 跟随 `web_attack` 策略
- `path_allowlist`：这些路径不做语义分析
- `param_allowlist`：这些参数名跳过

`sites[].waf.performance` 限制 `max_body_bytes`、`max_header_bytes` 和 `proxy_timeout`。

## 响应检查 {#response}

`sites[].waf.response` 可以扫描源站响应体里泄露的密钥（AWS 密钥形态、password 赋值等）。
把 `max_body_bytes` 控制在合理范围。

独立命中和夹杂命中怎么处理，见 [独立特征与夹杂特征](../../concepts/isolated-embedded/)。
