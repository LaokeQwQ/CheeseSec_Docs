---
title: 集群高可用与节点协同
linkTitle: 集群
weight: 120
description: 节点加入令牌、mTLS 双向认证通信、内置 Raft 共识引擎、Ansible 自动化编排与 CLI 集群管理工具链。
---

在大规模多节点部署场景下，CheeseWAF 支持组建分布式高可用集群。集群各节点间通过安全 mTLS 双向认证同步站点配置、IP 黑白名单与防护规则，并提供内置共识引擎、自动证书轮换、Ansible 批量部署与滚动升级能力。

在 Web 管理控制台中可进入 **集群管理** 模块，或通过命令行 `cheesewaf cluster` 与 REST API `/api/cluster/*` 进行管理。

## 1. 基础配置与模式定义 {#enable}

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

1. 将 `cluster.enabled` 设置为 `true`，并指定全局统一的 `cluster_id`。
2. 为每个物理机/虚拟机节点分配唯一的 `node_id`。
3. 配置 `interconnect.advertise_addr` 为该节点可被集群内其他节点访问的通信地址。
4. 保持 `mtls_required: true`，并在各节点配置受信的 `ca_file`、`cert_file` 与 `key_file` 证书文件。

### 脑裂与写保护机制

- `cluster.protection.freeze_writes_without_majority`：当发生网络分区导致无法形成多数派仲裁时，系统将自动冻结配置写操作，防止数据冲突与脑裂。
- `allow_traffic_in_protection_mode`：在写保护模式下，数据平面继续为现有业务提供反向代理与安全检测服务。

## 2. 集群 CLI 命令行运维工具链 {#cli-tools}

CheeseWAF 提供了开箱即用的集群 CLI 指令集，方便在终端完成控制面初始化与工作节点加入：

### 1. 主控节点初始化与令牌签发

```bash
# 将当前节点初始化为主控控制器，并生成集群根 CA 证书
cheesewaf cluster init

# 签发新的工作节点临时加入令牌（有效期由 --ttl 控制，默认 15m）
cheesewaf cluster token create --ttl 15m

# 查看或吊销现有的加入令牌
cheesewaf cluster token list
cheesewaf cluster token revoke <token_id>
```

### 2. 工作节点加入与证书轮换

```bash
# 在从属节点执行加入指令
cheesewaf cluster join \
  --controller https://10.0.0.1:9444 \
  --token <token> \
  --node-id node-worker-02 \
  --advertise-addr 10.0.0.2:9444 \
  --ca-cert /etc/cheesewaf/certs/cluster-ca.crt

# 在线安全轮换当前节点的 mTLS 互联证书
cheesewaf cluster cert rotate

# 检查当前节点的集群健康状态与多数派仲裁
cheesewaf cluster status
```

## 3. Ansible 批量自动化部署 {#ansible}

为了支持数十至数百台边缘节点的大规模快速交付，CheeseWAF 支持一键导出标准 Ansible 部署包：

- **Playbook 导出接口**：调用 `POST /api/cluster/deploy/ansible`，传入目标节点的主机清单、角色（`controller` / `worker`）、SSH 端口与地域标签，系统将自动生成完整的 Ansible Playbook 压缩包（包含 `hosts.ini`、安装任务、systemd 配置与证书下发流程）。
- **Web 控制台导出**：在 Web 管理控制台的 **集群管理** 模块中，可直接通过图形界面录入节点拓扑并点击「导出 Ansible 部署包」。

## 4. 集群核心 REST API 参考 {#ops}

| 运维操作 | REST API 路由 | 说明 |
| --- | --- | --- |
| **集群健康状态** | `GET /api/cluster/status` | 查询集群整体拓扑、版本与仲裁状态 |
| **节点清单** | `GET /api/cluster/nodes` | 列出所有节点信息、IP 与最后心跳时间 |
| **生成加入令牌** | `POST /api/cluster/join-tokens` | 签发临时加入令牌 |
| **节点加入** | `POST /api/cluster/join` | 携带令牌请求加入集群 |
| **证书轮换** | `POST /api/cluster/nodes/{id}/rotate-certificate` | 自动化轮换互联 mTLS 通信证书 |
| **节点下线吊销** | `POST /api/cluster/nodes/{id}/revoke` | 吊销节点证书并踢出集群 |
| **Ansible 部署包** | `POST /api/cluster/deploy/ansible` | 导出用于批量自动化部署的 Playbook |
| **滚动升级** | `POST /api/cluster/orchestrate/rolling-upgrade` | 触发集群节点的零停机滚动升级 |
| **升级回滚** | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` | 升级异常时一键回滚至上一稳定版本 |
| **共识状态** | `GET /api/cluster/consensus` | 查看内置 Raft 共识或外部 etcd 状态 |

系统默认采用内置共识提供方（`cluster.consensus.provider: builtin`）。若已有成熟的 etcd 集群，亦可通过配置 `etcd_endpoints` 接入外部共识服务。
