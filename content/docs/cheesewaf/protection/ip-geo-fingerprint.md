---
title: IP, geo, and fingerprint
linkTitle: IP and geo
weight: 30
description: Allow lists, deny lists, GeoIP, reputation overrides, and threat-intel feeds.
---

Console: **IP**.
Config: `protection.ip`.
REST: `/api/ip`, `/api/protection/ip`, `/api/ip/threat-intel/*`.

## Static lists {#lists}

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

Allow-listed addresses skip later IP denies.
Deny-listed addresses never reach the semantic engine.

## GeoIP {#geoip}

Set `geoip.enabled: true` and point `database` at a MaxMind-style Country MMDB.
`blocked_countries` uses ISO country codes.
CheeseWAF does not download GeoLite2 for you.

## Threat intel {#intel}

Operators can import, export, sync, and test providers from the console.
Lookups are available at `POST /api/ip/threat-intel/lookup`.

## Fingerprints {#fingerprints}

The data plane records a **soft client fingerprint** (not a hardware TPM identity).
After a high-confidence review, ALAP can save a fingerprint deny rule.
Treat fingerprint hits as supporting evidence, not as the only control.

When CheeseWAF sits behind another proxy, fill `sites[].waf.access_control.trusted_cidrs` or `trusted_proxy_providers` so the client IP is not the proxy’s address.
