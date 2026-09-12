---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: 商用级自托管 Web 应用防火墙。提供系统部署、安全防护、配置参考及运维管理手册。
---

CheeseWAF 是基于 Go 语言构建的商用级自托管 Web 应用防火墙（WAF）。系统采用数据平面与管理平面解耦的双平面架构，运行时内置轻量级持久化存储保存管理状态，并支持扩展 PostgreSQL 作为高性能异步访问日志存储。

在架构设计上，CheeseWAF 将**数据平面（Data Plane）**请求路径与**管理平面（Management Plane）**及异步 ALAP 审查流程彻底解耦。同一个 `cheesewaf` 进程内启动两个监听平面：数据平面负责有界、低延迟的同步检测与反向代理；管理平面承载管理 API、控制台界面与后台威胁审查队列，实时请求路径绝不阻塞等待远程大模型分析。

{{% pageinfo color="info" %}}
CheeseWAF 发行包请前往 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 获取。项目完全开源，遵循 [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE) 协议。
{{% /pageinfo %}}

## 核心机制 {#how-it-works}

1. **高性能数据平面检测**：入站请求经多层解码后进入抽象语法树（AST）语义分析引擎，对请求中可能存在的 SQL 注入、跨站脚本（XSS）、命令执行（RCE）等攻击和恶意请求实施毫秒乃至微秒级的阻断。
2. **异步 ALAP 智能研判**：在响应返回客户端后，对于判定边界模糊或嵌入在大段正常文本中的可疑样本，系统将其投递至后台异步审查队列，由配置的大语言模型（兼容 OpenAI Response / Chat Completions 协议与 Anthropic Messages 协议）进行深度语义研判。
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
{{< nav-card title="网关适配器" link="/zh/docs/cheesewaf/adapters/" icon="fa-solid fa-network-wired" desc="面向 NGINX 与 Envoy 的自托管 Go 适配器（adapterd），实现低耦合流量接入与安全熔断。" />}}
{{< nav-card title="插件与 CRP" link="/zh/docs/cheesewaf/plugins/" icon="fa-solid fa-puzzle-piece" desc="CRP v1 离线资源包规范、Ed25519 多方验签、内容寻址暂存及临时出站审计。" />}}
{{< nav-card title="隔离环境运维" link="/zh/docs/cheesewaf/operations/" icon="fa-solid fa-lock" desc="离线环境下的包完整性校验、本地存储维护以及受限网络条件下的运维管理指南。" />}}
{{< nav-card title="独立控制面运行时" link="/zh/docs/cheesewaf/control-plane-runtime/" icon="fa-solid fa-server" desc="说明 cheesewaf-control 的启动参数、安全验证检查、本地探针与接入模式。" />}}
{{< nav-card title="开发者想说" link="/zh/docs/cheesewaf/developer-words/" icon="fa-solid fa-heart" desc="关于 CheeseWAF 的研发初衷、设计哲学与创作者自述。" />}}
{{< /nav-cards >}}
