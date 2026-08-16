---
title: Quick start
linkTitle: Quick start
weight: 30
description: Initialize CheeseWAF, add the first site, and connect a model for ALAP.
---

Do these three steps after the process is running.

{{< nav-cards cols="1" >}}
{{< nav-card title="1. Initialize" link="/docs/cheesewaf/tutorial/setup/" icon="fa-solid fa-key" desc="Open /setup, create the first admin, store the generated secrets." />}}
{{< nav-card title="2. Add a site" link="/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="Domain, upstream, paranoia level 3." />}}
{{< nav-card title="3. Connect a model" link="/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-robot" desc="OpenAI-compatible endpoint for ALAP. Optional at first." />}}
{{< /nav-cards >}}

The data plane works without a model.
ALAP review stays empty until you configure `ai`.
