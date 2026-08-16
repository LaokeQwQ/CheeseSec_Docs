---
title: Web 控制台
linkTitle: 控制台
weight: 140
description: 管理界面上的页面，以及它们和本手册的对应关系。
---

完成 [初始化](../tutorial/setup/) 后，打开管理地址（默认 `http://127.0.0.1:9443/`）。

控制台是同一进程提供的 React 应用。
它使用会话 Cookie 和 CSRF。
登录可以要求 [登录验证码](../protection/bot-captcha/#login)。

## 页面对照 {#pages}

| 控制台路由 | 本手册 |
| --- | --- |
| `/` 仪表盘 | [监控](../monitor/) |
| `/sites` | [站点](../sites/) |
| `/ssl` | [TLS](../tls/) |
| `/rules` | [自定义规则](../protection/custom-rules/) |
| `/review` | [ALAP](../alap/) |
| `/logs` | [监控](../monitor/) |
| `/ip` | [IP 与地理](../protection/ip-geo-fingerprint/) |
| `/protection` | [防护](../protection/) |
| `/bot-challenge` | [Bot 与验证码](../protection/bot-captcha/) |
| `/edge` | [边缘](../edge/) |
| `/ai` | [ALAP](../alap/) |
| `/monitor` | [监控](../monitor/) |
| `/apisec` | [API 安全](../api-security/) |
| `/users` | [运维](../operations/) |
| `/ops` | [存储](../storage/) |
| `/updates` | [运维](../operations/) |
| `/block-pages` | [拦截页](../protection/block-page/) |
| `/attack-map` | [监控](../monitor/) |
| `/cluster` | [集群](../cluster/) |
| `/system` | [运维](../operations/) |
| `/captcha-lab` | [Bot 与验证码](../protection/bot-captcha/) |

主题（浅色、深色和几套配色）只存在于浏览器。
它们不会改数据平面。
