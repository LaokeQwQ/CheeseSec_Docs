---
title: 边缘优化：响应头、静态缓存与内容压缩
linkTitle: 边缘
weight: 80
description: 配置 HTTP 响应头增删改写、静态资源路径缓存及 Brotli/Gzip 高效压缩策略。
---

CheeseWAF 在反向代理链路上提供了边缘优化能力，支持自定义响应头注入与剥离、静态内容缓存加速以及动态内容压缩传输。

在 Web 管理控制台中进入 **边缘优化** 模块，底层配置对应 `edge` 块，支持通过 REST API `GET/PUT /api/edge` 进行热配置。

## 1. 响应头注入与剥离规则 {#headers}

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

- **`operation: "set"`**：向客户端响应中注入自定义响应头（如安全标识、Trace ID 或跨域头）。
- **`operation: "delete"`**：在响应返回给客户端前，安全剥离源站返回的内部敏感响应头（如 `X-Origin-Secret`、`Server` 内部版本等），防止技术栈信息泄露。

## 2. 静态内容缓存策略 {#cache}

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

- **路径前缀过滤**：通过 `path_prefixes` 限制仅缓存确定为公开静态资源的路径（如 `/assets/`、`/static/`），严禁对涉及用户会话或动态鉴权的 HTML/API 接口开启全局缓存。
- **缓存控制**：支持限定缓存的 HTTP 状态码（如 200 与 304）、缓存有效期（`ttl`）及允许缓存的最大单体体积（`max_body_bytes`）。

## 3. Brotli 与 Gzip 压缩 {#compression}

```yaml
edge:
  compression:
    enabled: true
    algorithms: ["br", "gzip"]
    level: 5
    min_bytes: 1024
```

- **多算法支持**：同时支持现代高压缩比的 Brotli（`br`）与通用的 Gzip 算法。
- **触发阈值**：通过 `min_bytes` 设定触发压缩的最小响应体积（如 1024 字节），避免对极短文本压缩反而增加开销。
- **内容类型**：预设规则支持覆盖 `text/*`、`application/json`、`application/javascript`、`application/xml` 及 `image/svg+xml`。
