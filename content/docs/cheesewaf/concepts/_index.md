---
title: Core Concepts
linkTitle: Concepts
weight: 40
description: In-depth exploration of the request processing lifecycle, paranoia level evaluation, payload isolation mechanisms, and unified access control.
---

This section introduces the foundational architecture and evaluation mechanics of CheeseWAF. Prior to tuning production paranoia levels or configuring advanced security policies, reviewing these concepts is strongly recommended:

{{< nav-cards cols="2" >}}
{{< nav-card title="Request Processing Pipeline" link="/docs/cheesewaf/concepts/pipeline/" icon="fa-solid fa-route" desc="Trace the end-to-end request lifecycle across network filters, access control, AST semantic inspection, and asynchronous ALAP review." />}}
{{< nav-card title="Paranoia Level Mechanism" link="/docs/cheesewaf/concepts/paranoia/" icon="fa-solid fa-layer-group" desc="Detailed breakdown of paranoia levels 0 through 5, false-positive suppression strategies, and dynamic time-windowed auto-promotion." />}}
{{< nav-card title="Isolated vs. Embedded Payloads" link="/docs/cheesewaf/concepts/isolated-embedded/" icon="fa-solid fa-code" desc="Distinguish standalone attack payloads from benign context embedding, and understand targeted gadget isolation safeguards." />}}
{{< nav-card title="Unified Management Surfaces" link="/docs/cheesewaf/concepts/management/" icon="fa-solid fa-table-columns" desc="Understand the shared RBAC authorization model, session mechanics, and audit trail spanning the Web console, TUI, and REST API." />}}
{{< /nav-cards >}}
