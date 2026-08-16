---
title: How CheeseWAF works
linkTitle: Introduction
weight: 10
description: Data plane vs ALAP, why requests are not sent to a model in line, and what ships in one binary.
---

Traditional regex WAFs keep large signature libraries.
They are expensive to maintain and easy to evade with encoding or wrapping.

Calling a large language model on every request adds network latency you cannot hide.

CheeseWAF splits the work.

## Two planes {#two-planes}

### Data plane {#data-plane}

The process that accepts HTTP, HTTPS, or HTTP/3 does this in order:

1. IP, GeoIP, and client soft-fingerprint checks
2. Bot challenge, rate limit, and waiting room
3. Semantic analysis of decoded parameter values
4. Reverse proxy to the configured upstream

This path must stay fast.
It never waits on a remote model.

### Control plane {#control-plane}

The management listener hosts:

- the setup wizard at `/setup`
- the Web console
- the REST API under `/api`
- optional Prometheus metrics

Keep `server.admin_public` false unless you also enable TLS and restrict who can reach the port.

### ALAP {#alap}

After the client already has a response, CheeseWAF can enqueue:

- isolated hits that were blocked at paranoia 5
- embedded hits that were allowed at levels 2–4
- other borderline samples the engine marks for review

A worker calls the configured model.
The operator (or auto-agree) then saves a lasting rule or dismisses the sample.

See [ALAP and the review queue](../alap/).

## What ships together {#what-ships}

| Piece | Role |
| --- | --- |
| `cheesewaf` | Forwarding process. Default command is `serve` |
| `waf-cli` | Same binary or a symlink. Default command is the TUI panel |
| `cheesewaf-gui` | Loopback-only desktop controller on Windows and macOS |
| Web console | React UI served from the management plane |
| SQLite | Default store, CGO-free (`modernc.org/sqlite`) |

You do not need Redis, Nginx, or an external database to start.

## Related pages {#related}

- [Request pipeline](../concepts/pipeline/)
- [Paranoia levels](../concepts/paranoia/)
- [Install](../install/)
