---
title: 配置参考
linkTitle: 配置
weight: 170
description: cheesewaf.yaml 的顶层键，以及本手册里解释每一段的位置。
---

第一次启动会在数据目录写出 `cheesewaf.yaml`。
模板是产品仓库里的 [`configs/cheesewaf.yaml`](https://github.com/LaokeQwQ/CheeseWAF/blob/master/configs/cheesewaf.yaml)。

| 键 | 手册 |
| --- | --- |
| `server` | [TLS](../tls/)、[介绍](../intro/) |
| `tls` | [TLS](../tls/) |
| `setup` | [初始化](../tutorial/setup/)、[存储](../storage/) |
| `deployment` / `cluster` | [集群](../cluster/) |
| `console` | [Bot 与验证码](../protection/bot-captcha/)、[监控](../monitor/) |
| `sites` | [站点](../sites/) |
| `protection` | [防护](../protection/) |
| `block_page` | [拦截页](../protection/block-page/) |
| `storage` | [存储](../storage/) |
| `logging` | [监控](../monitor/) |
| `ai` | [ALAP](../alap/) |
| `update` | [运维](../operations/) |
| `scheduler` | [存储](../storage/) |
| `edge` | [边缘](../edge/) |
| `monitor` | [监控](../monitor/) |
| `apisec` | [API 安全](../api-security/) |

## 超时 {#timeouts}

`server.read_timeout`、`write_timeout` 和 `idle_timeout` 作用于 HTTP 服务。
`sites[].waf.performance.proxy_timeout` 作用于源站。

## 重载 {#reload}

在控制台保存站点或防护策略时，对应片段会热加载。
改监听地址仍需要重启进程（`cheesewaf restart` 或 systemd）。
