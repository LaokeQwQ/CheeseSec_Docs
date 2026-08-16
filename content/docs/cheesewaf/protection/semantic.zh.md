---
title: AST 语义分析引擎
linkTitle: 语义引擎
weight: 10
description: 基于多层递归解码与抽象语法树（AST）语法分析的现代 Web 攻击检测引擎。
---

CheeseWAF 的核心检测器采用抽象语法树（AST）语法分析架构，而非传统的静态正则表达式匹配。引擎在处理入站请求时，首先对参数执行 URL 编码、Unicode、十六进制及嵌套 Base64 等多层递归解码，随后将规范化后的文本构建为特定语言的语法树，精准识别攻击载荷的语法语义。

## 语义引擎开关配置 {#engines}

在站点配置项 `sites[].waf.semantic_engines` 中，可按业务技术栈独立启用或关闭专项分析引擎：

| 引擎标识 | 目标攻击类型与检测说明 |
| --- | --- |
| `sql` | SQL 注入攻击（涵盖各种主流数据库方言的注入语法） |
| `xss` | 跨站脚本攻击（涵盖 HTML 标签闭合、事件注入与 JS 脚本上下文） |
| `rce` | 操作系统命令注入与代码执行攻击 |
| `lfi` | 本地文件包含与目录遍历（Path Traversal）攻击 |
| `xxe` | XML 外部实体注入攻击 |
| `ssrf` | 服务端请求伪造攻击 |
| `nosql` | NoSQL 数据库注入攻击（如 MongoDB 操作符注入） |
| `ssti` | 服务端模板注入攻击（涵盖 Jinja2、Twig 等主流模板引擎语法） |

{{% pageinfo color="info" %}}
建议保持核心引擎全量开启。若明确业务无对应技术栈风险（例如纯静态网站不需要 SQL 引擎），可单独关闭对应引擎以进一步优化检测耗时。
{{% /pageinfo %}}

## 分析预算与白名单控制 {#budget}

通过 `sites[].waf.semantic_policy` 可对分析耗时与特殊业务路径进行细粒度调控：

- **`budget_exhausted_policy`**：单次请求语法解析预算耗尽时的兜底策略。设为 `auto` 时将遵循全局 `web_attack` 策略。
- **`path_allowlist`**：路径白名单列表，匹配到的 URI 路径将直接跳过语义检测。
- **`param_allowlist`**：参数白名单列表，匹配到的特定参数名不执行语法分析。

在 `sites[].waf.performance` 中可进一步限制 `max_body_bytes`（请求体最大分析字节数）、`max_header_bytes` 及 `proxy_timeout`。

## 出站响应检测（敏感数据防泄露） {#response}

`sites[].waf.response` 支持对后端源站返回的响应体进行出站扫描，防止敏感凭据泄漏：

- **检测范围**：支持识别 AWS Access Key、私钥 PEM 结构及常见账号密码泄露模式。
- **性能建议**：对于大文件下载或视频流业务，建议结合路径规则将响应检测限制在 JSON/HTML 接口范围，并合理设置 `max_body_bytes`。

关于独立攻击与嵌入长文本攻击的判定逻辑，请参考 [独立特征与夹杂特征](../../concepts/isolated-embedded/)。
