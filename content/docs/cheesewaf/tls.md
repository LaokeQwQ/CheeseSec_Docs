---
title: TLS and certificates
linkTitle: TLS
weight: 90
description: Admin TLS, site certificates, ACME issuance, HTTP/3, and HSTS.
---

Console: **SSL**.
Config: `server.admin_tls`, `tls`, and per-site ACME calls.
REST: `/api/acme/providers`, `POST /api/sites/{id}/acme/issue`.

## Admin listener {#admin}

```yaml
server:
  admin_tls:
    enabled: false
    cert_file: "./data/certs/admin.crt"
    key_file: "./data/certs/admin.key"
    self_signed: true
```

Docker images turn admin TLS on with a self-signed cert.
A public admin listener must use a real certificate.

## Site TLS {#site}

```yaml
tls:
  auto_cert: false
  cert_file: "./data/certs/admin.crt"
  key_file: "./data/certs/admin.key"
  min_version: "1.3"
  hsts: true
```

`server.listen_tls` and `server.listen_http3` bind the data plane.
HTTP/3 needs `server.http3.enabled` and a TLS listener.

## ACME {#acme}

The console lists DNS providers at `GET /api/acme/providers`.
`POST /api/sites/{id}/acme/issue` requests a certificate for that site.
Keep account keys in the data directory, not in the git repo.
