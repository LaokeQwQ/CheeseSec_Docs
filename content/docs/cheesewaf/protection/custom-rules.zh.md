---
title: 自定义正则规则
linkTitle: 自定义规则
weight: 20
description: 编写基于 Go RE2 正则表达式的高性能匹配规则，支持优先级排序、匹配位置定位、校验约束与批量导入导出。
---

自定义规则引擎（Custom Rule Engine）在检测流水线中作为 **Phase 1 预筛选器** 运行（引擎优先级为 **250**）。它先于 AST 语义分析引擎（优先级 290+）执行，主要用于拦截已知的敏感管理路径探测、扫描器指纹特征以及针对特定业务接口的定制化阻断。一旦命中 `block` 动作，请求将立即被短路拦截，避免产生高昂的语法树解析开销。

在 Web 管理控制台中可进入 **规则管理** 模块进行可视化配置与导入导出，底层对应配置项为 `sites[].waf.custom_rules`，亦可通过 CLI 命令 `cheesewaf rules` 或 REST API 进行运维管理。

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
  - id: "challenge-bot-header"
    name: "Challenge suspicious scraper header"
    pattern: "(?i)(headlesschrome|phantomjs)"
    location: "header"
    action: "challenge"
    severity: "high"
    enabled: true
    priority: 200
```

## 字段属性与合法枚举 {#fields}

| 字段名 | 类型 | 说明与合法取值约束 |
| --- | --- | --- |
| `id` | 字符串 | 规则唯一标识符，单站点内不可重复。若导入时留空，系统将自动分配规则 ID |
| `name` | 字符串 | 规则名称，用于日志记录与可视化展示 |
| `pattern` | 字符串 | 正则表达式匹配模式（采用 Go RE2 语法，单条上限 16KB，编译指令上限 8192） |
| `location` | 字符串 | 匹配目标位置，严格限定为：`uri`、`query`、`header`、`body`、`cookie`（默认 `uri`） |
| `action` | 字符串 | 命中后的处置动作，严格限定为：`block`（阻断）、`log`（仅记录）、`challenge`（人机挑战，默认 `block`） |
| `severity` | 字符串 | 威胁等级：`low`、`medium`、`high`、`critical`（默认 `medium`） |
| `priority` | 整数 | 规则执行优先级（范围 -1000000～1000000），**数值越小越先执行** |
| `enabled` | 布尔值 | 规则启停开关（默认为 `true`） |

## 安全校验与约束规范 {#validation-limits}

为防止恶意或低效规则对数据平面造成性能衰竭，CheeseWAF 引擎在加载自定义规则时实施以下严格校验：

- **容量配额限制**：单站点最多配置 **256** 条自定义规则；单次导入文档总大小不得超过 **1MB**；单站点所有规则正则字符串总长度不得超过 **256KB**。
- **复杂度与抗 ReDoS 保证**：底层依赖 Go 标准库 `regexp`（RE2 保证线性时间复杂度，根除灾难性回溯 ReDoS 隐患）。编译后程序指令数超过 8192 的复杂正则将被拒绝。
- **重复性校验**：系统强制要求单站点内不得存在重复的规则 ID；同时严格禁止存在相同匹配位置与相同正则的规则（即重复的 `location + pattern`）。

## 批量导入、导出与模板生成 {#import-export}

从最新版本开始，CheeseWAF 原生支持通过命令行和 Web 控制台以 YAML 或 JSON 格式全量导入或导出站点规则：

### 1. 命令行管理（CLI）

```bash
# 生成标准自定义规则 YAML 模板
cheesewaf rules example --format yaml --file template.yaml

# 验证并全量替换指定站点的自定义规则（自动触发平滑热载）
cheesewaf rules import --site site-prod-01 --file new-rules.yaml

# 导出指定站点的自定义规则为 JSON
cheesewaf rules export --site site-prod-01 --format json --file rules-backup.json
```

### 2. Web 控制台交互

在 Web 管理控制台的 **规则管理** 页面中，点击右上角「导入/导出」按钮：
- 支持拖拽或选择本地 `.yaml` / `.json` 文件上传。
- 支持实时校验规则语法并在提交前预览变更差异。
- 支持一键导出当前站点的全量规则备份。

## 编写与运维最佳实践 {#best-practices}

- **特征精准收敛**：自定义规则适用于高频已知的路径探测（如后台管理路径、漏洞探测扫描器特征 Header）。复杂的跨站脚本（XSS）与 SQL 注入注入语义，建议直接交给后置的 AST 语义分析引擎处理。
- **合理利用短路阻断**：将确定的恶意特征以较小的 `priority` 数值排在靠前位置，利用短路机制直接丢弃攻击请求，从而降低整体 CPU 计算开销。
