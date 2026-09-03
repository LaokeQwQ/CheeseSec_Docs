---
title: High Availability & Cluster Federation
linkTitle: Cluster
weight: 120
description: Node join tokens, mutual TLS (mTLS) interconnects, built-in Raft consensus, Ansible automated orchestration, and CLI cluster management.
---

For large-scale, multi-node deployments, CheeseWAF supports distributed high-availability clustering. Cluster nodes synchronize site configurations, IP policies, and protection rules over mutual TLS (mTLS), backed by built-in consensus, automated certificate rotation, Ansible deployment generation, and zero-downtime rolling upgrades.

Cluster administration is accessible via the **Cluster** module in the Web Console, the `cheesewaf cluster` CLI commands, or REST APIs at `/api/cluster/*`.

## 1. Core Architecture & Configuration {#enable}

The default standalone configuration:

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

Steps to enable multi-node clustering:

1. Set `cluster.enabled` to `true` and assign a consistent `cluster_id`.
2. Assign a globally unique `node_id` to each physical or virtual instance.
3. Configure `interconnect.advertise_addr` as the routable IP/port accessible by peer nodes.
4. Keep `mtls_required: true` and configure trusted `ca_file`, `cert_file`, and `key_file` paths.

### Split-Brain Protection & Majority Quorum

- `cluster.protection.freeze_writes_without_majority`: When network partitioning prevents forming a majority quorum, configuration mutations are automatically frozen to prevent state divergence.
- `allow_traffic_in_protection_mode`: Ensures that the data plane continues forwarding and protecting traffic during read-only protection mode.

## 2. Cluster CLI Command Suite {#cli-tools}

CheeseWAF includes a comprehensive CLI suite for controller initialization, node joining, and certificate maintenance:

### 1. Controller Setup & Token Issuance

```bash
# Initialize current node as cluster controller and mint the cluster CA
cheesewaf cluster init

# Mint a temporary worker join token (default TTL: 15 minutes)
cheesewaf cluster token create --ttl 15m

# List active tokens or revoke an existing token
cheesewaf cluster token list
cheesewaf cluster token revoke <token_id>
```

### 2. Worker Node Joining & Certificate Rotation

```bash
# Join a worker node into the cluster using a token
cheesewaf cluster join \
  --controller https://10.0.0.1:9444 \
  --token <token> \
  --node-id node-worker-02 \
  --advertise-addr 10.0.0.2:9444 \
  --ca-cert /etc/cheesewaf/certs/cluster-ca.crt

# Rotate node interconnect mTLS certificates online
cheesewaf cluster cert rotate

# Inspect current node and cluster quorum health
cheesewaf cluster status
```

## 3. Ansible Automated Deployment {#ansible}

To simplify provisioning across dozens of edge nodes, CheeseWAF generates complete Ansible deployment bundles:

- **Playbook Generation API**: Call `POST /api/cluster/deploy/ansible` with a list of nodes, roles (`controller` / `worker`), SSH ports, and region metadata. CheeseWAF returns an archive containing `hosts.ini`, systemd definitions, installation tasks, and certificate distribution scripts.
- **Web UI Export**: In the **Cluster** view of the Web Console, configure the target node inventory and click "Export Ansible Bundle" to download ready-to-run playbooks.

## 4. Cluster REST API Reference {#ops}

| Operation | REST API Route | Description |
| --- | --- | --- |
| **Cluster Health** | `GET /api/cluster/status` | Query overall topology, software versions, and quorum state |
| **Node List** | `GET /api/cluster/nodes` | List active nodes, IPs, and heartbeat timestamps |
| **Issue Join Token** | `POST /api/cluster/join-tokens` | Mint a temporary join token |
| **Join Node** | `POST /api/cluster/join` | Join cluster carrying an authorized token |
| **Rotate Certificate** | `POST /api/cluster/nodes/{id}/rotate-certificate` | Rotate interconnect mTLS certificates |
| **Revoke Node** | `POST /api/cluster/nodes/{id}/revoke` | Revoke node certificate and evict from cluster |
| **Ansible Bundle** | `POST /api/cluster/deploy/ansible` | Export Ansible deployment playbooks |
| **Rolling Upgrade** | `POST /api/cluster/orchestrate/rolling-upgrade` | Trigger zero-downtime rolling upgrades |
| **Upgrade Rollback** | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` | Roll back to previous release version |
| **Consensus State** | `GET /api/cluster/consensus` | Inspect built-in Raft or external etcd status |

The system uses the built-in Raft consensus provider by default (`cluster.consensus.provider: builtin`). Existing external etcd clusters can be connected via `etcd_endpoints`.
