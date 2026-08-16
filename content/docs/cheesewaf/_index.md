---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: Self-hosted Web Application Firewall. Install, configure, and operate it.
---

CheeseWAF is a self-hosted Web Application Firewall.
It ships as one Go binary with an embedded SQLite store, a Web console, a CLI / TUI, and a REST management API.

The data plane inspects requests, then proxies them upstream.
It does not call a large language model on every request.
After the response is sent, an optional ALAP queue can review suspicious samples.

{{% pageinfo color="info" %}}
Download packaged builds from [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases).
The project is licensed under [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE).
{{% /pageinfo %}}

## How it works {#how-it-works}

1. **Data plane.** Parameters are decoded, then parsed. Deterministic SQL injection, XSS, and command execution can be blocked immediately.
2. **ALAP.** After the response is sent, ambiguous or embedded samples go to a background queue. Any OpenAI-compatible model can review them.
3. **Review results.** Findings marked `high` or `critical` can become lasting IP, fingerprint, or signature rules when auto-agree is on.

ALAP stands for **AI Large-Language-Model Auto Pilot**.

## Default listeners {#default-listeners}

| Plane | Default address | Role |
| --- | --- | --- |
| Data plane | `http://127.0.0.1:8080` | Receive site traffic, inspect, proxy upstream |
| Management plane | `http://127.0.0.1:9443` | Web console, REST API, setup wizard. Docker defaults to HTTPS |
| Cluster plane | `http://127.0.0.1:9444` | Node sync in cluster mode |
| Local controller | `http://127.0.0.1:17943` | Windows / macOS desktop controller only |

## Start here {#start-here}

{{< nav-cards cols="2" >}}
{{< nav-card title="Install" link="/docs/cheesewaf/install/" icon="fa-solid fa-download" desc="Linux, Docker, Windows, and macOS." />}}
{{< nav-card title="Quick start" link="/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="Initialize, add a site, connect a model." />}}
{{< nav-card title="Concepts" link="/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="Pipeline, paranoia levels, isolated vs embedded." />}}
{{< nav-card title="Protection" link="/docs/cheesewaf/protection/" icon="fa-solid fa-shield" desc="Semantic engine, IP, bot, rate limit, ACL." />}}
{{< /nav-cards >}}
