---
title: API 安全
linkTitle: API 安全
weight: 70
description: 接口发现、Schema 校验、JWT / JWKS、按路由限流，以及 RBAC。
---

控制台：**API 安全**。
配置：`apisec`。
REST：`/api/apisec/*`，再加上所有 `/api` 路由共用的权限表。

## 发现 {#discovery}

`apisec.discovery.enabled` 为真时，CheeseWAF 按 `sample_limit` 和 `window` 采样近期流量，列出接口。
`ignore_prefixes` 会跳过静态资源。

`GET /api/apisec/endpoints` 返回当前地图。
`POST /api/apisec/validate` 按 Schema 检查一条请求。

## 校验 {#validation}

```yaml
apisec:
  validation:
    enabled: true
    schemas:
      - id: "api-search"
        method: "GET"
        path_pattern: "^/api/search$"
        required_params: ["q"]
        required_headers: []
        max_body_bytes: 0
        enabled: false
```

先确认路径和必填字段，再打开某条 Schema。

## JWT {#jwt}

`apisec.auth` 可以要求签发方、受众、范围和算法。
密钥可以来自分享密钥、PEM 文件、内联 PEM、JWKS 文件、内联 JWKS，或远程 `jwks_url`。
远程 JWKS 缓存在 `jwks_cache_file`，按 `jwks_refresh_interval` 刷新。

## 接口限流 {#rate}

```yaml
apisec:
  rate_limits:
    - id: "login-api"
      method: "POST"
      path_pattern: "^/api/auth/login$"
      requests: 10
      window: 1m
      enabled: true
```

这是按已发现的 API 路由限流，不是全局 [数据平面令牌桶](../protection/ratelimit/)。

## 权限 {#permissions}

```yaml
apisec:
  permissions:
    admin: ["*"]
    readonly: ["read:*", "read:cluster"]
```

管理路由使用 `read:sites`、`write:protection`、`use:ai`、`approve:ai`、`manage:api_tokens` 这类名字。
路由和权限的对应见 [REST API](../api/)。
