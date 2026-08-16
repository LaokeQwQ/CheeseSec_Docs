---
title: 集群高可用与节点协同
linkTitle: 集群
weight: 120
description: 节点加入令牌、mTLS 双向认证通信、内置共识引擎、自动化滚动升级与节点状态同步。
---

在多节点大规模部署场景下，CheeseWAF 支持组建分布式高可用集群。集群各节点间通过安全 mTLS 双向认证同步站点配置、IP 黑白名单与防护规则，并提供内置共识引擎与滚动升级编排能力。

在 Web 管理控制台中进入 **集群管理** 模块，或通过命令行 `cheesewaf cluster` 及 REST API `/api/cluster/*` 进行管理。

## 1. 基础配置与单机/集群模式 {#enable}

单机默认配置如下：

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

启用集群多节点协同的步骤：

1. 将 `cluster.enabled` 设置为 `true`，并指定统一的 `cluster_id`。
2. 为每个物理/虚拟节点分配全局唯一的 `node_id`。
3. 配置 `interconnect.advertise_addr` 为该节点可被集群内其他节点访问的通信地址。
4. 保持 `mtls_required: true`，并在各节点配置受信的 `ca_file`、`cert_file` 与 `key_file` 证书文件。

### 脑裂与保护模式配置

- `cluster.protection.freeze_writes_without_majority`：当网络分区导致无法形成多数派仲裁时，自动冻结配置写操作，防止数据冲突。
- `allow_traffic_in_protection_mode`：指定在保护模式下数据平面是否继续提供反向代理与检测服务。

## 2. 节点加入与审批机制 {#join}

- **生成加入令牌**：主控节点调用 `POST /api/cluster/join-tokens` 签发临时加入令牌（有效期由 `token_ttl` 控制，默认为 15 分钟）。
- **节点发起加入**：待加入节点携带令牌调用 `POST /api/cluster/join` 请求加入集群。
- **安全审批**：若配置了 `require_approval: true`，新节点须经安全管理员在控制台手动审批后方可同步集群数据。

## 3. 集群常用运维接口 {#ops}

| 运维操作 | REST API 路由 | 说明 |
| --- | --- | --- |
| **集群健康状态** | `GET /api/cluster/status` | 查询集群整体健康度与仲裁状态 |
| **节点清单** | `GET /api/cluster/nodes` | 列出所有节点、IP、版本与在线状态 |
| **心跳同步** | `POST /api/cluster/nodes/{id}/heartbeat` | 节点定期上报心跳 |
| **证书轮换** | `POST /api/cluster/nodes/{id}/rotate-certificate` | 自动化轮换互联 mTLS 通信证书 |
| **节点下线吊销** | `POST /api/cluster/nodes/{id}/revoke` | 吊销节点证书并踢出集群 |
| **Ansible 部署包** | `POST /api/cluster/deploy/ansible` | 导出用于批量自动化部署的 Playbook |
| **滚动升级** | `POST /api/cluster/orchestrate/rolling-upgrade` | 触发集群节点的零停机滚动升级 |
| **升级回滚** | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` | 升级异常时一键回滚至上一稳定版本 |
| **共识状态** | `GET /api/cluster/consensus` | 查看内置 Raft 共识或外部 etcd 状态 |

系统默认采用内置共识提供方（`cluster.consensus.provider: builtin`）。若已有成熟的 etcd 集群，亦可通过配置 `etcd_endpoints` 接入外部共识服务。
