---
title: Protection
linkTitle: Protection
weight: 60
description: Semantic engine, custom rules, IP and geo, bot challenges, rate limits, ACL, and block pages.
---

Global defaults live under `protection` and `protection.policy`.
A site can overlay `sites[].waf.protection_policy`.

Console pages: **Protection**, **Rules**, **IP**, **Bot challenge**, **Block pages**.

{{< nav-cards cols="2" >}}
{{< nav-card title="Semantic engine" link="/docs/cheesewaf/protection/semantic/" desc="Decode, AST, per-engine switches." />}}
{{< nav-card title="Custom rules" link="/docs/cheesewaf/protection/custom-rules/" desc="Regex rules on URI and other locations." />}}
{{< nav-card title="IP, geo, fingerprint" link="/docs/cheesewaf/protection/ip-geo-fingerprint/" desc="Allow lists, deny lists, GeoIP, threat intel." />}}
{{< nav-card title="Bot and CAPTCHA" link="/docs/cheesewaf/protection/bot-captcha/" desc="JS challenge, slider, PoW, image, waiting room." />}}
{{< nav-card title="Rate limit" link="/docs/cheesewaf/protection/ratelimit/" desc="Token bucket and waiting room." />}}
{{< nav-card title="ACL" link="/docs/cheesewaf/protection/acl/" desc="Method, path, and header denies." />}}
{{< nav-card title="Block pages" link="/docs/cheesewaf/protection/block-page/" desc="Templates and custom HTML." />}}
{{< /nav-cards >}}
