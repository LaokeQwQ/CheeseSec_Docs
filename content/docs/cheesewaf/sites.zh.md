---
title: 站点管理与反向代理
linkTitle: 站点
weight: 50
description: 配置业务域名、上游源站负载均衡算法（轮询/加权/IP哈希/最小连接）、健康检查探测及站点专属防护策略。
---

在 CheeseWAF 中，**站点（Site）** 是业务反向代理与安全策略的基本组织单元。一个站点由一组对外绑定的域名（Host）与一个或多个后端上游源站（Upstream）构成。

## 管理与导入方式 {#create}

- **Web 控制台**：进入 **站点管理** 模块进行可视化新增、编辑与策略调试。
- **RESTful API**：支持通过 `GET/POST /api/sites` 与 `GET/PUT/DELETE /api/sites/{id}` 接口进行自动化管理。
- **Nginx 配置导入**：支持调用 `POST /api/nginx/import` 解析并导入现有的 Nginx `server` 块配置。

{{% pageinfo color="info" %}}
**YAML 配置层与 REST API 结构形态说明**：
- **YAML 配置层**（`cheesewaf.yaml`）：上游为对象数组 `upstreams: [{address: "127.0.0.1:8080", weight: 1}]`，支持为节点分配权重；防护配置嵌套在 `waf` 对象中。
- **REST API DTO 层**（`POST /api/sites`）：为扁平结构，`upstreams` 接收字符串数组（如 `["http://127.0.0.1:8080"]`），防护参数扁平铺开为 `waf_enabled`、`waf_mode` 与 `paranoia_level`（权重仅在 YAML 层承载，API 层不携带权重字段）。按 YAML 嵌套形态调用 REST API 会报错。
{{% /pageinfo %}}

## 站点配置字段说明 {#fields}

| 属性名称 | 配置键路径 | 类型与取值说明 |
| --- | --- | --- |
| **站点标识** | `sites[].id` | 站点全局唯一标识字符串 |
| **站点名称** | `sites[].name` | 便于识别的可读名称 |
| **匹配域名** | `sites[].domains` | 字符串数组，用于精确匹配入站 HTTP `Host` 请求头 |
| **上游源站** | `sites[].upstreams[].address` | 后端源站地址（格式为 `主机:端口`），支持配置 `weight` 权重 |
| **独立监听端口** | `sites[].listen_port` | 元数据字段（供 nginx 配置导入与 UI 识别展示；数据面统一由主监听按 Host 域名路由） |
| **负载均衡策略** | `sites[].loadbalance` | 负载均衡算法，支持 `round_robin`、`weighted`、`ip_hash`、`least_conn` |
| **站点启用状态** | `sites[].enabled` | 布尔值，设为 `false` 则暂停该站点的流量转发 |
| **WAF 防护开关** | `sites[].waf.enabled` | 是否对该站点的请求执行安全过滤 |
| **处置模式** | `sites[].waf.mode` | 可选 `block`（拦截阻断）、`monitor`（仅记录模式，亦兼容别名 `log`）或 `off`（关闭） |
| **防护等级** | `sites[].waf.paranoia_level` | 防护等级取值范围 0～5，默认为 3 |
| **语义分析引擎** | `sites[].waf.semantic_engines` | 支持独立开启 `sql`、`xss`、`rce`、`lfi`、`xxe`、`ssrf`、`nosql`、`ssti` |
| **自定义规则** | `sites[].waf.custom_rules` | 站点专属自定义正则规则列表（支持 CLI 与控制台批量导入导出） |
| **路径改写** | `sites[].waf.rewrite` | URI 路径内部静默重写或 HTTP 3xx 重定向规则 |
| **上游健康检查** | `sites[].waf.health_check` | 包含探测路径、检测间隔与健康/不健康阈值 |
| **可信代理网段** | `sites[].waf.access_control.trusted_cidrs` | 前置 CDN 或负载均衡器 CIDR 网段，用于解析真实源 IP |

## 负载均衡算法详解 {#loadbalance}

针对配置了多个后端上游源站的站点，`sites[].loadbalance` 支持以下 4 种负载均衡策略：

1. **`round_robin`（轮询，默认）**：请求依次循环分发给各健康上游节点，适合各源站规格性能一致的标准集群。
2. **`weighted`（加权轮询）**：根据各节点在 `upstreams[].weight` 中配置的权重比例分配请求（例如权重 3:1 时，每 4 个请求分配 3 个至主节点），适合异构服务器部署。
3. **`ip_hash`（客户端源 IP 哈希）**：基于真实客户端源 IP 进行一致性哈希计算，将同一客户端的请求稳定分发至同一后端节点，用于维持服务端本地会话（Session Sticky）。
4. **`least_conn`（最小活跃连接数）**：实时追踪分配至各源站的在途未完成请求数，将新请求动态分发至当前处理中连接数最少的健康节点，有效平抑长耗时请求导致的请求堆积。

## 上游健康检查探测 {#health}

当开启 `health_check.enabled: true` 时，CheeseWAF 会定期向各后端源站发起 HTTP 探测请求（路径由 `health_check.path` 指定）：

- 当源站连续探测失败次数达到 `unhealthy_threshold` 时，该节点将被暂时标记为不健康并移出负载均衡池。
- 当节点恢复正常且连续成功达到阈值后，系统将自动恢复其流量分发。
- 若所有源站均标记为不健康，Fail-Open 仅可对安全重试的空 `GET` 或 `HEAD` 请求回退尝试配置的上游。非幂等方法（如 `POST`、`PUT`）或携带请求体的请求不会被重放。

## 路径重写与重定向 {#rewrites}

路径改写规则支持配置 `pattern`（匹配正则）、`replacement`（替换目标）以及 `redirect_code`：

- **内部静默改写**：当 `redirect_code: 0` 时，系统在转发给源站前在内存中改写 URI 路径，客户端对此无感知。
- **外部重定向**：当 `redirect_code` 设为 `301` 或 `302` 时，直接向客户端返回 HTTP 重定向响应。

## 站点专属自定义规则 {#custom-rules-site}

每个站点均独立维护专属的 `custom_rules` 列表：
- 支持通过 Web 控制台「规则管理」直接编辑或导入导出。
- 支持使用 CLI 工具进行 CI/CD 流水线自动化同步，例如 `export CHEESEWAF_SITE_ID='site-demo'; export CHEESEWAF_RULES_FILE='rules.yaml'; cheesewaf rules import --site "$CHEESEWAF_SITE_ID" --file "$CHEESEWAF_RULES_FILE"`。
- 规则在请求进入 AST 语义分析前（Phase 1 Priority 250）进行评估，可精准阻断特定站点的探测流量。
