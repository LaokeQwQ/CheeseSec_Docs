---
title: IP, GeoIP & Client Fingerprinting
linkTitle: IP & GeoIP
weight: 30
description: Configure IP whitelists and blacklists, GeoIP country restrictions, threat intelligence feed synchronization, and client soft-fingerprinting.
---

CheeseWAF enforces network-layer access controls at the outermost boundary of the request pipeline. Manage these controls visually under **IP** in the Web console, or define them in the configuration file under `protection.ip`.

## Static Access Lists & Base Configuration {#lists}

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

- **IP Whitelist (`whitelist`)**: Matching client IPs immediately bypass subsequent IP restrictions, bot challenges, and semantic inspection.
- **IP Blacklist (`blacklist`)**: Matching client IPs are blocked at the network entry point, returning a block page without consuming semantic engine resources.

## GeoIP Country Restrictions {#geoip}

Block traffic from specific countries using offline MaxMind MMDB databases:

1. Set `geoip.enabled` to `true`.
2. Point `geoip.database` to a valid Country MMDB file path (e.g., `./data/GeoLite2-Country.mmdb`).
3. Specify ISO 3166-1 alpha-2 two-letter country codes in `blocked_countries` (e.g., `["US", "RU"]`).

## Threat Intelligence Integration {#intel}

Import third-party threat intelligence IP feeds directly into CheeseWAF. The Web console supports automated scheduled synchronization, manual updates, and connectivity tests. Query intelligence status for specific IPs via the REST endpoint `POST /api/ip/threat-intel/lookup`.

## Client Soft-Fingerprinting & Trusted Proxies {#fingerprints}

- **Client Soft-Fingerprints**: The Data Plane computes lightweight fingerprints based on TLS handshake parameters, HTTP header ordering, and related client attributes. ALAP review can persist malicious fingerprints as defense rules to serve as corroborating evidence.
- **Trusted Upstream Proxies**: When CheeseWAF is deployed behind a CDN, cloud load balancer, or reverse proxy, configure `sites[].waf.access_control.trusted_cidrs` or `trusted_proxy_providers` to correctly extract client IP addresses from `X-Forwarded-For` headers.
