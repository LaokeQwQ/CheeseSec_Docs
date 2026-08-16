---
title: 站点管理与反向代理
linkTitle: 站点
weight: 50
description: 配置业务域名、上游源站负载均衡、健康检查探测、路径重写及站点专属防护策略。
---

在 CheeseWAF 中，**站点（Site）** 是业务反向代理与安全策略的基本组织单元。一个站点由一组对外绑定的域名（Host）与一个或多个后端上游源站（Upstream）构成。

## 管理与导入方式 {#create}

- **Web 控制台**：进入 **站点管理** 模块进行可视化新增、编辑与策略调试。
- **RESTful API**：支持通过 `GET/POST /api/sites` 与 `GET/PUT/DELETE /api/sites/{id}` 接口进行自动化管理。
- **Nginx 配置导入**：支持调用 `POST /api/nginx/import` 解析并导入现有的 Nginx `server` 块配置。

## 站点配置字段说明 {#fields}

| 属性名称 | 配置键路径 | 类型与取值说明 |
| --- | --- | --- |
| **站点标识** | `sites[].id` | 站点全局唯一标识字符串 |
| **站点名称** | `sites[].name` | 便于识别的可读名称 |
| **匹配域名** | `sites[].domains` | 字符串数组，用于精确匹配入站 HTTP `Host` 请求头 |
| **上游源站** | `sites[].upstreams[].address` | 后端源站地址（格式为 `主机:端口`），支持配置 `weight` 权重 |
| **独立监听端口** | `sites[].listen_port` | 可选配置，为该站点分配独立的监听端口 |
| **负载均衡策略** | `sites[].loadbalance` | 负载均衡算法，默认为轮询 `round_robin` |
| **站点启用状态** | `sites[].enabled` | 布尔值，设为 `false` 则暂停该站点的流量转发 |
| **WAF 防护开关** | `sites[].waf.enabled` | 是否对该站点的请求执行安全过滤 |
| **处置模式** | `sites[].waf.mode` | `block`（拦截模式）或 `log`（仅记录模式） |
| **防护等级** | `sites[].waf.paranoia_level` | 防护等级取值范围 0～5，默认为 3 |
| **语义分析引擎** | `sites[].waf.semantic_engines` | 支持独立开启 `sql`、`xss`、`rce`、`lfi`、`xxe`、`ssrf`、`nosql`、`ssti` |
| **自定义规则** | `sites[].waf.custom_rules` | 站点级自定义正则匹配规则列表 |
| **路径改写** | `sites[].waf.rewrite` | URI 路径内部重写或 HTTP 3xx 重定向规则 |
| **上游健康检查** | `sites[].waf.health_check` | 包含探测路径、检测间隔与健康/不健康阈值 |
| **可信代理网段** | `sites[].waf.access_control.trusted_cidrs` | 前置 CDN 或负载均衡器 CIDR 网段，用于解析真实源 IP |

## 上游健康检查探测 {#health}

当开启 `health_check.enabled: true` 时，CheeseWAF 会定期向各后端源站发起 HTTP 探测请求（路径由 `health_check.path` 指定）：

- 当源站连续探测失败次数达到 `unhealthy_threshold` 时，该节点将被暂时标记为不健康并移出负载均衡池。
- 当节点恢复正常且连续成功达到阈值后，系统将自动恢复其流量分发。

## 路径重写与重定向 {#rewrites}

路径改写规则支持配置 `pattern`（匹配正则）、`replacement`（替换目标）以及 `redirect_code`：

- **内部静默改写**：当 `redirect_code: 0` 时，系统在转发给源站前在内存中改写 URI 路径，客户端对此无感知。
- **外部重定向**：当 `redirect_code` 设为 `301` 或 `302` 时，直接向客户端返回 HTTP 重定向响应。

## 站点级防护策略覆盖 {#policy}

通过 `sites[].waf.protection_policy` 可覆盖全局 `protection.policy` 的预设策略：

- `web_attack`：Web 应用通用攻击防护策略
- `api_security`：API 接口安全策略
- `bot_cc`：Bot 与防刷防护策略
- `threat_intel`：威胁情报协同策略

若字段值留空，站点将自动继承全局策略基线（系统预设为 `smart`）。
