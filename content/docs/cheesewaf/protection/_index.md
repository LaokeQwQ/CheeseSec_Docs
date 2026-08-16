---
title: Security Protection Policies
linkTitle: Protection
weight: 60
description: Complete guide to the AST semantic engine, custom regex rules, IP/GeoIP filtering, bot challenges, token bucket rate limits, ACLs, and block pages.
---

CheeseWAF provides a defense-in-depth architecture spanning from network-level controls to application semantic analysis. Baseline protection policies are defined globally in `protection` and `protection.policy`, with support for granular per-site overrides via `sites[].waf.protection_policy`.

{{< nav-cards cols="2" >}}
{{< nav-card title="AST Semantic Engine" link="/docs/cheesewaf/protection/semantic/" desc="Recursive parameter decoding, abstract syntax tree analysis, engine toggles, and analysis budget control." />}}
{{< nav-card title="Custom Regex Rules" link="/docs/cheesewaf/protection/custom-rules/" desc="High-performance regular expression matching on URIs, headers, and parameters with priority ordering." />}}
{{< nav-card title="IP, GeoIP & Fingerprints" link="/docs/cheesewaf/protection/ip-geo-fingerprint/" desc="IP access lists, ISO GeoIP country restrictions, threat intelligence synchronization, and client soft-fingerprinting." />}}
{{< nav-card title="Bot Challenges & CAPTCHA" link="/docs/cheesewaf/protection/bot-captcha/" desc="Silent JavaScript challenges, PoW (Altcha), interactive slider/image CAPTCHAs, and waiting room scheduling." />}}
{{< nav-card title="Rate Limiting" link="/docs/cheesewaf/protection/ratelimit/" desc="High-performance token bucket traffic shaping on the Data Plane with queue and drop actions." />}}
{{< nav-card title="Access Control Lists (ACL)" link="/docs/cheesewaf/protection/acl/" desc="Low-overhead prefix-tree filtering based on HTTP methods, URI prefixes, and request headers." />}}
{{< nav-card title="Block Response Pages" link="/docs/cheesewaf/protection/block-page/" desc="Pre-built modern block templates, custom HTML branding upload, and Trace ID request tracking." />}}
{{< /nav-cards >}}
