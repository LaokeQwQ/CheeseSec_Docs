---
title: ALAP 异步审查与自学习机制
linkTitle: ALAP
weight: 100
description: 异步大模型威胁审查队列、自动化规则采纳、AI 助手工具调用审批与自学习分析。
---

ALAP（AI Large-Language-Model Auto Pilot）是 CheeseWAF 的智能旁路分析大脑。它通过与数据平面完全解耦的异步队列机制，将大语言模型的泛化语义理解能力引入威胁检测流程，同时保障核心转发链路的零延迟开销。

在 Web 管理控制台中对应 **AI 配置** 与 **威胁审查** 模块，底层配置块为 `ai`。

## 1. 异步审查队列架构 {#queue}

在数据平面向客户端完成响应交付后，命中特定防护策略的边界样本与夹杂特征请求会被推入后台异步审查队列：

- **模型适配层**：后台 Worker 会根据 `ai.provider` 适配 OpenAI Chat Completions 或 Anthropic Messages 协议格式发起外部推理请求。
- **异步安全原则**：始终保持配置中 `ai.async: true`，数据平面不产生任何针对模型返回的同步阻塞等待。

## 2. 威胁研判与处置流程 {#decisions}

安全运维人员可通过控制台或 REST API 审查分析结果：

- **查询待审队列**：调用 `GET /api/review` 获取待研判样本列表与模型评分。
- **人工决策提交**：调用 `POST /api/review/{id}/decide` 记录处置决定（确认为攻击、误报放行或沉淀为防护规则）。
- **严格模式约束**：在防护等级 5 下已被数据平面当场拦截的样本，由于请求已物理终止，无法在事后逆向变更为放行状态，但支持转换为长期的全局封禁规则。

## 3. 自动采纳机制（Auto-Agree） {#auto-agree}

当开启 `ai.auto_agree: true` 时，系统将自动将模型判定为高危（`high`）或严重（`critical`）的高置信度样本转为永久生效的 IP 黑名单、软指纹封禁或自定义特征规则。

{{% pageinfo color="tip" %}}
建议在生产初期先关闭自动采纳，通过人工观察审查队列 1～2 周，校准提示词与模型识别质量后再开启全自动规则闭环。
{{% /pageinfo %}}

## 4. AI 运维助手与工具审批流 {#assistant}

CheeseWAF 提供了基于大模型的智能交互助手（接口 `POST /api/ai/assistant`，支持 Server-Sent Events 流式响应）：

- **安全沙箱与审批流**：当助手需要执行修改网络监听、删除站点或重载规则等高风险动作时，必须通过 `/api/ai/tools/approvals` 提交人工审批确认。
- **权限角色隔离**：
  - `use:ai`：仅允许发起分析与查询对话。
  - `write:ai`：允许修改 AI 配置并触发自学习任务。
  - `approve:ai`：具备批准高危工具调用的核心权限。

## 5. 定时自学习分析 {#self-learning}

调用 `POST /api/ai/self-learning/run` 可触发一轮针对近期全量访问日志与拦截样本的深度关联聚类分析，自动识别新兴的攻击探测趋势与特征模式。该任务亦可通过内置调度器实现自动化定时周期运行，详见 [存储与调度管理](../storage/)。
