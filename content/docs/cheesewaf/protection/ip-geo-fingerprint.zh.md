---
title: IP、地理位置与客户端指纹
linkTitle: IP 与地理
weight: 30
description: 配置 IP 黑白名单、GeoIP 国家封禁、威胁情报源同步及客户端软指纹防御体系。
---

CheeseWAF 在请求接入的最外层提供了网络层与客户端维度的快速访问控制能力。在 Web 控制台中进入 **IP 管理** 模块，或通过配置文件中的 `protection.ip` 进行设置。

## 静态名单与基础配置 {#lists}

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

- **IP 白名单（`whitelist`）**：命中白名单的客户端将直接跳过后续的 IP 拦截、Bot 挑战与语义分析。
- **IP 黑名单（`blacklist`）**：命中黑名单的请求将被当场拒绝并返回拦截页，不会进一步消耗语义引擎分析算力。

## GeoIP 地理位置封禁 {#geoip}

支持基于 MaxMind MMDB 格式的离线 IP 地理数据库实现国家与地区级流量阻断：

1. 将 `geoip.enabled` 设置为 `true`。
2. 将 `geoip.database` 指向有效的 Country MMDB 文件路径（如 `./data/GeoLite2-Country.mmdb`）。
3. 在 `blocked_countries` 列表中填入需要封禁的 ISO 3166-1 alpha-2 两位国家代码（如 `["US", "RU"]`）。

## 威胁情报源集成 {#intel}

支持导入第三方威胁情报 IP 库，并在控制台中支持情报源的自动化定时同步、手动更新与连通性测试。通过 REST API 端点 `POST /api/ip/threat-intel/lookup` 可查询特定 IP 的情报命中详情与置信度评分。

## 客户端软指纹与前置代理穿透 {#fingerprints}

- **客户端软指纹**：数据平面基于客户端 TLS 握手特征、HTTP 请求头顺序及相关特征计算轻量级软指纹。ALAP 异步分析在识别高危威胁后，支持将恶意指纹沉淀为封禁规则，作为辅助防御维度。
- **前置代理真实 IP 获取**：若 CheeseWAF 部署于 CDN、云负载均衡器或 Nginx 之后，必须在站点配置中声明 `sites[].waf.access_control.trusted_cidrs` 或 `trusted_proxy_providers`，以便正确从 `X-Forwarded-For` 等头部提取真实的客户端源 IP。
