---
title: ALAP Asynchronous Review & Self-Learning
linkTitle: ALAP
weight: 100
description: Asynchronous LLM threat review queue, automated rule adoption with fail-closed guarantees, AI assistant tool approvals, and self-learning analytics.
---

ALAP (AI Large-Language-Model Auto Pilot) serves as CheeseWAF's out-of-band analytical brain. By decoupling LLM semantic reasoning from real-time proxying, it introduces generalized intelligence without introducing latency into the forwarding data path.

Configured under the `ai` block, capabilities are managed across the **AI Settings** and **Threat Review** sections of the Web Console.

## 1. Asynchronous Queue & Concurrency Claims {#queue}

After response delivery completes, boundary samples and embedded attacks are pushed to the background review queue:

- **Protocol Adapters**: Background workers adapt prompts to OpenAI Chat Completions or Anthropic Messages protocols according to `ai.provider`.
- **Decoupled Guarantee**: `ai.async: true` ensures real-time traffic forwarding never blocks on third-party model inference.
- **Concurrency Decision Claims**: When multiple operators collaborate, the persistence layer uses atomic decision claims (`review_decisions` locks) to prevent race conditions and duplicate actions, while bounding queue retention.

## 2. Threat Triage & Operator Decisions {#decisions}

Security teams can audit and act upon threat findings via the console or REST API:

- **Queue Inspection**: Call `GET /api/review` to fetch flagged samples and model confidence scores.
- **Decision Submission**: Call `POST /api/review/{id}/decide` to mark samples as verified threats, false positives, or promote them to persistent protection rules.
- **Strict Invariance**: Payloads blocked under Paranoia Level 5 represent physically terminated connections and cannot be retroactively passed, but can be promoted to permanent global blocks.

## 3. Automated Rule Adoption & Fail-Closed Guardrails {#auto-agree}

When `ai.auto_agree: true` is enabled, the system automatically translates high-confidence malicious assessments (`high` or `critical`) into permanent IP denylists, client fingerprint bans, or custom rules.

{{% pageinfo color="warning" %}}
**Fail-Closed Invariance**: Proposed rules that fail syntax validation, lack clear site associations, or fall below confidence thresholds **fail closed**. The engine never injects unverified rules into the active data plane.
{{% /pageinfo %}}

## 4. AI Copilot Tool Approvals & Replay Protection {#assistant}

CheeseWAF includes a streaming AI copilot (`POST /api/ai/assistant` using Server-Sent Events):

- **Actor & Preview Binding**: When the assistant generates actions affecting network bindings, site definitions, or rule tables, it requires explicit approval via `/api/ai/tools/approvals`. Approval tokens are cryptographically bound to the authenticated operator (actor), the exact parameter preview fingerprint, and execution state, preventing replay attacks and privilege escalation.
- **RBAC Scope Separation**:
  - `use:ai`: Query and interactive chat dialogs.
  - `write:ai`: Modifying AI settings and triggering self-learning jobs.
  - `approve:ai`: Authorizing high-risk system-level tool executions.

## 5. Scheduled Self-Learning Analytics {#self-learning}

CheeseWAF includes automated periodic clustering of access logs and attack samples:

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

- **Configuration Properties**:
  - `min_confidence`: Minimum confidence score required to propose a rule (default 0.995).
  - `min_events` / `max_events`: Sample bounds for unsupervised clustering.
  - `max_rules_per_run`: Maximum rules synthesized per execution (default 3) to prevent rule bloat.
  - `dry_run`: Simulation mode; generates analytical reports without modifying active rules.
- **Manual Trigger**: Invoke `POST /api/ai/self-learning/run` to execute immediate cluster analysis over recent traffic.
