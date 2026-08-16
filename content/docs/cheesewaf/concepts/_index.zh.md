---
title: 核心概念
linkTitle: 概念
weight: 40
description: 深入解析流量处理生命周期、防护等级判定、特征隔离机制及多端统一管理体系。
---

本章详细介绍 CheeseWAF 的核心架构设计与检测判定原理。在调整生产环境防护等级或定制安全策略之前，建议深入了解以下机制：

{{< nav-cards cols="2" >}}
{{< nav-card title="流量处理路径" link="/zh/docs/cheesewaf/concepts/pipeline/" icon="fa-solid fa-route" desc="了解入站请求经过的网络层、访问控制、语义检测及异步 ALAP 的完整流转生命周期。" />}}
{{< nav-card title="防护等级机制" link="/zh/docs/cheesewaf/concepts/paranoia/" icon="fa-solid fa-layer-group" desc="详解 0～5 级防护等级定义、降误报策略以及基于时间窗口的动态临时升档机制。" />}}
{{< nav-card title="独立特征与夹杂特征" link="/zh/docs/cheesewaf/concepts/isolated-embedded/" icon="fa-solid fa-code" desc="区分独立攻击载荷与嵌入在长文本中的夹杂特征，理解针对 Gadget 的精准隔离保护。" />}}
{{< nav-card title="统一管理入口" link="/zh/docs/cheesewaf/concepts/management/" icon="fa-solid fa-table-columns" desc="了解 Web 控制台、TUI 命令行与 REST API 共享的 RBAC 鉴权与会话审计模型。" />}}
{{< /nav-cards >}}
