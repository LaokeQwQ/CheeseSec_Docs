---
title: Configuration reference
linkTitle: Config
weight: 170
description: Top-level keys in cheesewaf.yaml and where this manual explains each block.
---

First start writes `cheesewaf.yaml` into the data directory.
The template is [`configs/cheesewaf.yaml`](https://github.com/LaokeQwQ/CheeseWAF/blob/master/configs/cheesewaf.yaml) in the product repo.

| Key | Manual |
| --- | --- |
| `server` | [TLS](../tls/), [Intro](../intro/) |
| `tls` | [TLS](../tls/) |
| `setup` | [Initialize](../tutorial/setup/), [Storage](../storage/) |
| `deployment` / `cluster` | [Cluster](../cluster/) |
| `console` | [Bot and CAPTCHA](../protection/bot-captcha/), [Monitor](../monitor/) |
| `sites` | [Sites](../sites/) |
| `protection` | [Protection](../protection/) |
| `block_page` | [Block pages](../protection/block-page/) |
| `storage` | [Storage](../storage/) |
| `logging` | [Monitor](../monitor/) |
| `ai` | [ALAP](../alap/) |
| `update` | [Operations](../operations/) |
| `scheduler` | [Storage](../storage/) |
| `edge` | [Edge](../edge/) |
| `monitor` | [Monitor](../monitor/) |
| `apisec` | [API security](../api-security/) |

## Timeouts {#timeouts}

`server.read_timeout`, `write_timeout`, and `idle_timeout` apply to the HTTP servers.
`sites[].waf.performance.proxy_timeout` applies to the origin.

## Reload {#reload}

Saving a site or a protection policy in the console hot-reloads that slice.
A change to listen addresses still needs a process restart (`cheesewaf restart` or systemd).
