---
title: Connect Large Language Models
linkTitle: Connect Models
weight: 30
description: Configure OpenAI- or Anthropic-compatible API endpoints for ALAP asynchronous threat reasoning and self-learning rules.
---

CheeseWAF's ALAP (AI Large-Language-Model Auto Pilot) engine integrates with industry-standard LLM APIs to perform out-of-band semantic reasoning on suspicious and borderline traffic.

In the Web management console, navigate to the **AI** section and configure the following parameters:

| Setting | Configuration Key | Description & Examples |
| --- | --- | --- |
| **Enable AI** | `ai.enabled` | Master toggle for ALAP functionality (boolean) |
| **Provider** | `ai.provider` | API protocol dialect: `openai` or `anthropic` |
| **Base URL** | `ai.base_url` | API Base URL (e.g., `https://api.openai.com/v1`) |
| **API Key** | `ai.api_key` | Secret access token / API key provided by your LLM vendor |
| **Model Name** | `ai.model` | Model identifier (e.g., `gpt-4o-mini`, `claude-3-5-sonnet-latest`) |
| **Auto-Agreement** | `ai.auto_agree` | When enabled, threats evaluated as `high` or `critical` are automatically persisted as defensive rules |

## Best Practices & Security Guidelines {#best-practices}

- **Enforce Asynchronous Execution**: Always maintain `ai.async: true` in your configuration to guarantee that the Data Plane never blocks real-time traffic while waiting for model inference.
- **Connection Testing**: Before enabling rules, click **Test Connection** in the console to validate network routing, DNS resolution, and credential authentication.
- **Gradual Rollout of Auto-Agreement**: Keep `ai.auto_agree: false` during initial deployment. Review samples manually in the threat queue for 1–2 weeks to verify evaluation fidelity before enabling automated rule generation.

For details on assistant tool approvals, review queues, and automated self-learning, see [ALAP & Review Queue](../../alap/).
