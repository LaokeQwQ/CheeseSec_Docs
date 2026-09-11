---
title: 商业化平台架构
linkTitle: 商业化架构
weight: 130
description: CheeseWAF 控制面、数据面、插件、CRP、离线模式、诊断上传和灾备边界。
---

本文记录未来商业化能力的目标架构，不代表当前二进制已经提供这些服务。当前运行时使用 SQLite 保存管理状态，可选 PostgreSQL 日志 Sink，Bot 挑战使用内存后端，集群当前只有 builtin 单节点路径；配置 etcd 没有后端协调器，会 fail-closed。

CRP 解析器/导入器和本地 RuntimeStore 已提供经过验证的本地 staged/promote/rollback/reopen contract。CLI 提供 `crp verify` 和仅暂存的 `crp stage`；`crp activate` 与 `crp rollback` 也已经存在，但没有受保护的控制面和 sidecar 适配器时会 fail-closed。它们还不是完整的插件执行、服务启动、集群分发或 OTA 生命周期。CWEDP/NetLease transport 已作为独立包边界实现并有测试证据；主服务、节点注册、安装流程和生产编排仍需接线。

## 数据面和控制面

WAF 数据面负责低延迟检测、反向代理和已加载策略快照。未来的 `cheesewaf-control` 计划负责审批、Token、CRP、权限、审计和期望状态。独立命令的当前边界、探针和 fail-closed 启动行为见[独立控制面运行时](../control-plane-runtime/)。当前运行时还没有独立控制面、插件外部存储或租约服务。

目标设计使用 PostgreSQL 保存持久管理数据，native-raft 保存成员、epoch、fencing、期望配置和回滚引用，Redis 保存短期租约和缓存。当前 SQLite 管理存储尚未迁移到这套目标架构。

## 插件与 CRP

目标包模型计划使用 CheeseSec Vendor Root 和阈值签名。2-of-3、3-of-5、企业命名空间和默认信任规则都是规划内容，当前运行时不会执行。

目标 CRP 导入器会检查格式、摘要、签名、命名空间、来源和版本；当前 CLI 已在显式提供信任根与来源注册的前提下支持验证和暂存。吊销/透明日志强制及服务端激活尚未形成生产运行时导入入口。

当前 Ansible 导出器只负责 CheeseWAF 基础设施。内部 CWEDP 协议、broker、PostgreSQL ResumeStore、broker-bound HTTP/file transport 和 NetLease 边界已覆盖 HELLO/CAPABILITIES 协商、离线来源选择、来源隔离、分块断点续传、幂等、直接 IP 拨号、TLS/mTLS/NodeID/leaf pin 以及 MD5/SHA-1/SHA-256 校验，但尚未接入主 `serve`、节点注册、插件安装或生产编排。因此当前导出器或服务仍不会执行端到端的 CRP 安装、升级、回滚或 OTA 分发。

跨仓库交接边界如下：Ansible 可以引导基础设施、CheeseWAF 控制面和分发代理，但不得安装、升级、回滚、签名、晋级或改写插件 CRP。上述生命周期由经过认证的 CWEDP 自协商分发负责；Peer、镜像、OTA 端点和 Ansible 部署包只能作为传输来源，不能改变 manifest、签名集合、来源根、发布序号或 promotion 状态。

DuckDB 是默认关闭的可选 sidecar 或 CLI，只读取异步写入的 Parquet，用于跨集群分析和审计。它不参与 inline 授权，不进入 WAF 请求路径，也不承载 PostgreSQL、native-raft 或 Redis 状态。

## 离线模式

目标离线模式会限制管理扩展主动联网，同时允许数据面访问已配置的 Origin。当前二进制没有独立的插件出站控制器。

本地 `cheesewaf temporary-online probe` 已提供一次性 HTTPS broker、管理员确认、直接 IP TLS pin、有限计量和元数据审计。插件/控制面租约签发接口、`serve` 启动接线、持久租约生命周期和主机级出站强制仍未作为生产 API 暴露。

## 诊断上传

目标设计会把诊断上传限制为异步、脱敏接口。当前运行时没有插件诊断上传端点。

信封加密、对象存储和可恢复队列属于后续安全设计，当前二进制尚未启用。

## 运维原则

- 首次高风险操作明确确认，同一授权范围内减少重复输入，实质变化必须重新确认。
- 对象存储、透明日志、SIEM、KMS、LLM 或 Redis 故障只改变对应管理任务状态。
- 已验证 last-known-good 继续工作；高风险新操作在安全证据不足时进入 pending/staged。
- 任何确认、网络租约、上传、复制、回执、删除、吊销和恢复都有审计记录。
