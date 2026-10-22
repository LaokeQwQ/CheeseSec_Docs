---
title: CheeseSec Documentation
linkTitle: Home
description: Official product manuals and engineering guides for CheeseSec security solutions, covering deployment, configuration, and operations.
cascade:
  type: docs
no_list: true
---

Welcome to the official CheeseSec product documentation. This site provides architectural overviews, deployment guides, security policy configurations, and operational manuals for CheeseSec security components and services.

The site covers two independent products: **CheeseWAF** and **CheeseSec Plugins**. The plugin product serves the whole CheeseSec ecosystem; compatible hosts and versions are declared by each plugin.

CheeseWAF source code and pre-built binaries are hosted in the [CheeseWAF repository](https://github.com/LaokeQwQ/CheeseWAF) under the [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE).

## Products {#cheesewaf}

{{< nav-cards cols="2" >}}
{{< nav-card title="CheeseWAF" link="/docs/cheesewaf/" iconImage="/images/cheesewaf-logo.png" desc="Commercial-grade self-hosted Web Application Firewall featuring AST semantic analysis, bot mitigation, API security, and asynchronous LLM-driven threat review." />}}
{{< nav-card title="CheeseSec Plugins" link="/docs/plugins/" iconImage="/images/plugins-logo.svg" desc="An independent plugin product for the CheeseSec ecosystem. Develop, publish, and verify extensions for compatible hosts." />}}
{{< /nav-cards >}}

## Quick Navigation {#start}

| Scenario | Recommended Documentation |
| --- | --- |
| Deployment & Initial Setup | [System Installation](/docs/cheesewaf/install/) · [Quick Start](/docs/cheesewaf/tutorial/) |
| Core Architecture & Pipeline | [Architecture & Overview](/docs/cheesewaf/intro/) · [Core Concepts](/docs/cheesewaf/concepts/) |
| Site Configuration & Protection | [Sites & Reverse Proxy](/docs/cheesewaf/sites/) · [Protection Policies](/docs/cheesewaf/protection/) |
| API & Configuration Reference | [RESTful API Reference](/docs/cheesewaf/api/) · [Configuration Reference](/docs/cheesewaf/config/) |
| Plugin Development & Publication | [Plugin handbook](/docs/plugins/) · [Plugin store](https://store.cheesesec.com/) |
