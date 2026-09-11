---
title: 独立控制面运行时
linkTitle: 控制面运行时
weight: 140
description: 独立 cheesewaf-control 进程的命令参数、启动检查、本地状态接口和当前限制。
---

代码仓库包含独立的 `cheesewaf-control` 控制面进程。它会打开控制面 PostgreSQL 适配器和 native-raft 运行时，再提供本地状态服务。它不处理 WAF 请求，不托管 Web 控制台，也不替代主 `cheesewaf serve` 进程。

{{% pageinfo color="warning" %}}
本文说明当前源码和运行时契约，不是高可用部署手册。主 `cheesewaf serve` 路径仍使用 `storage.profile: temporary` 和内置 SQLite；生产管理存储仍会以 `ErrProductionStorageUnavailable` 拒绝启动。独立进程不提供空集群初始化、远程 join 流程、插件安装、OTA 或 CWEDP 执行。
{{% /pageinfo %}}

## 命令边界 {#command}

进程只接受命令行参数，不接受位置参数。

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
  --postgres-dsn '<由受保护的密钥来源提供>' \
  --timeout 15s
```

| 参数 | 默认值 | 规则 |
| --- | --- | --- |
| `--profile` | `production` | 只接受 `production` 配置。 |
| `--cluster-id` | 空 | 必填。不能包含空白、控制字符或不可见格式字符。 |
| `--node-id` | 自动生成 | 可选。不填写时，native-raft 会在 `--data-dir` 下生成并保存节点身份。 |
| `--data-dir` | 空 | 必填。请使用持久且权限受限的目录保存 native-raft 状态和快照。 |
| `--listen` | `127.0.0.1:9450` | 本地管理 HTTP 地址，必须是回环 `host:port`。 |
| `--raft-listen` | `127.0.0.1:9451` | native-raft 地址，必须是不同的回环 `host:port`。 |
| `--mode` | `join` | 只能是 `bootstrap` 或 `join`；默认值不会初始化集群。 |
| `--ca-file` | 空 | 必填的控制面和 native-raft TLS 信任 CA PEM 文件，必须是权限受限的普通文件。 |
| `--cert-file` | 空 | 必填的节点证书 PEM；设置 `--node-id` 时，证书身份必须匹配。 |
| `--key-file` | 空 | 必填的节点私钥 PEM，建议权限为 `0600`，不得写入日志或源码仓库。 |
| `--postgres-dsn` | 空 | 必填的管理 PostgreSQL DSN，不会写入状态 JSON。 |
| `--timeout` | `15s` | 必须为正数。超时会停止启动。 |

两个监听地址都会校验为回环地址。当前命令不提供远程管理监听。若要远程部署，需要单独设计 TLS、mTLS、ACL、审计和回滚控制。

`--postgres-dsn` 是独立的管理状态连接，不能与 `storage.postgresql.dsn` 混淆。后者仍是 `cheesewaf` 使用的可选异步访问日志 Sink。回环地址和 Unix Socket 的 PostgreSQL 连接可以使用；远程 PostgreSQL 主机必须启用并校验证书的 TLS。这个进程不会打开 Redis 连接。

CA、节点证书和私钥必须由受保护的配置流程提前生成并放置。没有真实 PostgreSQL、Raft TLS 和一致快照时，这个示例仍会 fail-closed；它不是可以直接成功创建 HA 集群的安装步骤。

## 启动顺序与 fail-closed 行为 {#startup}

只有完整的生产启动流程成功后，`cheesewaf-control` 才会绑定 HTTP 监听器：

1. 打开管理 PostgreSQL 适配器。
2. 执行 PostgreSQL 控制面表迁移并检查健康状态。
3. 读取 PostgreSQL 控制状态快照。
4. 打开、准备并检查 native-raft。
5. 读取 native-raft 快照。
6. 比较两份快照，包括 cluster、leader、term、epoch、revision、期望版本、摘要、载荷、冻结状态和 nonce ledger。
7. 校验快照，确认它没有覆盖本机已经保存的 last-known-good 状态。
8. 建立 fencing token，并确认它绑定同一个 cluster、leader、epoch、revision、摘要和 nonce。
9. 再次读取 native-raft。fencing 后如果 leader、term、epoch、revision 或摘要发生变化，启动失败。
10. 安装一致的快照，恢复控制面写入，并报告 `ready`。

迁移、健康检查、快照比较、校验或 fencing 任一步失败，命令都会返回错误。命令输出 `control-plane startup failed closed`，并在启动状态服务前退出。未验证的快照不会进入 ready 状态，系统也不会接受 proposal。若上层 supervisor 特意使用运行时提供的冻结诊断模式，可以暴露存活状态和冻结原因；这种模式不会报告 ready，也不会恢复写入。

当 PostgreSQL 没有状态行、native-raft 也没有状态时，两边都会得到空的冻结状态。要进入 ready，仍必须有已提交的 desired state revision、非零 term 和 epoch、已建立的 leader，以及匹配的 fencing nonce。因此，仅设置 `--mode bootstrap` 不能初始化空的生产集群，也不能凭空生成第一份期望状态。

## 本地状态接口 {#endpoints}

状态服务供本机 supervisor 和探针使用。它监听 `--listen`，该地址会被校验为仅限回环。

| 方法 | 路径 | 响应 |
| --- | --- | --- |
| `GET` | `/healthz` | 始终返回 `200` 和当前状态文档。若 supervisor 特意暴露冻结诊断，冻结状态也可以报告存活。 |
| `GET` | `/readyz` | 只有 `ready` 和 `write_ready` 都为 `true` 时返回 `200`，否则返回 `503`。 |
| `GET` | `/status` | 返回 `200`，内容包括阶段、ready 状态、集群/节点身份、leader、term、epoch、revision、更新时间和有长度限制的冻结原因。 |
| `POST` | `/proposals` | 未进入写入 ready 前返回 `503`；进入写入 ready 后，当前二进制因 proposal transport 尚未挂载而返回 `501`。其他方法返回 `405`。 |

状态响应不会包含凭据、PostgreSQL DSN、文件路径或后端原始错误。这个接口只用于本地诊断，不是集群 API。

## Bootstrap 与 join 模式 {#modes}

`bootstrap` 和 `join` 是 native-raft 的启动模式，不是完整的集群管理流程。

- `bootstrap` 只有在数据目录没有既有 Raft 状态时，才会调用 native-raft 的一次性 `BootstrapCluster`。进程仍然需要一致的 PostgreSQL 与 native-raft 快照，以及有效的已提交 fencing，才能进入 ready。
- `join` 不会调用 `BootstrapCluster`。全新的 join 节点不会自行成为 leader，也不能把空状态变成集群。当前 CLI 没有 controller 地址、join token 或远程注册参数。
- native-raft 包提供 leader 侧的 `Join` 操作，用于添加 voter。这个操作是内部运行时 API，不是 HTTP 接口，也不是 `cheesewaf-control` 子命令。在完整、经过测试的 follower 注册流程发布前，应把 `join` 视为只读注册模式。

因此，当前独立命令不能创建空集群、自动加入对等节点，也不能宣称已经提供生产级多节点 HA。仓库中的 native-raft 和 PostgreSQL 代码定义了一致性边界，但不会让现有 `cheesewaf serve` 自动切换到 PostgreSQL 或 native-raft 存储路径。

## 与主服务的关系 {#serve}

`cheesewaf serve` 仍是主 WAF 入口。它负责数据平面监听和现有管理平面；当前可运行的管理存储配置仍是 `storage.profile: temporary`。在主服务中添加管理 PostgreSQL DSN，或设置 `storage.profile: production`，都不会把它迁移到这个独立进程。主服务仍会等待完整的 PostgreSQL、Coordinator、native-raft、审批、审计和数据面接线完成后，才可能解除 fail-closed。

更大的目标架构见[商业化平台架构](../commercial-architecture/)。本文说明独立命令的可执行边界，应与仓库中的控制面启动契约一起阅读。
