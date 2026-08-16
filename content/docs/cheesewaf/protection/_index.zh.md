---
title: 安全防护策略
linkTitle: 防护
weight: 60
description: 涵盖 AST 语义分析引擎、自定义正则规则、IP/GeoIP、Bot 挑战验证、令牌桶限流、ACL 与拦截页配置。
---

CheeseWAF 构建了从网络接入层到应用语义层的多维度防御体系。全局防护基线由主配置文件中的 `protection` 与 `protection.policy` 定义，同时支持在各业务站点（`sites[].waf.protection_policy`）中按需覆盖。

{{< nav-cards cols="2" >}}
{{< nav-card title="语义分析引擎" link="/zh/docs/cheesewaf/protection/semantic/" desc="多层递归解码、AST 语法树构建及各专项语义引擎配置与分析预算控制。" />}}
{{< nav-card title="自定义规则" link="/zh/docs/cheesewaf/protection/custom-rules/" desc="基于正则表达式的 URI、请求头及参数匹配规则，支持优先级与威胁等级管理。" />}}
{{< nav-card title="IP、地理位置与指纹" link="/zh/docs/cheesewaf/protection/ip-geo-fingerprint/" desc="IP 白名单、黑名单、GeoIP 国家/地区封禁、威胁情报源同步与客户端软指纹识别。" />}}
{{< nav-card title="Bot 挑战与验证码" link="/zh/docs/cheesewaf/protection/bot-captcha/" desc="无感 JS 挑战、PoW（Altcha）、交互式滑块/图形验证码及排队室流量削峰机制。" />}}
{{< nav-card title="流量限流" link="/zh/docs/cheesewaf/protection/ratelimit/" desc="数据平面高性能令牌桶限流算法与超出阈值后的排队/阻断策略。" />}}
{{< nav-card title="访问控制列表（ACL）" link="/zh/docs/cheesewaf/protection/acl/" desc="基于 HTTP 请求方法、路径前缀及特定请求头的快速放行与阻断规则。" />}}
{{< nav-card title="拦截响应页" link="/zh/docs/cheesewaf/protection/block-page/" desc="内置现代拦截页模板、自定义 HTML 上传及请求追踪编号（Trace ID）展示。" />}}
{{< /nav-cards >}}
