---
title: 集群高可用与节点协同
linkTitle: 集群
weight: 120
description: 节点加入令牌、mTLS 双向认证健康/心跳互联、外部共识协调、Ansible 自动化编排与 CLI 集群管理工具链。
---

CheeseWAF 提供用于节点 mTLS 身份认证、健康/心跳上报和节点状态查询的集群互联。该互联不是站点策略复制通道。当前可运行配置支持单节点 builtin 协调器；选择 etcd 不会启用可用的共享集群后端，而会拒绝运行。下面的配置和命令不代表已提供可用于生产的多节点 HA。

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

下面的配置描述当前节点互联和准入 contract；它不会让当前二进制直接变成可用于生产的多节点 HA：

1. 将 `deployment.mode` 设置为 `cluster`、`cluster.enabled` 设置为 `true`，并指定全局统一的 `cluster_id`。
2. 为每个物理机/虚拟机节点分配唯一的 `node_id`。
3. 配置 `interconnect.advertise_addr` 为该节点可被集群内其他节点访问的通信地址。
4. 保持 `mtls_required: true`，并在各节点配置受信的 `ca_file`、`cert_file` 与 `key_file` 证书文件。

内置共识提供方只支持单节点。设置 `cluster.consensus.provider: etcd` 并填写 `etcd_endpoints`，不会让当前二进制支持共享集群部署。独立命令的公开参数和当前限制见[独立控制面运行时](../control-plane-runtime/)。

### 脑裂与写保护机制

- `cluster.protection.freeze_writes_without_majority`：当发生网络分区导致无法形成多数派仲裁时，系统将自动冻结配置写操作，防止数据冲突与脑裂。
- `allow_traffic_in_protection_mode`：在写保护模式下，数据平面继续为现有业务提供反向代理与安全检测服务。

## 2. 集群 CLI 命令行运维工具链 {#cli-tools}

CheeseWAF 提供用于集群初始化、令牌/证书操作和心跳检查的 CLI 入口：

### 1. 主控节点初始化与令牌签发

```bash
# 初始化本地单节点集群（互联地址默认只绑定回环）
cheesewaf cluster init

# 签发新的工作节点临时加入令牌（有效期由 --ttl 控制，默认 15m）
cheesewaf cluster token create --ttl 15m

# 查看或吊销现有的加入令牌
cheesewaf cluster token list
export CHEESEWAF_TOKEN_ID='token-id-to-revoke'
cheesewaf cluster token revoke "$CHEESEWAF_TOKEN_ID"
```

`cluster init` 初始化节点集群身份与通信配置。接入远程节点前，应将两个地址都改成可路由值（例如使用 `--force --advertise-addr 10.0.0.1:9444 --listen 0.0.0.0:9444` 重新执行），并配置统一的集群发现与协调后端。

### 2. 工作节点加入与证书轮换

```bash
export CHEESEWAF_CONTROLLER='https://10.0.0.1:9443'
export CHEESEWAF_JOIN_TOKEN='one-time-join-token'
export CHEESEWAF_NODE_ID='node-worker-02'
export CHEESEWAF_ADVERTISE_ADDR='10.0.0.2:9444'
export CHEESEWAF_CONTROLLER_CA='/var/lib/cheesewaf/certs/admin-ca.crt'

# 在工作节点使用一次性令牌与本地 CSR 执行加入
cheesewaf cluster join \
  --controller "$CHEESEWAF_CONTROLLER" \
  --token "$CHEESEWAF_JOIN_TOKEN" \
  --node-id "$CHEESEWAF_NODE_ID" \
  --advertise-addr "$CHEESEWAF_ADVERTISE_ADDR" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA"

export CHEESEWAF_API_TOKEN='management-token-with-write-cluster'

# 请求签发新的节点证书（需已有证书路径；写入后按服务语义 reload/restart）
cheesewaf cluster cert rotate \
  --controller "$CHEESEWAF_CONTROLLER" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA" \
  --api-token-env CHEESEWAF_API_TOKEN
# 检查当前节点的集群健康状态与多数派仲裁
cheesewaf cluster status
```

`--ca-file` 用于校验控制器 HTTPS 管理端证书，并不是加入响应返回的集群 CA。若控制器证书链已受系统信任可省略；使用私有 CA 时，应预先准备控制器 CA（例如 `admin-ca.crt`）。加入命令会在本地生成节点密钥与 CSR，接收集群 CA 和签发证书，并写入配置的数据目录；私钥不会发送给控制器。

证书轮换同样要求节点已有配置的身份/证书路径，并且 API 令牌来源必须三选一（`--api-token`、`--api-token-file` 或 `--api-token-env`）。命令只负责写入替换文件，需按服务的 reload/restart 流程后新证书才会生效。

## 3. Ansible 批量自动化部署 {#ansible}

`POST /api/cluster/deploy/ansible` 导出器生成 CheeseWAF 主服务引导包（inventory、变量、playbook、role、配置模板和 README）。运行前必须补充经过校验的二进制 URL 和 SHA-256、服务路径与所需配置，并逐条复核生成的命令。导出包不提供插件安装，也不是可直接运行的生产多节点 HA 部署包。

- **Playbook 导出接口**：调用 `POST /api/cluster/deploy/ansible`，传入目标节点的主机清单、角色（`waf` / `monitor`）、SSH 端口与地域标签。响应为 JSON，`files` 对象将相对文件名（如 `inventory.ini`、`playbook.yml` 及角色文件）映射到文本内容；保存后先填写经过校验的二进制变量和 etcd 设置，人工复核命令，再执行 playbook。
- **Web 控制台导出**：在 Web 管理控制台的 **集群管理** 模块中，可录入节点拓扑并点击「导出 Ansible 部署包」；下载内容仍需人工补全和复核，不是拿来就能执行的生产包。

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
| **滚动升级** | `POST /api/cluster/orchestrate/rolling-upgrade` | 创建按节点顺序编排的升级任务 |
| **升级回滚** | `POST /api/cluster/orchestrate/rolling-upgrade/{id}/rollback` | 创建逆序回滚任务，依据备份恢复配置 |
| **共识状态** | `GET /api/cluster/consensus` | 查看当前集群共识提供方与健康状态 |

单节点部署默认采用 `builtin` 模式。配置外部 `etcd` 端点，不会让当前二进制成为受支持的生产多节点 HA 部署。
