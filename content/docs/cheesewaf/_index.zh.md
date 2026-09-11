---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: 商用级自托管 Web 应用防火墙。提供系统部署、安全防护、配置参考及运维管理手册。
---

CheeseWAF 是自托管 Web 应用防火墙（WAF），以 Go 核心程序分发。当前运行时使用内置 SQLite 保存管理状态。PostgreSQL 只是可选的异步访问日志 Sink；Redis 尚未接入 Bot 挑战后端。集群协调当前只有单节点 `builtin` 路径；选择 `etcd` 只能记录共享集群要求，当前二进制没有 etcd 后端协调器，会保持 fail-closed。独立商业化控制面、native-raft、CWEDP 和 Socket Lease 服务尚未接入启动路径。CRP 已有本地验证导入和 staged 槽位层（`crp verify` / `crp stage`），但晋级、插件执行、集群分发和 OTA 仍不可用。

在架构设计上，CheeseWAF 将**数据平面（Data Plane）**请求路径与**管理平面（Management Plane）**监听及异步 ALAP 工作分开。当前同一个 `cheesewaf` 进程同时启动这两个监听：数据平面负责有界的同步检测与反向代理，管理平面承载 API、控制台和后台审查 Worker；请求路径不会等待远程大模型。独立的商业化控制面仍是尚未接线的后续组件。

{{% pageinfo color="info" %}}
CheeseWAF 发行包请前往 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 获取。项目完全开源，遵循 [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE) 协议。
{{% /pageinfo %}}

## 核心机制 {#how-it-works}

1. **高性能数据平面检测**：入站请求经多层解码后进入抽象语法树（AST）语义分析引擎，对请求中可能存在的 SQL 注入、跨站脚本（XSS）、命令执行（RCE）等攻击和恶意请求实施毫秒乃至微秒级的阻断。
2. **异步 ALAP 智能研判**：在响应返回客户端后，对于判定边界模糊或嵌入在大段正常文本中的可疑样本，系统将其投递至后台异步审查队列，由配置的大语言模型（兼容 OpenAI / Anthropic 协议）进行深度语义研判。
3. **闭环规则采纳与防御加固**：对模型判定为高危（`high`）或严重（`critical`）的威胁样本，系统支持人工确认或自动采纳。站点级自动采纳会沉淀为该站点的自定义载荷规则；全局 IP 黑名单与客户端软指纹处置仍需操作者明确执行。

## 默认监听平面 {#default-listeners}

CheeseWAF 默认在以下端口提供网络服务：

| 平面类型 | 默认监听地址 | 说明 |
| --- | --- | --- |
| **数据平面** | `http://127.0.0.1:8080` | 接收业务流量，执行同步安全检测并反向代理至上游源站 |
| **管理平面** | `http://127.0.0.1:9443` | 承载 Web 控制台、REST API 及 `/setup` 初始化向导（Docker 环境下默认启用 HTTPS） |
| **集群平面** | `https://127.0.0.1:9444` | `cluster.enabled: true` 时才启用的可选 TLS/mTLS 互联，用于节点身份、健康/心跳、拓扑与编排钩子；不是通用站点/策略复制通道 |
| **本地控制器** | `http://127.0.0.1:17943` | Windows 与 macOS 桌面环境下的本地辅助控制器端口 |

## 文档导航 {#start-here}

{{< nav-cards cols="2" >}}
{{< nav-card title="安装部署" link="/zh/docs/cheesewaf/install/" icon="fa-solid fa-download" desc="涵盖 Linux (systemd)、Docker Compose、Windows 及 macOS 的安装与配置。" />}}
{{< nav-card title="快速上手" link="/zh/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="分步指引：完成系统初始化、接入首个反向代理站点并配置大模型审查。" />}}
{{< nav-card title="核心概念" link="/zh/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="深入解析请求生命周期、防护等级机制、独立与夹杂特征及多端统一权限体系。" />}}
{{< nav-card title="安全防护" link="/zh/docs/cheesewaf/protection/" icon="fa-solid fa-shield" desc="语义分析引擎、自定义正则规则、IP/GeoIP、Bot 挑战、滑动窗口限流与 ACL。" />}}
{{< nav-card title="隔离环境运维" link="/zh/docs/cheesewaf/operations/" icon="fa-solid fa-lock" desc="当前可用的离线校验与存储维护；插件出站、诊断上传和恢复流程仍是设计阶段 contract。" />}}
{{< nav-card title="独立控制面运行时" link="/zh/docs/cheesewaf/control-plane-runtime/" icon="fa-solid fa-server" desc="说明 cheesewaf-control 的当前参数、fail-closed 启动检查、本地探针和 join 模式限制。" />}}
{{< /nav-cards >}}
