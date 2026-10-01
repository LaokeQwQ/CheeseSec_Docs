---
title: 商业化平台架构
linkTitle: 商业化架构
weight: 130
description: CheeseWAF 控制面、数据面、插件、CRP、离线模式、诊断上传和灾备边界。
---

本文档定义 CheeseWAF 商业化平台架构设计，涵盖控制面、数据面、插件安全规范及受限网络运维边界。

## 数据面和控制面

系统采用控制平面与数据平面分离的架构设计：
- **WAF 数据面**：处理请求检测、反向代理和当前策略快照评估。本文不对延迟或吞吐量作数值承诺。
- **独立控制面（`cheesewaf-control`）**：当前命令可连接 PostgreSQL 与 native-raft，提供 loopback 绑定的健康、就绪、状态和提案接口；它还不是完整的远程管理 API 或主 WAF 的高可用控制平面。运行边界见[独立控制面运行时](../control-plane-runtime/)。
- **状态存储**：代码包含 PostgreSQL、Redis 和 native-raft 适配器。生产模式要求显式配置依赖，缺失时 fail-closed；这些适配器本身不等于已完成多节点部署或灾备验收。

## 插件与 CRP 规范

CRP（CheeseWAF Resources Package）是平台定义的标准化资源扩展包：
- **信任根与签名校验**：支持官方 Vendor Root 与企业私有根，采用 Ed25519 阈值签名（如 2-of-3 签名）防篡改。
- **本地校验与暂存**：CLI 提供 `crp verify` 与 `crp stage` 命令，在显式指定信任根与来源的前提下进行离线解包、摘要校验与受控目录暂存。
- **激活与回滚**：生产 CRP 路由通过 PostgreSQL 授权、native-raft fencing 和 mTLS sidecar 执行；缺少必要依赖时拒绝操作。该流程不代表插件代码已全部具备可运行的扩展宿主。
- **OTA 状态**：当前 OTA 客户端只校验只读 HTTPS 索引并保留 last-known-good 文件状态；候选版本不会触发下载、安装或激活。

DuckDB 分析是规划中的 Plugin 扩展：由宿主提供引擎，以异步一次性任务读取已验证的脱敏 Parquet 快照，只输出 `analysis-record/v1`。它不得进入请求热路径或直接改变 WAF 策略。当前 CheeseWAF 尚无 DuckDB 作业运行时或审计导出器；接入前还需落实输入验证、OS 沙箱和资源限制。

## 离线模式与临时出站

在物理隔离或内网环境中，离线模式切断管理扩展的所有外部主动出站连接，同时保障数据面至后端源站（Origin）的正常转发：
- 本地 `cheesewaf temporary-online probe` 提供一次性受限 HTTPS 代理，需管理员二次授权，具备 IP 与 TLS 固定绑定及审计能力。
- 只有经过管理员明确审批的操作方可获得临时网络租约。

## 诊断与审计

- 诊断数据严格遵循最小化与脱敏原则，避免将敏感业务数据写入诊断日志。
- 高风险运维操作遵循首次明确确认、同一授权窗口内避免重复打扰、环境参数变动重新确认的安全原则。
