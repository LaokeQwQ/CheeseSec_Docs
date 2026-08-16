---
title: Cluster
linkTitle: Cluster
weight: 120
description: Join tokens, mTLS interconnect, builtin consensus, rolling upgrade, and traffic peers.
---

Console: **Cluster**.
Config: `cluster`.
CLI: `cheesewaf cluster`.
REST: `/api/cluster/*`.

The sample is a single node:

```yaml
deployment:
  mode: "standalone"
cluster:
  enabled: false
  ha_mode: "single-node"
  interconnect:
    listen: "127.0.0.1:9444"
    mtls_required: true
```

## Turn clustering on {#enable}

1. Set `cluster.enabled: true` and pick a `cluster_id`.
2. Give every node a unique `node_id`.
3. Point `interconnect.advertise_addr` at an address other nodes can reach.
4. Keep `mtls_required: true`. Fill `ca_file`, `cert_file`, `key_file`.

`cluster.protection.freeze_writes_without_majority` stops config writes without a majority.
`allow_traffic_in_protection_mode` decides whether the data plane still forwards during that freeze.

## Join {#join}

`POST /api/cluster/join-tokens` mints a token (`token_ttl`, default 15m).
A new node calls `POST /api/cluster/join`.
`require_approval: true` waits for an operator.

## Operations {#ops}

| Action | Route |
| --- | --- |
| Status | `GET /api/cluster/status` |
| Nodes | `GET /api/cluster/nodes` |
| Heartbeat | `POST /api/cluster/nodes/{id}/heartbeat` |
| Rotate cert | `POST /api/cluster/nodes/{id}/rotate-certificate` |
| Revoke node | `POST /api/cluster/nodes/{id}/revoke` |
| Ansible pack | `POST /api/cluster/deploy/ansible` |
| Rolling upgrade | `POST /api/cluster/orchestrate/rolling-upgrade` |
| Rollback | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` |
| Consensus | `GET /api/cluster/consensus` |

`cluster.consensus.provider` is `builtin` in the sample.
`etcd_endpoints` is reserved for an external provider and stays empty unless you switch.
