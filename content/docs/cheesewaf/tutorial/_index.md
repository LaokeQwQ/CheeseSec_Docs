---
title: Quick Start Guide
linkTitle: Quick Start
weight: 30
description: Three steps to complete initial system setup, onboard your first reverse proxy site, and configure asynchronous LLM threat review.
---

Once the daemon is up and running, follow these three essential steps to establish comprehensive web protection:

{{< nav-cards cols="1" >}}
{{< nav-card title="1. System Initialization" link="/docs/cheesewaf/tutorial/setup/" icon="fa-solid fa-key" desc="Access the /setup wizard, create your initial administrator account, securely archive master keys, and verify management boundaries." />}}
{{< nav-card title="2. Onboard Your First Site" link="/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="Configure public domain names, backend upstream server addresses, and set the baseline paranoia level to Level 3 (Smart Protection)." />}}
{{< nav-card title="3. Connect LLM Threat Review" link="/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-robot" desc="Connect OpenAI- or Anthropic-compatible APIs to enable asynchronous ALAP threat reasoning and closed-loop rule synthesis." />}}
{{< /nav-cards >}}

{{% pageinfo color="info" %}}
CheeseWAF's Data Plane provides deterministic AST semantic protection immediately upon startup, even without an LLM connected. Before configuring the `ai` block, the ALAP review queue simply remains idle.
{{% /pageinfo %}}
