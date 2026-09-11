---
title: Onboard Your First Site
linkTitle: First Site
weight: 20
description: Configure public domain names, backend upstream origin servers, and baseline paranoia protection in CheeseWAF.
---

Log in to the Web console and navigate to **Sites** → **New Site** to configure your first reverse proxy service:

{{% steps %}}

### 1. Configure Public Domains {#domain}

Enter the public hostnames used by your clients (e.g., `app.example.com`). CheeseWAF matches incoming HTTP `Host` headers against the configured `sites[].domains` list.

### 2. Configure Backend Upstream Origins {#upstream}

Specify the origin server address and port (e.g., `10.0.0.10:8000`). When multiple upstreams are defined, the system distributes traffic according to the configured load balancing policy (`round_robin` by default).

### 3. Set Baseline Paranoia Level {#paranoia}

New sites default to paranoia level **3 (Smart Standard Mode)**; if the current wizard exposes this option, leave it at 3. In this mode, the system blocks high-confidence standalone payloads while allowing embedded features through to asynchronous ALAP review, ensuring business continuity while collecting threat data.

### 4. Save & Hot-Reload {#save}

Click **Save Site**. CheeseWAF dynamically reloads site definitions in memory without terminating the main daemon or interrupting active connections.

{{% /steps %}}

After saving, update your DNS records or local `hosts` file to point the domain to the CheeseWAF Data Plane listener (`http://127.0.0.1:8080` by default) to verify end-to-end reverse proxy forwarding.

For health checks, automatic SSL issuance, and path rewrite configurations, see [Sites & Reverse Proxy](../../sites/).
