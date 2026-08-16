---
title: TLS 与证书
linkTitle: TLS
weight: 90
description: 管理端 TLS、站点证书、ACME 签发、HTTP/3 和 HSTS。
---

控制台：**SSL**。
配置：`server.admin_tls`、`tls`，以及按站点发起的 ACME。
REST：`/api/acme/providers`，`POST /api/sites/{id}/acme/issue`。

## 管理监听 {#admin}

```yaml
server:
  admin_tls:
    enabled: false
    cert_file: "./data/certs/admin.crt"
    key_file: "./data/certs/admin.key"
    self_signed: true
```

Docker 镜像会打开管理端 TLS，并用自签名证书。
对公网开放的管理监听必须换成正式证书。

## 站点 TLS {#site}

```yaml
tls:
  auto_cert: false
  cert_file: "./data/certs/admin.crt"
  key_file: "./data/certs/admin.key"
  min_version: "1.3"
  hsts: true
```

`server.listen_tls` 和 `server.listen_http3` 绑定数据平面。
HTTP/3 需要 `server.http3.enabled`，并且已经有 TLS 监听。

## ACME {#acme}

控制台通过 `GET /api/acme/providers` 列出 DNS 提供方。
`POST /api/sites/{id}/acme/issue` 给该站点申请证书。
账户密钥放在数据目录，不要放进 git。
