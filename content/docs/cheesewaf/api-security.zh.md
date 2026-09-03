---
title: API 接口安全
linkTitle: API 安全
weight: 70
description: 自动 API 资产发现、请求 Schema 结构校验、JWT/JWKS 鉴权、路由级精准限流及 RBAC 权限控制。
---

随着前后端分离与微服务架构的普及，API 接口已成为主要的攻击暴露面。CheeseWAF 的 API 安全模块提供接口自动发现、输入 Schema 强校验、JWT 身份认证及路由级精准限流能力。

在 Web 管理控制台中可进入 **API 安全** 模块进行可视化配置，底层对应配置文件中的 `apisec` 块。

## 1. 自动 API 资产发现 {#discovery}

启用 `apisec.discovery.enabled: true` 后，系统会在流量转发过程中根据 `window`（时间窗口）与 `sample_limit`（采样上限）自动对入站请求进行路径聚类，绘制 API 资产拓扑：

- **静态路径过滤**：配置 `ignore_prefixes` 可自动跳过静态文件路径（如 `/static`、`*.css`）。
- **资产查询接口**：调用 `GET /api/apisec/endpoints` 获取当前已识别的 API 接口清单与请求统计。
- **结构测试**：调用 `POST /api/apisec/validate` 可对单条测试请求进行 Schema 契约校验。

## 2. 请求 Schema 校验 {#validation}

Schema 校验模块用于强制校验入站请求的结构完整性，防范参数注入与未预期字段传递：

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
        enabled: true
```

支持校验请求方法、路径正则、必填 Query/Body 参数、必填 HTTP 请求头及允许的最大请求体长度（`max_body_bytes`）。

## 3. JWT 与 JWKS 身份认证 {#jwt}

通过 `apisec.auth` 可在前置代理层实现无状态的 JWT 令牌鉴权校验：

- **验证维度**：支持校验 Token 签名有效性、签发方（`iss`）、受众（`aud`）、有效时间戳（`exp`/`nbf`）及指定的加密算法。
- **密钥来源**：支持对称共享密钥、本地 PEM 证书文件、内联 PEM 文本、本地 JWKS 文件或远程 `jwks_url`。
- **自动缓存与刷新**：配置远程 JWKS 时，系统将公钥集缓存于 `jwks_cache_file`，并按 `jwks_refresh_interval` 周期自动刷新。

## 4. 路由级精准限流 {#rate}

与 [数据平面全局分片滑动窗口计数器限流](../protection/ratelimit/) 不同，API 接口限流专门针对已识别的具体业务路由进行配额控制（例如高频敏感的登录与发送验证码接口）：

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

## 5. RBAC 权限矩阵定义 {#permissions}

`apisec.permissions` 用于定义管理平面各角色的权限范围：

```yaml
apisec:
  permissions:
    admin: ["*"]
    readonly: ["read:*", "read:cluster"]
```

关于具体权限标识符（如 `read:sites`、`write:protection`、`manage:api_tokens`）与 REST API 端点的对应关系，请参考 [REST API 接口参考](../api/)。
