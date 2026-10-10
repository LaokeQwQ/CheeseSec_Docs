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

## 为什么选择 CheeseWAF {#why-cheesewaf}

市面上常见的 Web 安全防护方案通常面临几个痛点：
1. **传统正则 WAF（如 ModSecurity / CRS 规则集）**：靠维护成千上万条正则表达式防守。攻击者通过大小写变异、畸形 URL 编码或特殊注释很容易绕过；同时误报率高，日常运维需要大量写白名单，改一条规则要反复调试。
2. **直接调大模型的实验性 WAF**：每个 HTTP 请求都同步等待大模型返回，网页延迟直接飙升 500 ms 到 2 s，不仅拖慢业务，还极易刷爆 API 费用；一旦外部大模型网络抖动或超时，业务直接瘫痪。
3. **重型容器全家桶（如雷池 SafeLine 等）**：通常需要启动 5 到 10 个 Docker 容器（Tengine、Postgres、Redis 等），常驻内存 1～2 GB 起步，低配轻量云主机或 VPS 难以承受。
4. **商业云 WAF（如 Cloudflare / 云厂商高防）**：所有业务流量必须穿透第三方公网云节点，存在数据合规与隐私出境风险；按流量计费成本不可控，无法在纯离线内网部署。

CheeseWAF 的思路是：**用自研 AST 语法树做毫秒级即时拦截，大模型只在后台异步值守存疑流量，既没有正则的误报和绕过，也不增加线上任何延迟，极简轻量开箱即用。**

### 方案对比

| 对比维度 | 传统正则 WAF (如 ModSecurity) | 同步大模型 WAF | 重型容器全家桶 (如雷池) | 商业云 WAF (如 Cloudflare) | CheeseWAF |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **检测技术** | 正则特征匹配 | 每次请求同步调用大模型 | 正则 + 统计/语义分析 | 规则库 + 威胁情报 | **AST 语法分析 + 异步大模型值守 (ALAP)** |
| **请求额外延迟** | 1～10 ms | **500～2000 ms**（极高） | 2～15 ms | 取决于云节点网络 | **< 1 ms**（毫秒级阻断，0 模型等待） |
| **Token / API 成本** | 无 | 极高（全量请求计费） | 无 | 按流量计费 | **低（仅异步复核存疑样本）** |
| **抗混淆与误报** | 易被编码绕过，误报多 | 存在模型幻觉 | 规则复杂，维护成本高 | 依赖厂商情报更新 | **解析语法树，防混淆，误报率 < 0.8%** |
| **资源与部署成本** | 需配置编译 Nginx 模块 | 依赖外部 API | 需 5～10 个容器，内存 1～2 GB+ | 商业订阅计费 | **单二进制/单容器，内置 SQLite，内存几十 MB 起** |
| **现有架构侵入性** | 绑定特定 Web 服务 | 强制修改反代路径 | 通常需替换主网关 | 修改域名 DNS 接入 | **既能独立反代，也可通过 Sidecar 旁挂现有网关** |
| **数据与隐私合规** | 本地运行 | 业务流量全文发往外部 API | 本地运行 | 流量经过第三方公网节点 | **流量留在本地；大模型仅复核存疑样本，支持内网私有模型** |
| **网络隔离支持** | 支持离线 | 无法离线（依赖外部模型） | 部分支持 | 不支持（依赖云服务） | **支持完全离线运行与 CRP 离线签名验签** |

## 核心机制 {#how-it-works}

1. **高性能数据平面检测**：入站请求经多层解码后进入抽象语法树（AST）语义分析引擎，对请求中可能存在的 SQL 注入、跨站脚本（XSS）、命令执行（RCE）等攻击和恶意请求实施毫秒乃至微秒级的阻断。
2. **异步 ALAP 智能研判**：在响应返回客户端后，对于判定边界模糊或嵌入在大段正常文本中的可疑样本，系统将其投递至后台异步审查队列，由配置的大语言模型（兼容 OpenAI Response / Chat Completions 协议与 Anthropic Messages 协议）进行深度语义研判。
3. **闭环规则采纳与防御加固**：对模型判定为高危（`high`）或严重（`critical`）的威胁样本，系统支持人工确认或自动采纳。站点级自动采纳会沉淀为该站点的自定义载荷规则；全局 IP 黑名单与客户端软指纹处置仍需操作者明确执行。

## 默认监听平面 {#default-listeners}

CheeseWAF 默认在以下端口提供网络服务：

| 平面类型 | 默认监听地址 | 说明 |
| --- | --- | --- |
| **数据平面** | `http://127.0.0.1:8080` | 接收业务流量，执行同步安全检测并反向代理至上游源站 |
| **管理平面** | `https://PUBLIC_IP:9443/setup` → `https://PUBLIC_IP:9443/SECURITY_ENTRY` | 初始化固定使用 `/setup` 和一次性 Token；完成后访问无符号安全入口，由入口签发 Cookie 并跳转登录 |
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
