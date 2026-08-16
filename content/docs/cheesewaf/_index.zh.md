---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: 自托管的 Web 应用防火墙。安装、配置和运维手册。
---

CheeseWAF 是自托管的 Web 应用防火墙。
它以单个 Go 二进制发布，内置 SQLite、Web 控制台、命令行和 REST 管理接口。

数据平面检查请求后回源。
它不会在每个请求上同步调用大语言模型。
响应返回后，可选的 ALAP 队列再审查可疑样本。

{{% pageinfo color="info" %}}
发行包在 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases)。
项目使用 [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE)。
{{% /pageinfo %}}

## 工作方式 {#how-it-works}

1. **数据平面。** 参数先解码，再做语法分析。能确定的 SQL 注入、XSS、命令执行可以立即阻断。
2. **ALAP。** 响应已经返回后，边界模糊或夹杂在长文本里的样本进入后台队列。可以对接兼容 OpenAI 协议的模型。
3. **审查结果。** 判定为 `high` 或 `critical` 的样本，打开自动采纳后，可以写成长期的 IP、指纹或特征规则。

ALAP 是 **AI Large-Language-Model Auto Pilot** 的缩写。

## 默认监听 {#default-listeners}

| 平面 | 默认地址 | 作用 |
| --- | --- | --- |
| 数据平面 | `http://127.0.0.1:8080` | 接收站点流量，检测后回源 |
| 管理平面 | `http://127.0.0.1:9443` | Web 控制台、REST API、初始化向导。Docker 默认走 HTTPS |
| 集群平面 | `http://127.0.0.1:9444` | 集群模式下的节点同步 |
| 本地控制器 | `http://127.0.0.1:17943` | 仅 Windows / macOS 桌面控制器使用 |

## 从这里开始 {#start-here}

{{< nav-cards cols="2" >}}
{{< nav-card title="安装" link="/zh/docs/cheesewaf/install/" icon="fa-solid fa-download" desc="Linux、Docker、Windows、macOS。" />}}
{{< nav-card title="快速上手" link="/zh/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="初始化、加站点、接模型。" />}}
{{< nav-card title="概念" link="/zh/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="流量路径、防护等级、独立特征与夹杂特征。" />}}
{{< nav-card title="防护" link="/zh/docs/cheesewaf/protection/" icon="fa-solid fa-shield" desc="语义引擎、IP、Bot、限流、ACL。" />}}
{{< /nav-cards >}}
