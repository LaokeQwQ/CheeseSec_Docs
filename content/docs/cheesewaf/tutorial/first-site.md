---
title: Add the first site
linkTitle: First site
weight: 20
description: Point CheeseWAF at a domain and an upstream, then pick paranoia level 3.
---

In the console open **Sites** → **New site**.

{{% steps %}}

### Domain {#domain}

Enter the hostname clients already use, for example `app.example.com`.
CheeseWAF matches `sites[].domains`.

### Upstream {#upstream}

Enter the origin address, for example `10.0.0.10:8000`.
More than one upstream uses the site `loadbalance` policy (`round_robin` by default).

### Paranoia {#paranoia}

Use level **3** for a first production site.
Level 3 blocks isolated attack values and allows embedded hits for later ALAP review.

### Save {#save}

Save the site.
The process reloads the site list without a full restart.

{{% /steps %}}

Point DNS or the local hosts file at the CheeseWAF data-plane address.
Confirm the origin still answers through CheeseWAF before you raise the level.

Details: [Sites and reverse proxy](../../sites/).
