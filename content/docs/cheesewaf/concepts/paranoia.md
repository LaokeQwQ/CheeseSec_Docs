---
title: Paranoia levels
linkTitle: Paranoia levels
weight: 20
description: Per-site levels 0–5. Default is 3. Level 4 can rise to 5 for a timed window.
---

Set `sites[].waf.paranoia_level` per site.
Legal values are **0–5**.
The default is **3**.

The engine looks at **one decoded parameter value** at a time.
Path and parameter names stay visible.

| Level | Name | Isolated | Embedded | Timed rise |
| :---: | --- | --- | --- | :---: |
| **0** | Record only | Log, allow | Log, allow | No |
| **1** | Low monitor | Log, allow | Log, allow | No |
| **2** | Low-medium | **Block** | **Allow**, review later | No |
| **3** | Standard | **Block** | **Allow**, review later | No |
| **4** | Medium-high | **Block** | **Allow**, review later | **Yes** (rise to 5) |
| **5** | Strict | **Block** | **Block**, then review | Already max |

## Temporary rise {#promote}

At level 4, an embedded hit can raise the site to level 5 for `promote_seconds` (for example 300 seconds).
The deadline is stored in SQLite.
A process restart does not clear it.

## Level 5 review {#level-5}

A sample blocked at level 5 still enters the review queue with a `blocked` mark.
You cannot flip it to allow.
You can save a lasting deny rule (feature, URL, IP, or fingerprint).
