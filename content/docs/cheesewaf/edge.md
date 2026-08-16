---
title: Edge headers, cache, and compression
linkTitle: Edge
weight: 80
description: Set or delete response headers, cache static prefixes, and compress JSON or HTML.
---

Console: **Edge**.
Config: `edge`.
REST: `GET/PUT /api/edge`.

## Headers {#headers}

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

Use `set` to add a marker.
Use `delete` to strip origin-only headers before they reach the client.

## Cache {#cache}

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

Only cache prefixes you know are static.
Do not cache authenticated HTML.

## Compression {#compression}

```yaml
edge:
  compression:
    enabled: true
    algorithms: ["br", "gzip"]
    level: 5
    min_bytes: 1024
```

`content_types` in the sample covers `text/`, JSON, JavaScript, XML, and SVG.
