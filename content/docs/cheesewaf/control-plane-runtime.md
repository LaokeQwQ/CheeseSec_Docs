---
title: Standalone Control Runtime
linkTitle: Control Runtime
weight: 140
description: Command-line boundary, startup checks, local status endpoints, and current limits of the standalone cheesewaf-control process.
---

The repository includes `cheesewaf-control`, a separate control-plane process. It opens the control-plane PostgreSQL adapter and the native-raft runtime, then exposes a local status server. It does not handle WAF requests, host the Web Console, or replace the main `cheesewaf serve` process.

{{% pageinfo color="warning" %}}
This page describes the current source and runtime contract. It is not a deployment recipe for high availability. The main `cheesewaf serve` path still uses `storage.profile: temporary` with embedded SQLite and still rejects the production management profile with `ErrProductionStorageUnavailable`. The standalone process does not provide empty-cluster initialization, a remote join workflow, plugin installation, OTA, or CWEDP execution.
{{% /pageinfo %}}

## Command boundary {#command}

The process accepts flags only. Positional arguments are rejected.

```
cheesewaf-control --help
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
| `--profile` | `production` | Only the `production` profile is accepted. |
| `--cluster-id` | empty | Required. The value must not contain whitespace, control characters, or invisible format characters. |
| `--node-id` | generated | Optional. When omitted, native-raft generates and persists the node identity under `--data-dir`. |
| `--data-dir` | empty | Required. Use a persistent, private directory for native-raft state and snapshots. |
| `--listen` | `127.0.0.1:9450` | Local management HTTP address. It must be a loopback `host:port`. |
| `--raft-listen` | `127.0.0.1:9451` | Native-raft address. It must be a different loopback `host:port`. |
| `--mode` | `join` | Must be `bootstrap` or `join`; the default does not initialize a cluster. |
| `--ca-file` | empty | Required PEM CA bundle for the control-plane and native-raft TLS trust. Use a private, readable file. |
| `--cert-file` | empty | Required node certificate PEM. Its identity must match the configured node identity when one is supplied. |
| `--key-file` | empty | Required private key PEM. Keep it owner-readable (`0600`) and out of logs and source control. |
| `--postgres-dsn` | empty | Required management PostgreSQL DSN. It is never placed in status JSON. |
| `--timeout` | `15s` | Positive startup timeout. Expiration stops startup. |

Both listeners are validated as loopback addresses. The current command does not expose a remote management listener. A remote deployment would need a separate design with TLS, mTLS, ACLs, audit, and rollback controls.

The `--postgres-dsn` value is an independent management-state connection. It is not `storage.postgresql.dsn`, which remains the optional asynchronous access-log sink used by `cheesewaf`. Loopback and Unix-socket PostgreSQL connections are allowed; a remote PostgreSQL host must use certificate-verified TLS. Redis is not opened by this process.

The CA, node certificate, and private key must be created and installed by a protected provisioning process before this command is started. The example remains fail-closed until PostgreSQL, Raft TLS, and matching durable snapshots are available; it is not a successful HA bootstrap recipe.

## Startup and fail-closed behavior {#startup}

`cheesewaf-control` does not bind the HTTP listener until the full production bootstrap succeeds:

1. Open the management PostgreSQL adapter.
2. Prepare and health-check PostgreSQL, including the control-plane schema migration.
3. Load the PostgreSQL control-state snapshot.
4. Open, prepare, and health-check native-raft.
5. Load the native-raft snapshot.
6. Compare both snapshots, including cluster, leader, term, epoch, revision, desired version, digest, payload, frozen state, and nonce ledger.
7. Validate the snapshot and confirm it does not regress the local last-known-good state.
8. Establish a fencing token bound to the same cluster, leader, epoch, revision, digest, and nonce.
9. Read native-raft again. A leader, term, epoch, revision, or digest change after fencing fails startup.
10. Install the equal snapshot, resume control-plane writes, and report `ready`.

Any failed migration, health check, snapshot comparison, validation, or fencing step returns an error. The command reports `control-plane startup failed closed` and exits without starting the status server. No unverified snapshot becomes ready, and no proposal is accepted. Supervisors that deliberately use the runtime's frozen diagnostic mode may expose liveness and the freeze reason, but that mode never claims readiness or enables writes.

An empty PostgreSQL row and an empty native-raft state are treated as an empty, frozen state. Readiness still requires a committed desired-state revision, a non-zero term and epoch, an established leader, and a matching fencing nonce. Therefore `--mode bootstrap` alone cannot initialize an empty production cluster or invent its first desired state.

## Local status endpoints {#endpoints}

The status server is intended for local supervisors and probes. It listens on `--listen`, which is loopback-only by validation.

| Method | Path | Response |
| --- | --- | --- |
| `GET` | `/healthz` | Always `200` with the current status document. A frozen process can still report liveness when a supervisor deliberately exposes frozen diagnostics. |
| `GET` | `/readyz` | `200` only when both `ready` and `write_ready` are true; otherwise `503`. |
| `GET` | `/status` | `200` with phase, readiness, cluster/node identity, leader, term, epoch, revision, update time, and a bounded freeze reason. |
| `POST` | `/proposals` | `503` before write readiness. When write-ready, the current binary returns `501` because proposal transport is not mounted. Other methods return `405`. |

Status responses do not include credentials, PostgreSQL DSNs, filesystem paths, or raw backend errors. The endpoint is a local diagnostic surface, not a cluster API.

## Bootstrap and join modes {#modes}

`bootstrap` and `join` are native-raft startup modes, not complete cluster administration workflows.

- `bootstrap` calls native-raft's one-time `BootstrapCluster` operation only when the data directory has no existing Raft state. It still needs matching PostgreSQL and native-raft snapshots and a valid committed fence before the process can become ready.
- `join` never calls `BootstrapCluster`. A fresh join node does not become leader and cannot turn an empty state into a cluster. The current CLI has no controller address, join token, or remote enrollment flag.
- The native-raft package exposes a leader-side `Join` operation that adds a voter. That operation is an internal runtime API, not an HTTP endpoint or a `cheesewaf-control` subcommand. Treat `join` as a read-only registration mode until a complete, tested follower enrollment path is published.

The current standalone command therefore cannot be used to create an empty cluster, automatically add a peer, or claim production multi-node HA. Native-raft and PostgreSQL code in the repository define the consistency boundary; they do not make the existing `cheesewaf serve` storage path switch to PostgreSQL or native-raft.

## Relationship to the main server {#serve}

`cheesewaf serve` remains the main WAF entry point. It owns the data-plane listener and the existing management plane, and its current runnable management profile is `storage.profile: temporary`. Adding a PostgreSQL management DSN or selecting `storage.profile: production` in the main server does not migrate it to this process; the main server continues to fail closed until its complete PostgreSQL, coordinator, native-raft, approval, audit, and data-plane integration is delivered and accepted.

For the broader target architecture, see [Commercial Platform Architecture](../commercial-architecture/). This page is the executable boundary for the separate command and should be read together with the repository's control-plane startup contract.
