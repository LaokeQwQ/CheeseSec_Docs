---
title: IP、地理与指纹
linkTitle: IP 与地理
weight: 30
description: 白名单、黑名单、GeoIP、信誉覆盖和威胁情报源。
---

控制台：**IP**。
配置：`protection.ip`。
REST：`/api/ip`、`/api/protection/ip`、`/api/ip/threat-intel/*`。

## 静态名单 {#lists}

```yaml
protection:
  ip:
    whitelist: ["127.0.0.1", "::1"]
    blacklist: []
    access_rules: []
    reputation_overrides: {}
    tags: {}
    threat_intel: []
    geoip:
      enabled: false
      database: "./data/GeoLite2-Country.mmdb"
      blocked_countries: []
```

白名单地址会跳过后面的 IP 拒绝。
黑名单地址到不了语义引擎。

## GeoIP {#geoip}

把 `geoip.enabled` 设成 `true`，并把 `database` 指到 MaxMind 风格的 Country MMDB。
`blocked_countries` 用 ISO 国家代码。
CheeseWAF 不会替你下载 GeoLite2。

## 威胁情报 {#intel}

可以在控制台导入、导出、同步和测试情报源。
查询接口是 `POST /api/ip/threat-intel/lookup`。

## 指纹 {#fingerprints}

数据平面会记一份 **客户端软指纹**（不是硬件 TPM 身份）。
ALAP 在高置信审查后，可以把指纹写成封禁规则。
把指纹命中当成辅助证据，不要当唯一控制手段。

CheeseWAF 前面还有一层代理时，填写 `sites[].waf.access_control.trusted_cidrs` 或 `trusted_proxy_providers`，否则客户端 IP 会变成代理地址。
