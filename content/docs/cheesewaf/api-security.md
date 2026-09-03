---
title: API Security & Governance
linkTitle: API Security
weight: 70
description: Automated API asset discovery, request schema structure validation, JWT/JWKS authentication, route-level rate limiting, and RBAC policies.
---

With the widespread adoption of single-page applications and microservices, API endpoints represent a primary attack surface. CheeseWAF's API Security module delivers automatic endpoint discovery, strict contract schema validation, stateless JWT authentication, and route-level rate limiting.

Configure settings visually in the Web console under **API Security**, or define them in configuration files under the `apisec` block.

## 1. Automated API Asset Discovery {#discovery}

When `apisec.discovery.enabled: true` is active, CheeseWAF samples live request streams across `window` intervals up to `sample_limit` volumes, automatically clustering URI paths into an API asset inventory:

- **Static Path Filtering**: Configure `ignore_prefixes` to exclude static assets (such as `/static`, `*.css`, or image paths).
- **Asset Query Endpoint**: Invoke `GET /api/apisec/endpoints` to retrieve the current inventory of discovered endpoints and traffic statistics.
- **Contract Testing**: Invoke `POST /api/apisec/validate` to validate a test request against registered schemas.

## 2. Request Schema Validation {#validation}

Schema validation enforces strict structural contracts on incoming requests, preventing unauthorized parameter injection and parameter pollution:

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

Supports validation of HTTP methods, path regular expressions, mandatory query/body parameters, mandatory HTTP headers, and maximum allowable body payload sizes (`max_body_bytes`).

## 3. JWT & JWKS Authentication {#jwt}

Enforce stateless JSON Web Token authentication at the proxy layer via `apisec.auth`:

- **Claim Verification**: Validates cryptographic signatures, token issuers (`iss`), audiences (`aud`), timestamps (`exp`/`nbf`), and allowed signing algorithms.
- **Key Providers**: Supports symmetric shared secrets, local PEM certificate files, inline PEM strings, local JWKS files, and remote `jwks_url` endpoints.
- **Automated Caching & Rotation**: Remote JWKS keys are cached locally in `jwks_cache_file` and automatically refreshed according to `jwks_refresh_interval`.

## 4. Route-Level Precision Rate Limiting {#rate}

Unlike global [Data Plane sharded sliding-window counter limiting](../protection/ratelimit/), API rate limiting applies strictly to specific HTTP method and path combinations (such as sensitive authentication or SMS dispatch endpoints):

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

## 5. RBAC Permission Matrix {#permissions}

`apisec.permissions` defines role-based access control mappings for the management plane:

```yaml
apisec:
  permissions:
    admin: ["*"]
    readonly: ["read:*", "read:cluster"]
```

For the mapping between permission identifiers (such as `read:sites`, `write:protection`, `manage:api_tokens`) and REST API endpoints, see [RESTful API Reference](../api/).
