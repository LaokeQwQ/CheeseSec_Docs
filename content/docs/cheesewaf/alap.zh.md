---
title: ALAP 与审查队列
linkTitle: ALAP
weight: 100
description: 异步模型审查、自动采纳、助手、工具审批和自学习。
---

控制台：**AI** 和 **审查**。
配置：`ai`。
REST：`/api/ai/*` 和 `/api/review/*`。

## 队列 {#queue}

响应返回之后，CheeseWAF 可以把样本送进模型队列。
worker 按 `ai.provider` 走 Chat Completions 或 Messages。

保持 `ai.async: true`。
数据平面不能等这条路径。

## 研判 {#decisions}

`GET /api/review` 列出条目。
`POST /api/review/{id}/decide` 记录放行、拒绝，或把结果写成规则。

防护等级 5 下被阻断的条目，不能改成放行。
仍可以写成长期规则。

## 自动采纳 {#auto-agree}

打开自动采纳后，`high` 和 `critical` 结论可以在无人点击时变成 IP、指纹或特征规则。
先把自动采纳 **关掉**，审查一周队列后再考虑打开。

## 助手和工具 {#assistant}

`POST /api/ai/assistant`（以及流式接口）可以带工具改配置。
危险工具走 `/api/ai/tools/approvals`。
角色：

- `use:ai`：分析
- `write:ai`：改 AI 配置、跑自学习
- `approve:ai`：批准待执行的工具调用

## 自学习 {#self-learning}

`POST /api/ai/self-learning/run` 会对近期样本跑一轮类似定时任务的处理。
调度器也可以按时间跑。见 [存储与调度](../storage/)。
