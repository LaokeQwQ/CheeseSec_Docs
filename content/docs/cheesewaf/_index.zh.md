---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: 企业级自托管 Web 应用防火墙。提供系统部署、安全防护、配置参考及运维管理手册。
---

CheeseWAF 是一款企业级自托管 Web 应用防火墙（WAF），采用单 Go 二进制分发，内置无 CGO 依赖的 SQLite 存储、现代化 Web 控制台、交互式 TUI 命令行工具以及完整的 RESTful 管理接口，开箱即用且无需外部数据库或代理组件。

在架构设计上，CheeseWAF 实现了**数据平面（Data Plane）与控制平面（Control Plane）的分离**。数据平面负责毫秒级同步流量检测与反向代理，杜绝在实时转发链路中同步调用大语言模型引入不可控时延；控制平面则通过异步 ALAP（AI Large-Language-Model Auto Pilot）机制对可疑请求进行旁路智能研判与规则自学习。

{{% pageinfo color="info" %}}
CheeseWAF 发行包请前往 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 获取。项目完全开源，遵循 [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE) 协议。
{{% /pageinfo %}}

## 核心机制 {#how-it-works}

1. **高性能数据平面检测**：入站请求经多层解码后进入抽象语法树（AST）语义分析引擎，对明确的 SQL 注入、跨站脚本（XSS）、命令执行（RCE）等攻击实施当场毫秒级阻断。
2. **异步 ALAP 智能研判**：在响应返回客户端后，对于判定边界模糊或嵌入在大段正常文本中的可疑样本，系统将其投递至后台异步审查队列，由配置的大语言模型（兼容 OpenAI / Anthropic 协议）进行深度语义研判。
3. **闭环规则采纳与防御加固**：对模型判定为高危（`high`）或严重（`critical`）的威胁样本，系统支持人工确认或自动采纳，将其沉淀为长期的 IP 黑名单、软指纹或特征规则。

## 默认监听平面 {#default-listeners}

CheeseWAF 默认在以下端口提供网络服务：

| 平面类型 | 默认监听地址 | 说明 |
| --- | --- | --- |
| **数据平面** | `http://127.0.0.1:8080` | 接收业务流量，执行同步安全检测并反向代理至上游源站 |
| **管理平面** | `http://127.0.0.1:9443` | 承载 Web 控制台、REST API 及 `/setup` 初始化向导（Docker 环境下默认启用 HTTPS） |
| **集群平面** | `http://127.0.0.1:9444` | 集群高可用模式下的节点间通信与状态同步 |
| **本地控制器** | `http://127.0.0.1:17943` | Windows 与 macOS 桌面环境下的本地辅助控制器端口 |

## 文档导航 {#start-here}

{{< nav-cards cols="2" >}}
{{< nav-card title="安装部署" link="/zh/docs/cheesewaf/install/" icon="fa-solid fa-download" desc="涵盖 Linux (systemd)、Docker Compose、Windows 及 macOS 的安装与配置。" />}}
{{< nav-card title="快速上手" link="/zh/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="分步指引：完成系统初始化、接入首个反向代理站点并配置大模型审查。" />}}
{{< nav-card title="核心概念" link="/zh/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="深入解析请求生命周期、防护等级机制、独立与夹杂特征及多端统一权限体系。" />}}
{{< nav-card title="安全防护" link="/zh/docs/cheesewaf/protection/" icon="fa-solid fa-shield" desc="语义分析引擎、自定义正则规则、IP/GeoIP、Bot 挑战、令牌桶限流与 ACL。" />}}
{{< /nav-cards >}}
