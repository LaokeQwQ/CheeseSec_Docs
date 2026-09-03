---
title: TLS & Certificate Management
linkTitle: TLS
weight: 90
description: Management plane TLS encryption, business site HTTPS certificate configuration, ACME automated issuance, HTTP/3, and HSTS policies.
---

CheeseWAF provides comprehensive TLS/HTTPS cryptographic capabilities, covering secure transport encryption for the management plane as well as automated certificate provisioning, renewal, and HTTP/3 support for business traffic.

Manage certificates visually in the Web console under **SSL**, or configure settings under `server.admin_tls` and `tls`.

## 1. Management Plane TLS Configuration {#admin}

```yaml
server:
  admin_tls:
    enabled: false
    cert_file: "./data/certs/admin.crt"
    key_file: "./data/certs/admin.key"
    self_signed: true
```

- **Container Default Behavior**: The Docker deployment image enables management TLS by default, generating a self-signed certificate upon initial container launch.
- **Production Requirements**: If the management plane is exposed over public networks, replace self-signed certificates with a trusted CA-signed certificate.

## 2. Business Site TLS & HTTP/3 Configuration {#site}

```yaml
tls:
  auto_cert: false
  cert_file: "./data/certs/site.crt"
  key_file: "./data/certs/site.key"
  min_version: "1.3"
  hsts: true
```

- **Data Plane Listeners**: Configure `server.listen_tls` to enable an HTTPS ingress listener; it has no default value and remains disabled until explicitly set. Enable HTTP/3 with `server.http3.enabled: true`; `server.listen_http3` may be set explicitly and otherwise falls back to the TLS listener (or `:443` when neither address is set).
- **TLS Version Constraints**: Use `min_version` to enforce minimum protocol versions (e.g., `1.2` or `1.3`).
- **HSTS Enforcement**: Setting `hsts: true` automatically injects the `Strict-Transport-Security` header into outbound responses.
- **HTTP/3 (QUIC) Support**: Set `server.http3.enabled: true` to enable UDP-based HTTP/3 support (requires an active TLS listener).

## 3. ACME Automated Certificate Issuance & Renewal {#acme}

CheeseWAF natively supports the ACME protocol for automated certificate management (e.g., Let's Encrypt):

1. **Query DNS Providers**: Call `GET /api/acme/providers` to list the DNS API challenge providers that are configured and enabled in the running instance; this is not a catalog of every provider supported by the implementation.
2. **Issue Certificates**: Invoke `POST /api/sites/{id}/acme/issue` for a site to automatically perform DNS challenge verification and bind the issued certificate.
3. **Secure Key Storage**: ACME account private keys and generated certificates are persisted securely in the runtime data directory; do not commit them to Git.
