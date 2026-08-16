---
title: 集群
linkTitle: 集群
weight: 120
description: 加入令牌、互联 mTLS、内置共识、滚动升级和流量对等节点。
---

控制台：**集群**。
配置：`cluster`。
命令行：`cheesewaf cluster`。
REST：`/api/cluster/*`。

示例是单节点：

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

## 打开集群 {#enable}

1. 把 `cluster.enabled` 设成 `true`，并指定 `cluster_id`。
2. 每个节点用不同的 `node_id`。
3. 把 `interconnect.advertise_addr` 设成其他节点能访问的地址。
4. 保持 `mtls_required: true`。填好 `ca_file`、`cert_file`、`key_file`。

`cluster.protection.freeze_writes_without_majority` 在没有多数派时停止写配置。
`allow_traffic_in_protection_mode` 决定这种保护模式下数据平面还要不要转发。

## 加入 {#join}

`POST /api/cluster/join-tokens` 签发令牌（`token_ttl`，默认 15 分钟）。
新节点调用 `POST /api/cluster/join`。
`require_approval: true` 时要等运维批准。

## 运维动作 {#ops}

| 动作 | 路由 |
| --- | --- |
| 状态 | `GET /api/cluster/status` |
| 节点 | `GET /api/cluster/nodes` |
| 心跳 | `POST /api/cluster/nodes/{id}/heartbeat` |
| 轮换证书 | `POST /api/cluster/nodes/{id}/rotate-certificate` |
| 吊销节点 | `POST /api/cluster/nodes/{id}/revoke` |
| Ansible 包 | `POST /api/cluster/deploy/ansible` |
| 滚动升级 | `POST /api/cluster/orchestrate/rolling-upgrade` |
| 回滚 | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` |
| 共识 | `GET /api/cluster/consensus` |

示例里 `cluster.consensus.provider` 是 `builtin`。
`etcd_endpoints` 留给外部提供方，不切换就保持空。
