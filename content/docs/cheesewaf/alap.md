---
title: ALAP and the review queue
linkTitle: ALAP
weight: 100
description: Asynchronous model review, auto-agree, the assistant, tool approvals, and self-learning.
---

Console: **AI** and **Review**.
Config: `ai`.
REST: `/api/ai/*` and `/api/review/*`.

## Queue {#queue}

After the response, CheeseWAF can enqueue samples for the model.
The worker uses Chat Completions or Messages, depending on `ai.provider`.

Keep `ai.async: true`.
The data plane must not wait on this path.

## Decisions {#decisions}

`GET /api/review` lists items.
`POST /api/review/{id}/decide` records allow, deny, or save as a rule.

At paranoia 5, a blocked item cannot be flipped to allow.
You can still save a lasting rule.

## Auto-agree {#auto-agree}

When auto-agree is on, `high` and `critical` findings can become IP, fingerprint, or signature rules without a human click.
Start with auto-agree **off** until you have reviewed a week of queue items.

## Assistant and tools {#assistant}

`POST /api/ai/assistant` (and the stream variant) chats with tools that can change config.
Dangerous tools go through `/api/ai/tools/approvals`.
Roles:

- `use:ai` — analyze
- `write:ai` — change AI config, run self-learning
- `approve:ai` — approve a pending tool call

## Self-learning {#self-learning}

`POST /api/ai/self-learning/run` starts a scheduled-style pass over recent samples.
The scheduler can also run this on a timer. See [Storage and scheduler](../storage/).
