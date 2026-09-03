---
title: TLS 与证书管理
linkTitle: TLS
weight: 90
description: 管理平面 TLS 安全加固、业务站点 HTTPS 证书配置、ACME 自动化签发、HTTP/3 及 HSTS 策略。
---

CheeseWAF 提供了完善的 TLS/HTTPS 安全加密支持，涵盖管理平面的访问加固以及业务数据平面的证书挂载、自动续期与 HTTP/3 协议支持。

在 Web 管理控制台中进入 **SSL 证书** 模块，底层对应配置文件中的 `server.admin_tls` 与 `tls` 块。

## 1. 管理平面 TLS 配置 {#admin}

```yaml
server:
  admin_tls:
    enabled: false
    cert_file: "./data/certs/admin.crt"
    key_file: "./data/certs/admin.key"
    self_signed: true
```

- **容器环境默认行为**：Docker 部署环境下默认启用管理端 TLS，并自动生成自签名证书。
- **生产安全要求**：若管理平面需要对外部公网开放，建议替换为权威机构签发的正式证书，避免使用浏览器自签名警告证书。

## 2. 业务站点 TLS 与 HTTP/3 配置 {#site}

```yaml
tls:
  auto_cert: false
  cert_file: "./data/certs/site.crt"
  key_file: "./data/certs/site.key"
  min_version: "1.3"
  hsts: true
```

- **数据平面监听**：配置 `server.listen_tls` 才会启用 HTTPS 监听；该字段没有默认值，未显式设置时保持关闭。将 `server.http3.enabled: true` 才会启用 HTTP/3；可显式设置 `server.listen_http3`，否则会回退到 TLS 监听地址（两者都未设置时使用 `:443`）。
- **TLS 版本约束**：支持通过 `min_version` 强制限制最低加密协议版本（如 `1.2` 或 `1.3`）。
- **HSTS 响应头**：开启 `hsts: true` 将在出站响应中自动注入 `Strict-Transport-Security` 响应头。
- **HTTP/3 (QUIC) 支持**：启用 `server.http3.enabled: true` 可开启基于 UDP 的 HTTP/3 协议支持（需前置已开启 TLS 监听）。

## 3. ACME 自动化证书签发与续期 {#acme}

CheeseWAF 内置了对 Let's Encrypt 等 ACME 协议证书颁发机构的支持：

1. **查询 DNS 提供商**：调用 `GET /api/acme/providers` 获取当前配置驱动已启用的 DNS API 插件列表。
2. **发起证书签发**：调用 `POST /api/sites/{id}/acme/issue` 为指定站点申请证书，系统将自动完成 DNS 挑战验证与证书绑定。
3. **安全存储**：ACME 账户私钥与申请的证书持久化存储在运行时数据目录下，请勿提交至 Git 版本控制系统。
