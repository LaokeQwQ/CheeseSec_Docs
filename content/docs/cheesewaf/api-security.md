---
title: API security
linkTitle: API security
weight: 70
description: Endpoint discovery, schema checks, JWT / JWKS, per-route rate limits, and RBAC.
---

Console: **API security**.
Config: `apisec`.
REST: `/api/apisec/*` plus the permission tables used by every other `/api` route.

## Discovery {#discovery}

When `apisec.discovery.enabled` is true, CheeseWAF samples recent traffic (`sample_limit`, `window`) and lists endpoints.
`ignore_prefixes` skips static assets.

`GET /api/apisec/endpoints` returns the current map.
`POST /api/apisec/validate` checks one request against a schema.

## Validation {#validation}

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

Enable a schema only after you have confirmed the path and required fields.

## JWT {#jwt}

`apisec.auth` can require JWT issuers, audiences, scopes, and algorithms.
Keys can come from a shared secret, a PEM file, inline PEM, a JWKS file, inline JWKS, or a remote `jwks_url`.
Remote JWKS is cached in `jwks_cache_file` and refreshed every `jwks_refresh_interval`.

## API rate limits {#rate}

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

This is per discovered API route, not the global [data-plane bucket](../protection/ratelimit/).

## Permissions {#permissions}

```yaml
apisec:
  permissions:
    admin: ["*"]
    readonly: ["read:*", "read:cluster"]
```

Management routes use names such as `read:sites`, `write:protection`, `use:ai`, `approve:ai`, `manage:api_tokens`.
See [REST API](../api/) for the route-to-permission map.
