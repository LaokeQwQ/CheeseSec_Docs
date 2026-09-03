---
title: 流量处理路径与两阶段流水线
linkTitle: 流量路径
weight: 10
description: 深度解析同步检测转发链路的两阶段流水线架构（Pre-Filters 预筛选 + 语义 Worker 线程池）与响应交付后的异步 ALAP 旁路研判链路。
---

CheeseWAF 的流量处理链路分为**同步检测链路**与**异步旁路研判链路**两大部分。系统在同步链路中采用了独特的**两阶段流水线（Two-Phase Pipeline）**架构，兼顾极端高并发下的微秒级快速阻断与复杂语法树解析的高吞吐：

```mermaid
flowchart TB
  Client[客户端请求] --> Ingress[网络接入层 HTTP / HTTPS / HTTP3]
  subgraph Phase1 [Phase 1: 预筛选器链 Pre-Filters (顺序执行 / 短路阻断 / 优先级 < 290)]
    IP{IP / 地理位置 / 软指纹} -->|放行| Bot{Bot 挑战 / 限流 / 排队室}
    Bot -->|放行| Rules{自定义规则引擎 Priority 250}
  end
  Ingress --> IP
  IP -->|命中黑名单| Block[返回拦截页]
  Bot -->|触发挑战| Challenge[验证码校验 / 排队等待]
  Challenge -->|挑战通过| Rules
  Rules -->|命中阻断规则| Block

  subgraph Phase2 [Phase 2: 语义分析组 Semantic Group (Worker 线程池并发 / 确定性合并 / 优先级 >= 290)]
    Sem[AST 语义分析引擎: SQL / XSS / RCE / LFI / NoSQL / SSTI 等]
  end
  Rules -->|无阻断| Sem

  Sem --> Shape{特征形态判断}
  Shape -->|独立特征 2~5 级| Block
  Shape -->|夹杂特征 5 级| Block
  Shape -->|夹杂特征 2~4 级| Pass[放行并投递异步队列]
  Shape -->|无异常| Origin[转发至上游源站]
  Pass --> Origin
  Pass -.-> Queue[ALAP 异步审查队列]
  Sem -.->|5 级阻断样本| Queue
  Queue --> LLM[调用配置的大语言模型]
  LLM --> Review{研判判定}
  Review -->|高危 / 严重| Rule[沉淀为长期规则]
  Review -->|低危 / 误报| Dismiss[归档忽略 / 加入白名单]
  Rule -.-> IP
```

## 两阶段流水线设计（Phase 1 与 Phase 2） {#two-phase-pipeline}

为了在生产高流量下保障服务时延确定性，CheeseWAF 的请求检测流水线在内存中将所有注册的检测器按 `Priority` 分离为两个截然不同的执行阶段：

### 1. Phase 1：Pre-Filters 顺序预筛选器（优先级 < 290）

- **涵盖范围**：IP 黑白名单与地理围栏、Bot 挑战与防刷识别、令牌桶限流，以及 **自定义正则规则引擎（Priority 250）**。
- **执行特性**：单线程**顺序执行**，对执行顺序极度敏感。
- **快速短路机制**：任意前置检测器判定为 `ActionBlock` 时，请求将立即被短路拦截并终止流水线，**绝对不进入昂贵的 AST 语法树解析阶段**。这使得针对已知敏感路径、特定扫描特征的大规模扫描流量在毫秒级内被拦截丢弃。

### 2. Phase 2：Semantic Group 并发语义分析组（优先级 >= 290）

- **涵盖范围**：SQL 注入、XSS 跨站脚本、RCE 命令注入、LFI 文件遍历、NoSQL 注入、SSTI 模板注入、SSRF 以及 XXE 等深层语法分析器。
- **执行特性**：
  - **Worker 协程池并发调度**：系统维护全局共享的 Worker 协程池（上限为 8 协程），入站请求将各项语义分析任务并发推入任务队列并行分析。
  - **请求上下文隔离（Forked Context）**：每个检测器在独立的 Fork 上下文中运行，向元数据和检测结果写入数据时互不干扰，在架构上杜绝并发数据竞争（Data Race）。
  - **确定性优先级合并**：所有并发检测器执行完成（或超时）后，系统严格按照既定的优先级序号执行稳定合并，确保威胁评估结果与日志记录在任何并发环境下均保持 100% 幂等。

## 流水线超时与预算控制（Budget Protection） {#budget-protection}

- **100ms 硬超时防线**：整个流水线设有全局 100ms 硬超时时钟，防止复杂畸形载荷将 WAF 进程长时间卡死。
- **分析预算耗尽策略（`budget_exhausted_policy`）**：当请求体异常巨大或语法树分析在超时窗口内未能完整结束时，系统将触发安全兜底策略：
  - `auto`：遵循站点的全局防护处置模式。
  - `block`：预算耗尽时一律以安全为先予以阻断。
  - `pass`：以业务可用性为先予以放行。
  - `challenge`：引导客户端完成人机验证码校验。
- **过载保护（Guard Overload）**：底层内置基于协程管程与信号量的过载防护，当极端并发导致分析队列溢出时主动触发 `ErrDetectionOverload`，保障主服务进程的高可用与自愈。

## 异步旁路研判链路（ALAP Loop） {#async-path}

异步链路完全独立于实时转发流程，在客户端完成响应接收后于后台触发：

- **样本投递**：在防护等级 2～4 下被放行的夹杂特征样本，以及在等级 5 下被阻断的高危样本，均会被投递至 ALAP 审查队列。
- **模型智能分析**：后台 Worker 异步调用大模型提取攻击意图并输出置信度评估。
- **闭环规则沉淀**：判定为高危（`high`）或严重（`critical`）的威胁，可通过人工审核或自动采纳机制，实时回写为 IP 黑名单或自定义特征规则，实现自适应安全加固。

{{% pageinfo color="info" %}}
各过滤器的具体配置参数请参考 [安全防护](../../protection/)；关于如何配置大模型分析请参考 [ALAP 异步审查](../../alap/)。
{{% /pageinfo %}}
