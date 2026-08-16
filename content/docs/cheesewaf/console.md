---
title: Web console
linkTitle: Console
weight: 140
description: Pages in the management UI and how they map to this manual.
---

After [setup](../tutorial/setup/), open the management URL (default `http://127.0.0.1:9443/`).

The console is a React app served by the same process.
It uses session cookies plus CSRF.
Login can require a [login CAPTCHA](../protection/bot-captcha/#login).

## Page map {#pages}

| Console route | This manual |
| --- | --- |
| `/` Dashboard | [Monitor](../monitor/) |
| `/sites` | [Sites](../sites/) |
| `/ssl` | [TLS](../tls/) |
| `/rules` | [Custom rules](../protection/custom-rules/) |
| `/review` | [ALAP](../alap/) |
| `/logs` | [Monitor](../monitor/) |
| `/ip` | [IP and geo](../protection/ip-geo-fingerprint/) |
| `/protection` | [Protection](../protection/) |
| `/bot-challenge` | [Bot and CAPTCHA](../protection/bot-captcha/) |
| `/edge` | [Edge](../edge/) |
| `/ai` | [ALAP](../alap/) |
| `/monitor` | [Monitor](../monitor/) |
| `/apisec` | [API security](../api-security/) |
| `/users` | [Operations](../operations/) |
| `/ops` | [Storage](../storage/) |
| `/updates` | [Operations](../operations/) |
| `/block-pages` | [Block pages](../protection/block-page/) |
| `/attack-map` | [Monitor](../monitor/) |
| `/cluster` | [Cluster](../cluster/) |
| `/system` | [Operations](../operations/) |
| `/captcha-lab` | [Bot and CAPTCHA](../protection/bot-captcha/) |

Themes (light, dark, and several color packs) are local to the browser.
They do not change the data plane.
