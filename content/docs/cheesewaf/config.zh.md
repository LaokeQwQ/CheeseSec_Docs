---
title: 配置文件参考
linkTitle: 配置
weight: 170
description: cheesewaf.yaml 主配置文件结构导航、顶层键解析、超时控制与热重载范围说明。
---

CheeseWAF 在首次启动时会在运行数据目录的 `config/` 目录下自动生成 `cheesewaf.yaml` 主配置文件（默认 `./data/config/cheesewaf.yaml`）。预设配置模板可参考源码库中的 [`configs/cheesewaf.yaml`](https://github.com/LaokeQwQ/CheeseWAF/blob/dev/configs/cheesewaf.yaml)。

`configs/cheesewaf.yaml` 是源码模板，不是运行时状态文件。初始化、站点管理和控制台保存操作会写入运行时配置；源码构建时请先复制到 `./data/config/cheesewaf.yaml` 或其他明确的数据目录，避免把数据库路径、证书、密钥和站点变更写回 Git 工作区中的模板。

## 顶层配置块索引 {#top-level-keys}

| 顶层配置键 | 功能模块与定位 | 详细参考章节 |
| --- | --- | --- |
| `server` | 基础网络监听、管理端口与网络层超时 | [架构介绍](../intro/) · [TLS 与证书](../tls/) |
| `tls` | 数据平面 TLS/HTTPS 证书与 HSTS 配置 | [TLS 与证书](../tls/) |
| `setup` | 初始化状态与运行时数据目录定义 | [系统初始化](../tutorial/setup/) · [存储与调度](../storage/) |
| `deployment` / `cluster` | 部署形态（单机/集群）与高可用协同参数 | [集群高可用](../cluster/) |
| `console` | Web 控制台个性化与管理端登录安全 | [Bot 与验证码](../protection/bot-captcha/) · [监控与日志](../monitor/) |
| `sites` | 业务反向代理站点、域名与上游配置 | [站点管理](../sites/) |
| `protection` | 全局安全基线（语义引擎、IP、Bot、限流等） | [安全防护策略](../protection/) |
| `block_page` | 阻断拦截页模板与自定义响应 HTML 清洗 | [拦截响应页](../protection/block-page/) |
| `storage` | `temporary` SQLite 管理存储；预留但当前会拒绝的 `production` 配置；可选外部日志 Sink | [存储与调度](../storage/) |
| `logging` | 访问日志输出级别、格式与文件轮转 | [监控与日志](../monitor/) |
| `ai` | ALAP 大语言模型连接与异步研判参数 | [ALAP 异步审查](../alap/) |
| `update` | OTA 预留配置；当前运行时尚未实现更新 Worker | [系统运维](../operations/) |
| `scheduler` | 自动化清理、配置快照与定时报表任务调度器；配置快照不是完整数据库导出 | [存储与调度](../storage/) |
| `edge` | 边缘响应头注入、静态缓存与 Gzip/Brotli 压缩 | [边缘特性](../edge/) |
| `monitor` | Prometheus 指标导出、Remote Write 与告警通知器 | [监控与日志](../monitor/) |
| `apisec` | API 资产发现、Schema 校验与 RBAC 权限矩阵 | [API 接口安全](../api-security/) |
| `performance` | Go 运行时垃圾回收（GC）自适应调优（`memory_limit_ratio` / `min_gogc`） | [架构介绍](../intro/) |
| `time_sync` | NTP 时间同步服务器与时钟偏差共识算法配置 | [监控与日志](../monitor/) |
| `captcha_assets` | 验证码自定义背景图与点选图标静态资源目录 | [Bot 与验证码](../protection/bot-captcha/) |
| `acme` | ACME 自动化证书签发与 DNS 认证提供商配置 | [TLS 与证书](../tls/) |
| `vulnerability` | 漏洞预警情报源订阅配置 | [系统运维](../operations/) |

## 超时机制配置 {#timeouts}

- **接入层超时**：`server.read_timeout`、`server.write_timeout` 与 `server.idle_timeout` 控制客户端与 WAF 之间的 HTTP 连接生命周期。
- **反向代理超时**：`sites[].waf.performance.proxy_timeout` 控制 WAF 向后端上游源站发起请求与等待响应的最大超时时间。

## 动态热重载范围 {#reload}

- **即时热生效**：在 Web 控制台或通过 REST API 保存站点配置、自定义规则、IP 黑白名单、Bot 挑战策略及 ACL 规则时，系统会在内存中实时原子热重载，无需重启服务进程。
- **需重启生效**：修改 `server.listen`、`server.admin_listen` 等底层物理监听端口或网络驱动层参数后，须重启服务进程（通过 `cheesewaf restart` 或 systemd 服务管理器）。
