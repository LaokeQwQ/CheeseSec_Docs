---
title: Gateway Adapters
linkTitle: Adapters
weight: 55
description: Go-first self-hosted gateway adapters for NGINX, Envoy, and Kubernetes, decoupling protocol translation from the core detection engine.
---

[CheeseWAF-Adapters](https://github.com/LaokeQwQ/CheeseWAF-Adapters) provides Go-first, self-hosted gateway adapters for CheeseWAF. It completely separates gateway-specific glue code from the core detection engine. By running as a lightweight daemon (`adapterd`) beside your reverse proxy or workload, it translates gateway-specific protocols into a standardized, versioned HTTP inspection contract and maps core security decisions back to native gateway responses.

## Architecture & Design Principles {#architecture}

```text
    NGINX / Envoy / Kubernetes Gateway
                  |
                  | auth_request / ext_authz / ext_proc
                  v
    CheeseWAF-Adapters (Go, adapterd)
                  |
                  | Versioned HTTP Inspection Contract (/api/v1/adapter/inspect)
                  v
    CheeseWAF Core Daemon (Self-hosted, Go)
                  |
                  +-- Inline Synchronous Decisions (allow / block / challenge)
                  +-- Asynchronous Telemetry / Postanalytics (/api/v1/adapter/telemetry)
```

- **Self-Hosted & Sidecar-First**: Operates without external SaaS control planes or vendor dependencies. By default, `adapterd` deploys as a local loopback process (`127.0.0.1:9080`) directly alongside the gateway.
- **Ultra-Thin Adapter Boundary**: Focuses exclusively on protocol translation and response mapping. It never duplicates detectors, AST parsers, signature tables, or management state; all security decisions remain centralized in CheeseWAF core.
- **Fail-Closed by Default**: When the CheeseWAF core service is unreachable or encounters timeouts, the adapter returns HTTP `503 Service Unavailable`. Traffic is never silently allowed unless explicitly configured.
- **Bounded Request Body Handling**: By default, request bodies are not forwarded to the core. When explicitly enabled, body inspection is capped at a strict boundary (default 64 KB). Truncated payloads are flagged with `BodyTruncated=true`; if the core returns `allow` or times out, the adapter rejects the request with HTTP `413 Request Entity Too Large`.
- **Security Credentials & Network Policy**: Gateway callers authenticate using the dedicated `X-CheeseWAF-Adapter-Token` HTTP header (never via `Authorization: Bearer`), restricted to validated CIDR blocks configured in `CHEESEWAF_ADAPTER_TRUSTED_PROXY_CIDRS`.

## Versioned Inspection Contract (`v1`) {#contract}

The adapter communicates with the CheeseWAF core via `contracts/inspection/v1`:

- **Inline Inspection Endpoint**: Accessible by default at `/api/v1/adapter/inspect`, receiving normalized client metadata, TLS fingerprints, and bounded body content within a strict latency budget (default 100ms).
- **Core Security Actions**:
  - `allow`: Permits the request and forwards it upstream.
  - `block`: Terminates the request and renders a configured block page or status code.
  - `challenge`: Triggers client verification (such as silent JS challenge or CAPTCHA).
  - `log`: Permits the request while recording an audit entry (normalized to monitoring mode).
- **Asynchronous Telemetry Endpoint**: Hosted at `/api/v1/adapter/telemetry`, receiving rate-limited, best-effort events without impacting real-time forwarding throughput.

## Gateway Integration Examples {#gateways}

### 1. NGINX `auth_request` Configuration

Use NGINX's `ngx_http_auth_request_module` to authorize incoming requests with `adapterd`:

```nginx
# Primary business site configuration
location / {
    auth_request /cheesewaf_auth;
    auth_request_set $waf_status $upstream_status;

    # Forward to upstream application upon successful authorization
    proxy_pass http://backend_cluster;
}

# Internal authorization subrequest endpoint
location = /cheesewaf_auth {
    internal;
    proxy_pass http://127.0.0.1:9080/v1/inspect;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-CheeseWAF-Adapter-Token "YOUR_SECURE_ADAPTER_TOKEN";
    proxy_set_header X-Original-URI $request_uri;
    proxy_set_header X-Original-Method $request_method;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### 2. Envoy `ext_authz` Configuration

Configure Envoy's external authorization HTTP filter in the filter chain:

```yaml
http_filters:
  - name: envoy.filters.http.ext_authz
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
      http_service:
        server_uri:
          uri: 127.0.0.1:9080
          cluster: cheesewaf_adapter_cluster
          timeout: 0.100s
        authorization_request:
          allowed_headers:
            patterns:
              - exact: cookie
              - exact: user-agent
              - prefix: x-
          headers_to_add:
            - key: x-cheesewaf-adapter-token
              value: "YOUR_SECURE_ADAPTER_TOKEN"
      failure_mode_allow: false
      with_request_body:
        max_request_bytes: 65536
        pack_as_bytes: true
```

{{% pageinfo color="warning" %}}
When Envoy indicates `x-envoy-auth-partial-body: true`, the adapter flags the body as incomplete and rejects the request with HTTP 413 unless the core explicitly blocks it, preventing large-payload truncation bypasses.
{{% /pageinfo %}}

## Runtime Configuration Reference {#env}

```bash
# Launch the local adapter daemon
adapterd --listen 127.0.0.1:9080 --core-url http://127.0.0.1:8080
```

| Variable / Flag | Default Value | Description |
| --- | --- | --- |
| `CHEESEWAF_ADAPTER_LISTEN` / `--listen` | `127.0.0.1:9080` | Local network address for the adapter daemon |
| `CHEESEWAF_CORE_URL` / `--core-url` | **Required** | Address of the self-hosted CheeseWAF data plane or core inspection service |
| `CHEESEWAF_CORE_INSPECT_PATH` | `/api/v1/adapter/inspect` | Core inline inspection API path |
| `CHEESEWAF_CORE_TELEMETRY_PATH` | `/api/v1/adapter/telemetry` | Core telemetry reporting endpoint |
| `CHEESEWAF_CORE_HEALTH_PATH` | `/healthz` | Core health endpoint used for `/readyz` probe delegation |
| `CHEESEWAF_CORE_TOKEN` | Empty | Bearer token used by adapterd to communicate with the core |
| `CHEESEWAF_ADAPTER_TOKEN` | Empty | Dedicated token required from gateways in `X-CheeseWAF-Adapter-Token` |
| `CHEESEWAF_ADAPTER_TRUSTED_PROXY_CIDRS` | `127.0.0.1/32,::1/128` | Trusted CIDR list permitted to provide forwarded client IP headers |
| `CHEESEWAF_ADAPTER_REQUEST_TIMEOUT` | `100ms` | Maximum execution budget for inline decisions |
| `CHEESEWAF_ADAPTER_FAIL_MODE` | `closed` | Fail mode when core is offline: `closed` (HTTP 503) or `open` (HTTP 204) |
| `CHEESEWAF_ADAPTER_FORWARD_BODY` | `false` | Enables bounded request body inspection |
| `CHEESEWAF_ADAPTER_MAX_BODY_BYTES` | `65536` | Maximum body capture limit (64 KB) |
| `CHEESEWAF_ADAPTER_FORWARD_SENSITIVE_HEADERS` | `false` | Permits forwarding credentials (Cookie/Authorization) to the core |

## Roadmap {#roadmap}

1. **Streaming Protocol**: Envoy `ext_proc` adapter for streaming inspection of large request bodies and dynamic response header mutations.
2. **Kubernetes Integration**: Dedicated Kubernetes Sidecar Controller supporting automated injection and routing via Pod Annotations.
3. **Ecosystem Gateways**: Native integrations for Kong, Apache APISIX, and Traefik.
