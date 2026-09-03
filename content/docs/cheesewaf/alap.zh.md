---
title: ALAP 异步审查与自学习机制
linkTitle: ALAP
weight: 100
description: 异步大模型威胁审查队列、自动化规则采纳、AI 助手工具调用审批与自学习分析。
---

ALAP（AI Large-Language-Model Auto Pilot）是 CheeseWAF 的智能旁路分析大脑。它通过与数据平面完全解耦的异步队列机制，将大语言模型的泛化语义理解能力引入威胁检测流程，同时保障核心转发链路的零延迟开销。

在 Web 管理控制台中对应 **AI 配置** 与 **威胁审查** 模块，底层配置块为 `ai`。

## 1. 异步审查队列与并发索赔机制 {#queue}

在数据平面向客户端完成响应交付后，命中特定防护策略的边界样本与夹杂特征请求会被推入后台异步审查队列：

- **模型适配层**：后台 Worker 会根据 `ai.provider` 适配 OpenAI Chat Completions 或 Anthropic Messages 协议格式发起外部推理请求。
- **异步安全原则**：始终保持配置中 `ai.async: true`，数据平面不产生任何针对模型返回的同步阻塞等待。
- **并发索赔与队列保护（Decision Claims）**：多管理员协作时，底层存储引擎通过原子索赔机制（`review_decisions` 锁）锁定待审样本，防止多人并发重复判定，并设定最大保留周期自动清理陈旧样本。

## 2. 威胁研判与处置流程 {#decisions}

安全运维人员可通过控制台或 REST API 审查分析结果：

- **查询待审队列**：调用 `GET /api/review` 获取待研判样本列表与模型评分。
- **人工决策提交**：调用 `POST /api/review/{id}/decide` 记录处置决定（确认为攻击、误报放行或沉淀为防护规则）。
- **严格模式约束**：在防护等级 5 下已被数据平面当场拦截的样本，由于请求已物理终止，无法在事后逆向变更为放行状态。操作者仍可提交独立的人工研判决定（载荷、URI、IP 或指纹）来创建所选规则。

## 3. 自动化规则采纳（Auto-Agree 与 Fail-Closed） {#auto-agree}

当开启站点级 `sites[].waf.semantic_policy.auto_agree: true` 时，系统会将模型判定为高危（`high`）或严重（`critical`）的高置信度样本自动沉淀为该站点的自定义载荷规则。自动采纳本身不会创建全局 IP 黑名单或客户端软指纹封禁；这些仍需操作者单独明确执行。

{{% pageinfo color="warning" %}}
**安全闭环约束（Fail-Closed）**：任何未通过完整前置校验、未明确关联合法站点、或模型置信度未达到阈值的自动化规则建议，系统一律执行 **Fail-Closed** 安全丢弃，绝不在未经充分验证的情况下擅自向数据平面热注入未受控规则。
{{% /pageinfo %}}

## 4. AI 运维助手与工具审批流防篡改 {#assistant}

CheeseWAF 提供了基于大模型的智能交互助手（接口 `POST /api/ai/assistant`，支持 Server-Sent Events 流式响应）：

- **操作者与状态强绑定（Actor & Preview Binding）**：当助手生成修改网络监听、删除站点或重载规则等高风险工具调用时，必须通过 `/api/ai/tools/approvals` 提交人工审批确认。审批令牌由系统在内存中与当前经过身份认证的操作者（Actor）、工具预览指纹及状态进行不可篡改的加密绑定，从根源上杜绝审批回放与越权提权。
- **权限角色隔离**：
  - `use:ai`：仅允许发起分析与查询对话。
  - `write:ai`：允许修改 AI 配置并触发自学习任务。
  - `approve:ai`：具备批准高危工具调用的核心权限。

## 5. 定时自学习分析（Self-Learning） {#self-learning}

系统内置了自动化威胁自学习任务调度，配置参数如下：

```yaml
ai:
  self_learning:
    enabled: false
    auto_apply: false
    dry_run: true
    interval: 24h
    at: "03:30"
    min_confidence: 0.995
    min_events: 5
    max_events: 200
    max_rules_per_run: 3
    action: "block"
```

- **参数约束**：
  - `min_confidence`：自动沉淀规则的最低模型置信度阈值（默认 0.995）。
  - `min_events` / `max_events`：聚类分析所需的最少与最多关联攻击事件样本数。
  - `max_rules_per_run`：单次自学习运行允许生成的最大规则配额（默认 3 条），防止规则库膨胀。
  - `dry_run`：演练模式开关，开启时仅生成分析报告而不实际应用规则。
- **手动触发**：调用 `POST /api/ai/self-learning/run` 可立即触发一轮针对近期访问日志的深度关联聚类分析。
