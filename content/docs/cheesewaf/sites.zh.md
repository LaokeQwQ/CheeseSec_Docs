---
title: 站点与反向代理
linkTitle: 站点
weight: 50
description: 域名、上游、负载均衡、健康检查，以及每个站点自己的 WAF 开关。
---

一个 **站点** 是一组对外主机名，加上一个或多个源站。
CheeseWAF 站在这些源站前面做反向代理。

## 创建和修改 {#create}

控制台：**站点**。
REST：`GET/POST /api/sites`，`GET/PUT/DELETE /api/sites/{id}`。
也可以用 `POST /api/nginx/import` 导入 Nginx 的 server 块。

## 常用字段 {#fields}

| 字段 | 配置键 | 说明 |
| --- | --- | --- |
| 站点 id | `sites[].id` | 稳定编号，出现在 URL 里 |
| 名称 | `sites[].name` | 显示名 |
| 域名 | `sites[].domains` | 匹配 Host |
| 上游 | `sites[].upstreams[].address` | `主机:端口`，可选 `weight` |
| 监听端口 | `sites[].listen_port` | 可选的额外监听 |
| 负载均衡 | `sites[].loadbalance` | 默认 `round_robin` |
| 启用 | `sites[].enabled` | 关掉就跳过这个站点 |
| 打开 WAF | `sites[].waf.enabled` | |
| 模式 | `sites[].waf.mode` | 一般是 `block` |
| 防护等级 | `sites[].waf.paranoia_level` | 0～5 |
| 引擎 | `sites[].waf.semantic_engines` | `sql`、`xss`、`rce`、`lfi`、`xxe`、`ssrf`、`nosql`、`ssti` |
| 自定义规则 | `sites[].waf.custom_rules` | 在 URI 等位置上的正则 |
| 改写 | `sites[].waf.rewrite` | 路径改写或重定向 |
| 健康检查 | `sites[].waf.health_check` | 路径、间隔、阈值 |
| 可信网段 | `sites[].waf.access_control.trusted_cidrs` | 前面还有一层代理时用来取真实客户端 IP |

## 健康检查 {#health}

`health_check.enabled` 为真时，CheeseWAF 探测每个上游的 `health_check.path`。
连续失败达到 `unhealthy_threshold` 后，这个源站离开池子。

## 路径改写 {#rewrites}

改写规则有 `pattern`、`replacement`，以及可选的 `redirect_code`。
`redirect_code: 0` 表示内部改写。
填 3xx 则把客户端重定向到新路径。

## 站点策略覆盖 {#policy}

`sites[].waf.protection_policy` 可以覆盖全局 `protection.policy` 里的键：

- `web_attack`
- `api_security`
- `bot_cc`
- `threat_intel`

空字符串继承全局值（示例里是 `smart`）。
