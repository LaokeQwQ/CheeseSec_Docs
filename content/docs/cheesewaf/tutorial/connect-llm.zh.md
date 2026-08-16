---
title: 接入大模型
linkTitle: 接入大模型
weight: 30
description: 把 ALAP 指到兼容 OpenAI 或 Anthropic 的接口。
---

第一天可以先不配 ALAP。
需要异步审查、并把结果写成规则时再打开。

在控制台打开 **AI**。

| 字段 | 含义 |
| --- | --- |
| 启用 | 总开关（`ai.enabled`） |
| 提供方 | `openai` 或 `anthropic` |
| 接口地址 | Chat Completions / Messages 的基地址，例如 `https://api.openai.com/v1` |
| API Key | 该接口的密钥 |
| 模型 | 模型名，例如 `gpt-4o-mini` |
| 自动采纳 | 打开后，`high` / `critical` 结论可以变成长期规则 |

示例配置里 `ai.enabled` 默认是 `false`。
`ai.async` 保持 `true`，数据平面就不会等模型。

先在控制台用 **测试连接**，再打开自动采纳。

见 [ALAP 与审查队列](../../alap/)。
