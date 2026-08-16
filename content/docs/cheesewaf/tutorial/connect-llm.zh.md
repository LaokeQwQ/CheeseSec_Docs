---
title: 接入大语言模型
linkTitle: 接入大模型
weight: 30
description: 配置兼容 OpenAI 或 Anthropic 协议的大模型接口，为 ALAP 启用异步智能研判与威胁自学习能力。
---

CheeseWAF 的 ALAP（AI Large-Language-Model Auto Pilot）支持接入主流大语言模型服务，对边界可疑流量进行异步深度语义研判。

在 Web 管理控制台中进入 **AI 配置** 模块，填写以下参数：

| 配置项 | 配置键名 | 参数说明与示例 |
| --- | --- | --- |
| **启用 AI** | `ai.enabled` | ALAP 功能总开关（布尔值） |
| **模型提供方** | `ai.provider` | 支持 `openai` 或 `anthropic` |
| **接口地址** | `ai.base_url` | API Base URL（如 `https://api.openai.com/v1`） |
| **API 密钥** | `ai.api_key` | 对应模型服务商提供的访问密钥（API Key） |
| **模型名称** | `ai.model` | 调用的模型标识（如 `gpt-4o-mini`、`claude-3-5-sonnet-latest`） |
| **自动采纳** | `ai.auto_agree` | 开启后，模型判定的高危（`high`）与严重（`critical`）威胁将自动沉淀为防护规则 |

## 运行与安全建议 {#best-practices}

- **坚持异步模式**：确保配置中 `ai.async: true` 保持开启状态，严禁在同步实时转发路径中同步等待外部模型返回。
- **连通性校验**：保存配置前，建议点击控制台中的 **测试连接** 按钮，验证网络连通性与 API 密钥有效性。
- **渐进式启用自动采纳**：在接入初期建议保持 `ai.auto_agree: false`，在人工观察审查队列研判质量稳定后，再评估是否开启自动规则沉淀。

关于 ALAP 的工具调用权限、自动化研判流程及定时自学习机制，请参考 [ALAP 与审查队列](../../alap/)。
