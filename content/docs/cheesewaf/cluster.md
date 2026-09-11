---
title: High Availability & Cluster Federation
linkTitle: Cluster
weight: 120
description: Node join tokens, mutual TLS (mTLS) health and heartbeat interconnects, external consensus coordination, Ansible orchestration, and CLI cluster management.
---

For large-scale, multi-node deployments, CheeseWAF provides a cluster interconnect for mTLS node identity, health and heartbeat reporting, topology/status, and orchestration hooks. The interconnect is not a site-policy replication channel. The current runnable path is a builtin single-node coordinator; selecting etcd records the shared-cluster requirement but has no etcd-backed coordinator in this binary, so it fails closed rather than falling back from a shared deployment to heartbeat election. The commercial target is native-raft for desired-state ordering, epoch fencing, and rollback references, with PostgreSQL as durable management truth. Until that migration is complete, this page's etcd commands describe a contract and are not evidence that native-raft is already shipped.

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

The following values describe the current interconnect and admission contract; they do not turn the current binary into a production multi-node HA deployment:

1. Set `deployment.mode: cluster` and `cluster.enabled: true`, then assign a consistent `cluster_id`.
2. Assign a globally unique `node_id` to each physical or virtual instance.
3. Configure `interconnect.advertise_addr` as the routable IP/port accessible by peer nodes.
4. Keep `mtls_required: true` and configure trusted `ca_file`, `cert_file`, and `key_file` paths.

The built-in consensus provider is intentionally limited to a single node and keeps only an in-memory configuration-version log. Selecting `cluster.consensus.provider: etcd` with `etcd_endpoints` records the required shared-cluster contract, but the current binary has no etcd-backed coordinator and therefore remains in protection mode instead of pretending that heartbeat state is consensus. The staged native-raft contract is documented in [Commercial Architecture](../commercial-architecture/); the separate command's current startup and join limits are in [Standalone Control Runtime](../control-plane-runtime/). Neither page enables native-raft through this configuration key.

### Split-Brain Protection & Majority Quorum

- `cluster.protection.freeze_writes_without_majority`: When network partitioning prevents forming a majority quorum, configuration mutations are automatically frozen to prevent state divergence.
- `allow_traffic_in_protection_mode`: Ensures that the data plane continues forwarding and protecting traffic during read-only protection mode.

## 2. Cluster CLI Command Suite {#cli-tools}

CheeseWAF includes a CLI surface for local cluster initialization, token/certificate operations, and heartbeat checks. These commands expose the current compatibility contract; they do not make the unwired shared-cluster backend production-ready:

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

`cluster init` only writes configuration; the service initializes its cluster identity when cluster mode starts. Before adding remote peers, use routable values for both addresses (for example, rerun with `--force --advertise-addr 10.0.0.1:9444 --listen 0.0.0.0:9444`) and configure the explicit etcd contract described above. Because the etcd backend and native-raft startup unit are not wired, this remains a local compatibility surface and does not provide production HA. The command validates address syntax but cannot prove network reachability.

### 2. Worker Node Joining & Certificate Rotation

```bash
export CHEESEWAF_CONTROLLER='https://10.0.0.1:9443'
export CHEESEWAF_JOIN_TOKEN='one-time-join-token'
export CHEESEWAF_NODE_ID='node-worker-02'
export CHEESEWAF_ADVERTISE_ADDR='10.0.0.2:9444'
export CHEESEWAF_CONTROLLER_CA='/var/lib/cheesewaf/certs/admin-ca.crt'

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

The current `POST /api/cluster/deploy/ansible` exporter generates a CheeseWAF daemon bootstrap package only (inventory, variables, playbook, role, configuration template, and README). It does not include a CWEDP agent and is not a ready-to-run production bundle: before execution, provide a verified binary URL and SHA-256, service paths, and (for more than one node) the external etcd endpoints required by the generated role. The optional `deploy/ansible/full.yml` playbook can install a pull-only CWEDP agent only in its explicit `provision_only=true` hand-off mode, after all external control-plane preflight values plus the agent URL and SHA-256 are supplied; it still does not make CheeseWAF production storage runnable. Plugin CRP installation, upgrade, rollback, signing, promotion, and authenticated distribution are never performed by Ansible; those lifecycle operations belong to CWEDP.

- **Playbook Generation API**: Call `POST /api/cluster/deploy/ansible` with a list of nodes, roles (`waf` / `monitor`), SSH ports, and region metadata. The response is JSON with a `files` object mapping relative filenames (for example `inventory.ini`, `playbook.yml`, and role files) to their text contents. Save those entries as a package, fill in the required verified binary variables and etcd settings, review the generated commands, and only then run the playbook.
- **Web UI Export**: In the **Cluster** view of the Web Console, configure the target node inventory and click "Export Ansible Bundle" to download the generated bundle for review and completion; it is not a ready-to-run production package.

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
| **Rolling Upgrade** | `POST /api/cluster/orchestrate/rolling-upgrade` | Create a sequential orchestration task; remote installation/restart and zero-downtime guarantees are not provided by the current compatibility path |
| **Upgrade Rollback** | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` | Create a reverse-order rollback task when external backups are available; native-raft/canary fencing and a remote restore worker are not wired |
| **Consensus State** | `GET /api/cluster/consensus` | Inspect builtin in-memory status or the configured-but-unwired etcd requirement; it is not proof of a running external coordinator |

The default provider is `builtin`, which is safe only for a single-node/local deployment and records versions in memory. Multi-node or shared-configuration configurations must select `etcd` and provide `etcd_endpoints`, but the current binary fails closed until an etcd-backed coordinator is wired; the built-in coordinator does not replicate site or policy data. Native-raft migration remains a planned implementation stage and must not be inferred from the presence of this documentation.
