---
title: Paranoia Level Mechanism
linkTitle: Paranoia Levels
weight: 20
description: Understand paranoia levels 0 through 5, differential actions for isolated vs. embedded payloads, and dynamic time-windowed promotion.
---

CheeseWAF allows configuring the paranoia level independently for each reverse proxy site via `sites[].waf.paranoia_level`. Supported values range from **0 to 5**, with **3 (Standard Smart Protection)** recommended as the production baseline.

The paranoia level mechanism balances high threat detection rates with false-positive suppression. When inspecting decoded parameter values, the AST semantic engine executes tiered responses based on payload morphology (Isolated vs. Embedded).

{{% pageinfo color="info" %}}
**Two Independent Knobs**:
- `waf.paranoia_level` (0–5) drives the **AST semantic engine itself**—determining how strictly the engine identifies attack payload morphology (Isolated vs. Embedded features).
- Ingress proxy enforcement actions are driven by an entirely separate setting: `protection_policy.web_attack` (`off`, `low`, `smart`, `high`, `strict`, default `smart`). It dictates downstream action thresholds (severity and confidence cutoffs, aggregate risk scoring, and failure policies when the 100ms detection budget is exhausted). The two controls are completely decoupled.
{{% /pageinfo %}}

## Paranoia Levels Comparison {#levels}

| Level | Policy Profile | Isolated Payload | Embedded Payload | Auto-Promotion |
| :---: | --- | --- | --- | :---: |
| **0** | **Record Only** | Log alert & allow | Log alert & allow | No |
| **1** | **Observation Mode** | Log alert & allow | Log alert & allow | No |
| **2** | **Basic Defense** | **Block immediately** | **Allow**, enqueue for ALAP review | No |
| **3** | **Smart Standard (Recommended)** | **Block immediately** | **Allow**, enqueue for ALAP review | No |
| **4** | **Active Defense** | **Block immediately** | **Allow**, trigger auto-promotion & review | **Yes** (promotes to 5) |
| **5** | **Strict Defense** | **Block immediately** | **Block immediately**, enqueue for review | Already maximum |

## Dynamic Auto-Promotion Mechanism {#promote}

At **Paranoia Level 4**, when suspicious embedded payloads are detected within live traffic, the system proactively promotes the site to **Level 5 (Strict Mode)** for a configurable duration defined by `promote_seconds` (e.g., 300 seconds) to prevent reconnaissance-stage exploitation.

- **State Persistence**: The promotion deadline timestamp is stored in the embedded SQLite database, persisting across daemon restarts.
- **Automatic Decay**: Once the promotion window elapses without subsequent suspicious triggers, the site seamlessly reverts to its baseline Level 4 configuration.

## Level 5 Review Constraints {#level-5}

Samples blocked under Paranoia Level 5 are submitted to the ALAP review queue with a `blocked` status tag:

- **Non-Retroactive Release**: Because the connection was physically terminated, operators cannot mutate the sample status to "Allowed".
- **Rule Synthesis**: Upon review, confirmed threats can be exported into permanent global defense rules (including signature patterns, URL path filters, IP blacklists, or client soft-fingerprints).
