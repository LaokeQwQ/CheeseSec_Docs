---
title: High Availability & Cluster Federation
linkTitle: Cluster
weight: 120
description: Node join tokens, mutual TLS (mTLS) health and heartbeat interconnects, external consensus coordination, Ansible orchestration, and CLI cluster management.
---

For large-scale, multi-node deployments, CheeseWAF provides a cluster interconnect for mTLS node identity, health and heartbeat reporting, topology/status, and orchestration hooks. The interconnect is not a site-policy replication channel: it does not by itself synchronize site definitions, IP policies, or protection rules. The built-in coordinator is a single-node, in-memory configuration-version log for local/standalone use; multi-node or shared-configuration deployments must use an external coordinator such as etcd and fail closed when that requirement is not met.

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

The built-in consensus provider is intentionally limited to a single node and keeps only an in-memory configuration-version log. For multiple nodes or shared configuration, set `cluster.consensus.provider: etcd` and configure valid `etcd_endpoints`; the service refuses unsafe fallback to builtin heartbeat election.

### Split-Brain Protection & Majority Quorum

- `cluster.protection.freeze_writes_without_majority`: When network partitioning prevents forming a majority quorum, configuration mutations are automatically frozen to prevent state divergence.
- `allow_traffic_in_protection_mode`: Ensures that the data plane continues forwarding and protecting traffic during read-only protection mode.

## 2. Cluster CLI Command Suite {#cli-tools}

CheeseWAF includes a comprehensive CLI suite for controller initialization, node joining, and certificate maintenance:

### 1. Controller Setup & Token Issuance

```bash
# Initialize a local single-node cluster (defaults bind the interconnect to loopback)
cheesewaf cluster init

# Mint a temporary worker join token (default TTL: 15 minutes)
cheesewaf cluster token create --ttl 15m

# List active tokens or revoke an existing token
cheesewaf cluster token list
export CHEESEWAF_TOKEN_ID='token-id-to-revoke'
cheesewaf cluster token revoke "$CHEESEWAF_TOKEN_ID"
```

`cluster init` only writes configuration; the service initializes its cluster identity when cluster mode starts. Before adding remote peers, use routable values for both addresses (for example, rerun with `--force --advertise-addr 10.0.0.1:9444 --listen 0.0.0.0:9444`) and configure external etcd as described above. The command validates address syntax but cannot prove network reachability.

### 2. Worker Node Joining & Certificate Rotation

```bash
export CHEESEWAF_CONTROLLER='https://10.0.0.1:9443'
export CHEESEWAF_JOIN_TOKEN='one-time-join-token'
export CHEESEWAF_NODE_ID='node-worker-02'
export CHEESEWAF_ADVERTISE_ADDR='10.0.0.2:9444'
export CHEESEWAF_CONTROLLER_CA='/etc/cheesewaf/certs/admin-ca.crt'

# Join a worker node into the cluster using a one-time token and local CSR
cheesewaf cluster join \
  --controller "$CHEESEWAF_CONTROLLER" \
  --token "$CHEESEWAF_JOIN_TOKEN" \
  --node-id "$CHEESEWAF_NODE_ID" \
  --advertise-addr "$CHEESEWAF_ADVERTISE_ADDR" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA"

export CHEESEWAF_API_TOKEN='management-token-with-write-cluster'

# Request a new node certificate (requires existing certificate paths; reload/restart the service after writing)
cheesewaf cluster cert rotate \
  --controller "$CHEESEWAF_CONTROLLER" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA" \
  --api-token-env CHEESEWAF_API_TOKEN
# Inspect current node and cluster quorum health
cheesewaf cluster status
```

`--ca-file` is the CA used to verify the controller's HTTPS management endpoint, not the cluster CA returned during enrollment. It is optional when the controller certificate chains to the system trust store; pre-provision the controller's private CA (for example, `admin-ca.crt`) when needed. The join command generates the node's local key and CSR, receives the cluster CA and signed certificate, and writes them under the configured data directory; the private key is never sent to the controller.

Certificate rotation likewise requires a configured existing node identity/certificate path and exactly one API-token source (`--api-token`, `--api-token-file`, or `--api-token-env`). It writes replacement files locally; follow the service's reload/restart procedure before expecting the new certificate to be used.

## 3. Ansible Automated Deployment {#ansible}

To simplify provisioning across dozens of edge nodes, CheeseWAF generates complete Ansible deployment bundles:

- **Playbook Generation API**: Call `POST /api/cluster/deploy/ansible` with a list of nodes, roles (`waf` / `monitor`), SSH ports, and region metadata. The response is JSON with a `files` object mapping relative filenames (for example `inventory.ini`, `playbook.yml`, and role files) to their text contents; save those entries as an Ansible package before running the playbook.
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
| **Consensus State** | `GET /api/cluster/consensus` | Inspect the single-node builtin in-memory version log or external etcd coordination status |

The default provider is `builtin`, which is safe only for a single-node/local deployment and records versions in memory. Multi-node or shared-configuration clusters must select `etcd` and provide `etcd_endpoints`; the built-in coordinator does not replicate site or policy data.
