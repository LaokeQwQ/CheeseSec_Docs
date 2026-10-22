---
title: CheeseSec 官方文档
linkTitle: 首页
description: CheeseSec 旗下安全产品官方手册与工程实践指南，涵盖我司发行产品的部署、配置与运维。
cascade:
  type: docs
no_list: true
---

欢迎查阅 CheeseSec 官方产品手册。本站提供旗下产品与服务的架构设计说明、部署指引、安全防护配置及生产运维手册。

本站分别收录 **CheeseWAF** 和 **CheeseSec 插件**两个独立产品的文档。插件体系面向整个 CheeseSec 生态，具体支持的宿主和版本以插件说明为准。

CheeseWAF 的源码与预编译分发包托管于 [CheeseWAF 仓库](https://github.com/LaokeQwQ/CheeseWAF)，遵循 [Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE) 开源协议。

## 产品矩阵 {#cheesewaf}

{{< nav-cards cols="2" >}}
{{< nav-card title="CheeseWAF" link="/zh/docs/cheesewaf/" icon="fa-solid fa-shield-halved" desc="企业级自托管 Web 应用防火墙。提供语义分析、Bot 防护、API 安全及异步大模型审查能力。" />}}
{{< nav-card title="CheeseSec 插件" link="/zh/docs/plugins/" iconImage="/images/plugins-logo.svg" desc="面向 CheeseSec 生态的独立插件产品，提供开发、签名校验、发布与分发体系，宿主兼容性以插件说明为准。" />}}
{{< /nav-cards >}}

## 快速导航 {#start}

| 操作场景 | 推荐文档 |
| --- | --- |
| 快速部署与基础运行 | [系统安装](/zh/docs/cheesewaf/install/) · [快速上手](/zh/docs/cheesewaf/tutorial/) |
| 核心架构与流量机制 | [产品架构介绍](/zh/docs/cheesewaf/intro/) · [核心概念解析](/zh/docs/cheesewaf/concepts/) |
| 业务接入与防护策略 | [站点与反向代理](/zh/docs/cheesewaf/sites/) · [安全防护策略](/zh/docs/cheesewaf/protection/) |
| 系统集成与参数参考 | [REST API 接口](/zh/docs/cheesewaf/api/) · [配置文件参考](/zh/docs/cheesewaf/config/) |
| 插件开发与发布 | [插件手册](/zh/docs/plugins/) · [插件商店](https://store.cheesesec.com/) |
