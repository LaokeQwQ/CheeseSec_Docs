---
title: "Edge Optimization: Headers, Caching & Compression"
linkTitle: Edge Features
weight: 80
description: Edge HTTP header rewriting, static resource proxy caching, and Brotli/Gzip response payload compression.
---

CheeseWAF provides edge acceleration capabilities at the reverse proxy layer to optimize response latency and reduce origin bandwidth consumption. Manage these settings visually under **Edge** in the Web console, or define them in configuration files under the `edge` block.

## 1. HTTP Response Header Rewriting {#headers}

```yaml
edge:
  headers:
    enabled: true
    rules:
      - id: "set-edge-marker"
        operation: "set"
        header: "X-CheeseWAF"
        value: "edge"
        enabled: true
      - id: "remove-origin-leak"
        operation: "delete"
        header: "X-Origin-Secret"
        enabled: true
```

- **Set Headers (`set`)**: Appends custom tracking or security headers (e.g., `X-Content-Type-Options: nosniff`).
- **Strip Headers (`delete`)**: Removes sensitive internal origin response headers (such as `Server`, `X-Powered-By`, or internal debug tokens) before responses reach the public internet.

## 2. Static Asset Proxy Caching {#cache}

```yaml
edge:
  cache:
    enabled: true
    mode: "public"
    ttl: 5m
    status_codes: [200, 304]
    path_prefixes: ["/assets/", "/static/"]
    max_body_bytes: 2097152
```

- **Path Targeting**: Specify path prefixes in `path_prefixes` strictly for purely static assets (e.g., CSS, JS, fonts, images).
- **Security Caution**: Never configure caching rules for authenticated dynamic API endpoints or personalized HTML pages.

## 3. High-Efficiency Response Compression {#compression}

```yaml
edge:
  compression:
    enabled: true
    algorithms: ["br", "gzip"]
    level: 5
    min_bytes: 1024
```

- **Compression Algorithms**: Supports Brotli (`br`) and standard Gzip (`gzip`) algorithms.
- **Trigger Conditions**: Responses are compressed only when payload sizes exceed `min_bytes` (e.g., 1024 bytes) and match defined MIME types (`text/*`, `application/json`, `application/javascript`, `image/svg+xml`).
