---
title: 边缘响应头、缓存和压缩
linkTitle: 边缘
weight: 80
description: 设置或删除响应头，缓存静态前缀，压缩 JSON 或 HTML。
---

控制台：**边缘**。
配置：`edge`。
REST：`GET/PUT /api/edge`。

## 响应头 {#headers}

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

`set` 用来加标记。
`delete` 用来在到达客户端之前去掉只该源站看到的头。

## 缓存 {#cache}

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

只缓存你确定是静态的前缀。
不要缓存需要登录的 HTML。

## 压缩 {#compression}

```yaml
edge:
  compression:
    enabled: true
    algorithms: ["br", "gzip"]
    level: 5
    min_bytes: 1024
```

示例里的 `content_types` 覆盖 `text/`、JSON、JavaScript、XML 和 SVG。
