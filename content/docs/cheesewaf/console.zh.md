---
title: Web 管理控制台
linkTitle: 控制台
weight: 140
description: 现代化 React 管理控制台功能导航、模块路由映射与安全交互机制。
---

CheeseWAF 内置了基于 React 构建的单页可视化管理控制台，由 `cheesewaf` 进程的管理监听器直接托管。完成 [系统初始化](../tutorial/setup/) 后，请访问配置的管理地址。独立部署可按配置使用 HTTP/HTTPS；官方 Docker Compose 将管理端以 HTTPS 绑定在 Docker 宿主机回环地址，因此应在宿主机打开 `https://127.0.0.1:9443/`（或使用 SSH 隧道），除非明确修改绑定，否则不要使用远程主机地址。

控制台采用基于 Session Cookie 的状态保持与严格的 CSRF 双重防御机制（HTTP 环境自动自适应，HTTPS 下强制启用 Secure 属性），并支持在登录页启用 [人机验证码防护](../protection/bot-captcha/#login)。

## 控制台路由与手册对照表 {#pages}

| 控制台前端路由 | 功能定位与模块说明 | 对应文档参考 |
| --- | --- | --- |
| `/` | 仪表盘：实时 QPS、阻断统计与威胁态势卡片 | [监控与日志](../monitor/) |
| `/sites` | 站点管理：域名绑定、源站上游、4 种负载均衡策略与健康检查 | [站点管理](../sites/) |
| `/ssl` | SSL 证书：管理证书上传与 ACME 自动化申请 | [TLS 与证书](../tls/) |
| `/rules` | 规则管理：站点专属正则规则配置，支持 YAML/JSON 批量导入导出与 RE2 实时语法校验 | [自定义规则](../protection/custom-rules/) |
| `/review` | 威胁审查：ALAP 异步分析样本研判、决策索赔与规则沉淀 | [ALAP 异步审查](../alap/) |
| `/logs` | 日志检索：请求 Trace ID 追溯与多维日志过滤 | [监控与日志](../monitor/) |
| `/ip` | IP 管理：IP 黑白名单、GeoIP 封禁与情报同步 | [IP、地理与指纹](../protection/ip-geo-fingerprint/) |
| `/protection` | 防护配置：AST 语义引擎开关与策略基线调整 | [安全防护策略](../protection/) |
| `/bot-challenge` | Bot 挑战：JS 挑战、滑块验证码与排队室策略 | [Bot 与验证码](../protection/bot-captcha/) |
| `/edge` | 边缘优化：响应头改写、静态缓存与压缩规则 | [边缘特性](../edge/) |
| `/ai` | AI 配置：大模型连接参数、自学习任务与自动化采纳设置 | [ALAP 异步审查](../alap/) |
| `/monitor` | 监控告警：Prometheus 导出、Remote Write 与 Webhook 通知器 | [监控与日志](../monitor/) |
| `/apisec` | API 安全：接口发现、Schema 校验与路由限流 | [API 接口安全](../api-security/) |
| `/users` | 用户管理：管理员账号、角色划分与 2FA/TOTP 维护 | [系统运维](../operations/) |
| `/ops` | 运维调度：自动化任务调度与日志清理维护 | [存储与调度](../storage/) |
| `/updates` | 检查更新：查看 OTA 预留配置的能力状态；当前更新器不可用 | [系统运维](../operations/) |
| `/block-pages` | 拦截页面：拦截页模板管理、HTML 安全清洗与沙箱预览 | [拦截响应页](../protection/block-page/) |
| `/attack-map` | 攻击大屏：实时全球攻击态势大屏、内置规范中国国界线与 100% 纯离线 3D 地球 | [监控与日志](../monitor/) |
| `/cluster` | 集群管理：节点状态、加入令牌、证书轮换、Ansible 引导包导出和编排任务查看；共享集群后端与远端 Worker 尚未接线 | [集群高可用](../cluster/) |
| `/system` | 系统配置：运行时参数、NTP 同步与备份能力状态；当前备份/还原 API 返回 501 | [系统运维](../operations/) |
| `/captcha-lab` | 验证码实验室：人机挑战题型调试与素材定制 | [Bot 与验证码](../protection/bot-captcha/) |

控制台内置了浅色、深色及多套主题色系，个性化配置仅在浏览器本地生效，不会对数据平面的请求转发造成任何影响。
