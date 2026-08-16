---
title: High Availability Clustering & Node Synchronization
linkTitle: Cluster
weight: 120
description: Node join tokens, mutual TLS (mTLS) inter-node communication, embedded consensus, automated rolling upgrades, and cluster state synchronization.
---

In multi-node, large-scale deployments, CheeseWAF supports clustering across distributed nodes. Nodes synchronize site configurations, IP access lists, and defensive rules via secure mutual TLS (mTLS) channels, backed by an embedded consensus engine and rolling upgrade orchestration.

Manage clusters visually in the Web console under **Cluster**, via terminal commands using `cheesewaf cluster`, or programmatically via `/api/cluster/*`.

## 1. Baseline Configuration & Standalone vs. Cluster Mode {#enable}

The default standalone configuration is defined as follows:

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

To enable multi-node clustering:

1. Set `cluster.enabled` to `true` and define a shared `cluster_id`.
2. Assign a globally unique `node_id` to each physical/virtual host.
3. Configure `interconnect.advertise_addr` with an address reachable by all other cluster members.
4. Maintain `mtls_required: true` and configure trusted `ca_file`, `cert_file`, and `key_file` paths on each node.

### Split-Brain & Protection Mode Policies

- `cluster.protection.freeze_writes_without_majority`: Freezes configuration write mutations during network partitions when a quorum majority cannot be reached, preventing state divergence.
- `allow_traffic_in_protection_mode`: Determines whether Data Plane instances continue proxying traffic while the cluster is in protected freeze mode.

## 2. Node Onboarding & Approval Mechanism {#join}

- **Issue Join Tokens**: The primary node invokes `POST /api/cluster/join-tokens` to generate temporary join tokens (validity configured by `token_ttl`; defaults to 15 minutes).
- **Node Join Request**: A candidate node submits its join token to `POST /api/cluster/join`.
- **Administrative Approval**: When `require_approval: true` is configured, joining nodes require manual operator confirmation in the console before cluster synchronization begins.

## 3. Cluster Operations API Reference {#ops}

| Operation | REST API Endpoint | Description |
| --- | --- | --- |
| **Cluster Status** | `GET /api/cluster/status` | Queries overall cluster health, node counts, and quorum status |
| **Node List** | `GET /api/cluster/nodes` | Lists member nodes, IP addresses, software versions, and status |
| **Heartbeat** | `POST /api/cluster/nodes/{id}/heartbeat` | Regular heartbeat status reporting from nodes |
| **Rotate Certificate** | `POST /api/cluster/nodes/{id}/rotate-certificate` | Automated rotation of inter-node mTLS communication certificates |
| **Revoke Node** | `POST /api/cluster/nodes/{id}/revoke` | Revokes node authorization and removes it from cluster membership |
| **Ansible Bundle** | `POST /api/cluster/deploy/ansible` | Exports automated Ansible playbooks for bulk node provisioning |
| **Rolling Upgrade** | `POST /api/cluster/orchestrate/rolling-upgrade` | Initiates zero-downtime rolling upgrades across all nodes |
| **Upgrade Rollback** | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` | Rolls back to the previous stable release upon upgrade failure |
| **Consensus State** | `GET /api/cluster/consensus` | Queries state for embedded Raft consensus or external etcd |

The system uses an embedded consensus provider by default (`cluster.consensus.provider: builtin`). If an existing etcd cluster is available, define `etcd_endpoints` to connect an external consensus backend.
