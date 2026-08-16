---
title: ALAP Asynchronous Review & Self-Learning
linkTitle: ALAP
weight: 100
description: Asynchronous LLM threat review queue, automated rule synthesis, AI assistant tool approvals, and self-learning analysis.
---

ALAP (AI Large-Language-Model Auto Pilot) serves as CheeseWAF's intelligent reasoning engine. Through an asynchronous queue decoupled entirely from the Data Plane, ALAP leverages the generalized semantic understanding of LLMs for threat analysis without adding any latency to the critical forwarding path.

Manage ALAP in the Web console under **AI** and **Review**, or configure parameters under the `ai` configuration block.

## 1. Asynchronous Review Architecture {#queue}

After the Data Plane completes response delivery to the client, borderline samples and embedded feature requests matching specific criteria are pushed to the background review queue:

- **Model Protocol Adapters**: Background workers query external LLMs formatted according to `ai.provider` (supporting OpenAI Chat Completions or Anthropic Messages protocols).
- **Asynchronous Principle**: Always maintain `ai.async: true` to ensure the Data Plane never blocks real-time traffic while waiting for external model inference.

## 2. Threat Review & Operator Decision Workflow {#decisions}

Security operators can audit analysis findings via the console or REST API:

- **Query Pending Queue**: Call `GET /api/review` to retrieve unreviewed samples and model confidence ratings.
- **Submit Decisions**: Call `POST /api/review/{id}/decide` to record decisions (confirm threat, dismiss false positive, or synthesize defense rules).
- **Strict Mode Constraints**: Under Paranoia Level 5, requests blocked inline by the Data Plane cannot be retroactively marked as allowed, but can be converted into long-term global defense rules.

## 3. Automated Rule Agreement (Auto-Agree) {#auto-agree}

When `ai.auto_agree: true` is active, high-confidence samples evaluated as `high` or `critical` threats are automatically persisted as permanent IP blacklists, client soft-fingerprints, or custom signature rules without requiring manual approval.

{{% pageinfo color="tip" %}}
During initial deployment, keep auto-agreement disabled. Audit the review queue manually for 1–2 weeks to calibrate prompts and verify model evaluation quality before enabling full closed-loop automation.
{{% /pageinfo %}}

## 4. AI Operations Assistant & Tool Approval Workflow {#assistant}

CheeseWAF provides an interactive LLM-powered operations assistant (invoked via `POST /api/ai/assistant`, with Server-Sent Events streaming support):

- **Approval Sandbox**: High-risk tool calls—such as mutating listeners, deleting sites, or reloading rules—must be submitted to `/api/ai/tools/approvals` for explicit human confirmation.
- **Granular RBAC Roles**:
  - `use:ai`: Allows initiating conversational queries and threat analysis.
  - `write:ai`: Permits modifying AI configuration and executing self-learning jobs.
  - `approve:ai`: Authorized to approve pending high-risk tool executions.

## 5. Automated Threat Self-Learning {#self-learning}

Invoke `POST /api/ai/self-learning/run` to trigger a cluster analysis pass across recent access logs and blocked payloads, automatically identifying emerging attack patterns and probing trends. This task can also be scheduled periodically via the built-in task scheduler. See [Storage & Task Scheduling](../storage/).
