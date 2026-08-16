---
title: 防护
linkTitle: 防护
weight: 60
description: 语义引擎、自定义规则、IP 与地理、Bot 挑战、限流、ACL 和拦截页。
---

全局默认在 `protection` 和 `protection.policy`。
站点可以用 `sites[].waf.protection_policy` 覆盖。

控制台页面：**防护**、**规则**、**IP**、**Bot 挑战**、**拦截页**。

{{< nav-cards cols="2" >}}
{{< nav-card title="语义引擎" link="/zh/docs/cheesewaf/protection/semantic/" desc="解码、语法树、各引擎开关。" />}}
{{< nav-card title="自定义规则" link="/zh/docs/cheesewaf/protection/custom-rules/" desc="URI 等位置上的正则规则。" />}}
{{< nav-card title="IP、地理、指纹" link="/zh/docs/cheesewaf/protection/ip-geo-fingerprint/" desc="白名单、黑名单、GeoIP、威胁情报。" />}}
{{< nav-card title="Bot 与验证码" link="/zh/docs/cheesewaf/protection/bot-captcha/" desc="JS 挑战、滑块、PoW、图形验证码、排队室。" />}}
{{< nav-card title="限流" link="/zh/docs/cheesewaf/protection/ratelimit/" desc="令牌桶和排队室。" />}}
{{< nav-card title="ACL" link="/zh/docs/cheesewaf/protection/acl/" desc="按方法、路径、请求头拒绝。" />}}
{{< nav-card title="拦截页" link="/zh/docs/cheesewaf/protection/block-page/" desc="模板和自定义 HTML。" />}}
{{< /nav-cards >}}
