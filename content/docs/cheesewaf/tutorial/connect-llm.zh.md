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
| **接口地址** | `ai.api_base` | API Base URL（如 `https://api.openai.com/v1`） |
| **允许私网地址** | `ai.allow_private_api_base` | 是否允许指向内网/本地模型网关（如 Ollama、LocalAI，布尔值，默认 `false`） |
| **API 密钥** | `ai.api_key` | 对应模型服务商提供的访问密钥（API Key） |
| **模型名称** | `ai.model` | 调用的模型标识（如 `gpt-4o-mini`、`claude-3-5-sonnet-latest`） |
| **自动采纳** | `sites[].waf.semantic_policy.auto_agree` | 站点级配置：开启后，模型判定的高危与严重威胁将自动沉淀为该站点的防护规则 |

**旧配置迁移：** 当前版本不会读取旧的 `ai.base_url` 与 `ai.auto_agree`。请将 `ai.base_url` 手动迁移为 `ai.api_base`，并将审批开关分别迁移到各站点的 `sites[].waf.semantic_policy.auto_agree`；保存后按需 reload/restart 服务。

## 运行与安全建议 {#best-practices}

- **坚持异步模式**：确保配置中 `ai.async: true` 保持开启状态，严禁在同步实时转发路径中同步等待外部模型返回。
- **连通性校验**：保存配置前，建议点击控制台中的 **测试连接** 按钮，验证网络连通性与 API 密钥有效性。
- **渐进式启用自动采纳**：在接入初期建议保持 `sites[].waf.semantic_policy.auto_agree` 关闭，在人工观察审查队列研判质量稳定后，再评估是否开启自动规则沉淀。

关于 ALAP 的工具调用权限、自动化研判流程及定时自学习机制，请参考 [ALAP 与审查队列](../../alap/)。
