---
title: Standalone Control Runtime
linkTitle: Control Runtime
weight: 140
description: Public command parameters, local status endpoints, and current limits of the standalone cheesewaf-control process.
---

`cheesewaf-control` is a separate command with a local status service. It does not inspect WAF traffic, host the Web Console, or replace `cheesewaf serve`.

{{% pageinfo color="warning" %}}
This command does not provide a complete high-availability deployment, empty-cluster initialization, remote node enrollment, plugin installation, or OTA updates. The main WAF service continues to use its own configuration and supported storage profile.
{{% /pageinfo %}}

## Command parameters {#command}

The process accepts flags only. Positional arguments are rejected. Use `cheesewaf-control --help` to inspect the parameters supported by your installed version.

```text
cheesewaf-control \
  --profile production \
  --cluster-id cluster-a \
  --node-id node-a \
  --data-dir /var/lib/cheesewaf/control \
  --listen 127.0.0.1:9450 \
  --raft-listen 127.0.0.1:9451 \
  --mode join \
  --ca-file /etc/cheesewaf/control/ca.pem \
  --cert-file /etc/cheesewaf/control/node.pem \
  --key-file /etc/cheesewaf/control/node-key.pem \
  --postgres-dsn '<provided-by-a-protected-secret-source>' \
  --timeout 15s
```

| Flag | Default | Rule |
| --- | --- | --- |
| `--profile` | `production` | Only `production` is accepted. |
| `--cluster-id` | empty | Required; whitespace, control characters, and invisible format characters are rejected. |
| `--node-id` | generated | Optional node identity, persisted under `--data-dir` when generated. |
| `--data-dir` | empty | Required persistent directory with restricted permissions. |
| `--listen` | `127.0.0.1:9450` | Local HTTP address; must be a loopback `host:port`. |
| `--raft-listen` | `127.0.0.1:9451` | Consensus listener; must be a different loopback `host:port`. |
| `--mode` | `join` | Must be `bootstrap` or `join`; the default does not initialize a cluster. |
| `--ca-file` | empty | Required PEM CA bundle in a protected regular file. |
| `--cert-file` | empty | Required node certificate PEM; its identity must match an explicitly configured node identity. |
| `--key-file` | empty | Required private key PEM; keep it owner-readable (`0600`) and out of logs and source control. |
| `--postgres-dsn` | empty | Required management database connection; never included in status JSON. |
| `--timeout` | `15s` | Positive startup timeout. Expiration stops startup. |

Both listeners are restricted to loopback. A remote database connection requires certificate-verified TLS. The management database connection is separate from the optional `storage.postgresql.dsn` access-log sink used by the main WAF service.

The paths and identities above are examples. Prepare valid credentials and the required service state before running the command; the example alone does not create a working HA deployment.

## Startup status {#startup}

The command validates its configuration and required dependencies before reporting readiness. A startup failure prints `control-plane startup failed closed` and exits. Stop and correct the reported configuration or dependency problem before trying again. A running process or a successful liveness response alone does not mean it is ready to accept writes.

## Local status endpoints {#endpoints}

The status service is for local supervisors and probes on `--listen`.

| Method | Path | Response |
| --- | --- | --- |
| `GET` | `/healthz` | `200` with the current status document; liveness does not imply readiness. |
| `GET` | `/readyz` | `200` only when ready for writes; otherwise `503`. |
| `GET` | `/status` | `200` with bounded status and readiness information. |
| `POST` | `/proposals` | `503` before readiness; the current command returns `501` when ready because this operation is unavailable. Other methods return `405`. |

Status responses exclude credentials, database connection strings, and private filesystem paths. These endpoints are not a remote cluster-management API.

## Startup modes {#modes}

`bootstrap` and `join` select startup modes. Neither mode provides a complete cluster-administration workflow. The command cannot initialize an empty production cluster or enroll remote peers, and it has no controller-address or join-token flag. Do not use these modes as evidence that production multi-node HA is available.

## Main WAF service {#serve}

Continue to run `cheesewaf serve` for WAF traffic and the Web Console. Starting `cheesewaf-control` does not migrate the main service's storage or change its supported features. See [Cluster](../cluster/) for the main service's public configuration and current limits.
