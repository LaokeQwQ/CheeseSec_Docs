---
title: Quick Start Guide
linkTitle: Quick Start
weight: 30
description: Three steps to complete initial system setup, onboard your first reverse proxy site, and configure asynchronous LLM threat review.
---

Start with the one-line Linux installer. It asks for a language, downloads and verifies the latest stable release, creates a public HTTPS management entry, and prints a short-lived setup URL. Then follow these three steps:

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | sudo bash
```

{{< nav-cards cols="1" >}}
{{< nav-card title="1. System Initialization" link="/docs/cheesewaf/tutorial/setup/" icon="fa-solid fa-key" desc="Access the /setup wizard, create your initial administrator account, securely archive master keys, and verify management boundaries." />}}
{{< nav-card title="2. Onboard Your First Site" link="/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="Configure public domain names, backend upstream server addresses, and set the baseline paranoia level to Level 3 (Smart Protection)." />}}
{{< nav-card title="3. Connect LLM Threat Review" link="/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-robot" desc="Connect OpenAI- or Anthropic-compatible APIs to enable asynchronous ALAP threat reasoning and closed-loop rule synthesis." />}}
{{< /nav-cards >}}

{{% pageinfo color="info" %}}
Keep the complete HTTPS setup URL private. Its URL fragment contains a one-time token that the browser converts to the `X-CheeseWAF-Setup-Token` header; it is revoked after setup. If the server cannot reach GitHub, use the signed archive and checksum files from the [release page](https://github.com/LaokeQwQ/CheeseWAF/releases) and follow the offline installation section.

CheeseWAF's Data Plane provides deterministic AST semantic protection immediately after startup, even without an LLM connected. Before configuring the `ai` block, the ALAP review queue simply remains idle.
{{% /pageinfo %}}
