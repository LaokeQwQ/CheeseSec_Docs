---
title: Connect a model
linkTitle: Connect a model
weight: 30
description: Point ALAP at an OpenAI-compatible or Anthropic-compatible endpoint.
---

ALAP is optional for a first day.
Turn it on when you want asynchronous review and lasting rules.

In the console open **AI**.

| Field | Meaning |
| --- | --- |
| Enabled | Master switch (`ai.enabled`) |
| Provider | `openai` or `anthropic` |
| Endpoint | Chat Completions / Messages base URL, for example `https://api.openai.com/v1` |
| API key | Secret for that endpoint |
| Model | Model name, for example `gpt-4o-mini` |
| Auto-agree | When on, `high` / `critical` findings can become lasting rules |

The sample config starts with `ai.enabled: false`.
`ai.async` stays `true` so the data plane never waits on the model.

Use **Test connection** in the console before you trust auto-agree.

See [ALAP and the review queue](../../alap/).
