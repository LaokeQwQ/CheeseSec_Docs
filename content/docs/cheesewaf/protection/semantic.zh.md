---
title: AST 语义分析引擎
linkTitle: 语义引擎
weight: 10
description: 基于多层递归解码与抽象语法树（AST）语法分析的现代 Web 攻击检测引擎，具备 97.08% 实网语料检出率与微秒级预筛选性能。
---

CheeseWAF 的核心检测器采用抽象语法树（AST）语法分析架构，而非传统的静态正则表达式堆叠。入站请求首先经过 URL 编码、Unicode、十六进制及嵌套 Base64 等多层递归解码，随后构建特定语言的语法树，精准识别载荷的语义意图。

经过基于 多套权威工业级实网语料库与独立标注保真度分类器（Corpus Fidelity Classifier）的大规模评测与缺口修复，语义引擎的标注可信检出率（TPR）已提升至 **97.08%**。

## 语义引擎开关配置 {#engines}

在站点配置项 `sites[].waf.semantic_engines` 中，可按业务技术栈独立启用或关闭专项分析引擎：

| 引擎标识 | 目标攻击类型与深度检测能力说明 |
| --- | --- |
| `sql` | **SQL 注入**：主流 SQL 方言语法树构建；内置 **XPath 注入解析器**；重量级时间盲注（笛卡尔积、`generate_series`）识别；注释空格截断防御 |
| `xss` | **跨站脚本**：HTML/SVG 标签闭合；**全字符离散混淆协议检测**（无死角识别如 `j a v a s c r i p t:`、CDATA 与 HTML 注释离散穿插）；混淆 `javascript:` 伪协议拼接识别；`dynsrc`/`lowsrc` 属性探针；JS 字符串逃逸；畸形事件处理器属性防护 |
| `rce` | **命令与代码执行**：系统命令表对齐（覆盖 `id`、`ls`、`echo`、`netstat`、`lsof` 等）；换行命令链；绝对路径 Basename 自动提取匹配；`;` + 系统调用组合检测 |
| `lfi` | **文件包含与目录遍历**：POSIX 与 **Windows 绝对路径识别**（智能排除 `Program Files` 等合法路径防误报）；超长 UTF-8 折叠展开；SSI 服务器包含指令（`<!--#exec`）识别 |
| `nosql` | **NoSQL 数据库注入**：支持请求头深度分析（如 `X-User-Filter`）；MongoDB Shell 语法逃逸；注入型操作符与合法过滤型操作符隔离分析 |
| `ssti` | **服务端模板注入**：Jinja2、Twig 等主流语法树识别；引号操作数探针；整值模板表达式智能绕过字段名门限分析 |
| `ssrf` | **服务端请求伪造**：入站 URL 参数协议检测；整请求体为 URL 时自动识别为 Fetch Sink 并触发防护 |
| `xxe` | **XML 外部实体注入**：DOCTYPE 实体声明、SYSTEM/PUBLIC 外部资源引用与参数实体攻击拦截 |
| `webshell` | **Webshell 与恶意脚本**：结合 PHP 执行原语分析与 **香农信息熵（Shannon Entropy $\ge$ 5.2）** 测算，精准识别长 Base64 与多层加密变形一句话木马，有效避免长重复字符、JWT 凭据及前端压缩源码误报 |

{{% pageinfo color="tip" %}}
建议在生产环境中保持核心引擎全量开启。若明确业务无对应技术栈（例如纯静态网站无需 SQL 引擎），可关闭特定引擎以进一步减少单次请求的 CPU 耗时。
{{% /pageinfo %}}

## 性能保障与低时延设计 {#performance}

为了在具备深层语法分析能力的同时保持微秒级的极低延迟，引擎实现了以下优化机制：

- **廉价子串门限前置（Substring Pre-Filters）**：在执行复杂的语法树解析或高成本正则前，先通过常数时间（O(1) 或 O(n)）的廉价特征子串门限进行初筛，无潜在风险的正常业务参数在微秒级直接跳过。
- **并发 Worker 池与请求上下文隔离**：多个语义分析器在 Phase 2 阶段通过并发 Worker 协程池执行，检测上下文互不干扰，并在结束时按照优先级确定性合并结果。
- **100ms 硬超时防线**：若遭遇超大畸形请求体导致计算耗尽，流水线将根据 `budget_exhausted_policy` 触发安全兜底，绝不拖垮宿主机。

## 分析预算与白名单控制 {#budget}

通过 `sites[].waf.semantic_policy` 可对分析耗时与特殊业务路径进行细粒度调控：

- **`budget_exhausted_policy`**：单次请求语法解析预算耗尽时的兜底策略。可选 `auto`（默认，遵循 web_attack 策略等级）、`open`（放行可用优先）、`observe`（仅记录观察）或 `closed`（挑战/严格拦截）。
- **`path_allowlist`**：路径白名单列表，匹配到的 URI 路径将直接跳过语义检测。
- **`param_allowlist`**：参数白名单列表，匹配到的特定参数名不执行语法分析。

**迁移说明：** 规范配置路径为 `sites[].waf.semantic_policy.budget_exhausted_policy`。旧版本若将该字段放在其他非规范路径，当前版本不会读取，请手动移动到每个站点的 `waf.semantic_policy` 下。迁移旧枚举时，将 `pass` 映射为 `open`，将 `block` 或 `challenge` 映射为 `closed`（当前 `closed` 在分析无法完成时优先挑战）。留空或设置为 `auto` 时，实际策略会根据站点 `web_attack` 等级推导。

在 `sites[].waf.performance` 中可进一步限制 `max_body_bytes`（请求体最大分析字节数，默认 8MB）、`max_header_bytes` 及 `proxy_timeout`。

## 出站响应检测（敏感数据防泄露） {#response}

`sites[].waf.response` 支持对后端源站返回的响应体进行出站扫描，防止敏感凭据泄漏：

- **检测范围**：支持识别 AWS Access Key、常见账号密码泄露模式及站点自定义敏感模式（注意：站点自定义 `sensitive_patterns` 将覆盖系统默认规则，默认配置下 PEM 私钥扫描未激活，可在 `sensitive_patterns` 中按需配置启用）。
- **性能建议**：对于大文件下载或视频流业务，建议结合路径规则将响应检测限制在 JSON/HTML 接口范围，并合理设置 `max_body_bytes`。

关于独立攻击与嵌入长文本攻击的判定逻辑，请参考 [独立特征与夹杂特征](../../concepts/isolated-embedded/)。
