---
title: 网关适配器 (Adapters)
linkTitle: 网关适配器
weight: 55
description: 面向 NGINX、Envoy 及 Kubernetes 的自托管网关适配器，解耦协议转换与检测核心，支持 inline 授权与异步遥测。
---

[CheeseWAF-Adapters](https://github.com/LaokeQwQ/CheeseWAF-Adapters) 是面向 CheeseWAF 的 Go-first、自托管网关适配组件。它将特定网关的胶水代码与 WAF 核心检测引擎彻底解耦，通过轻量级守护进程 `adapterd` 部署于网关或业务旁边，负责将外部网关协议转换为标准化的版本化检查契约，并将决策结果转换回网关原生响应。

## 架构与核心原则 {#architecture}

```text
    NGINX / Envoy / Kubernetes 网关
                  |
                  | auth_request / ext_authz / ext_proc
                  v
    CheeseWAF-Adapters (Go, adapterd)
                  |
                  | 版本化 HTTP 检查契约 (/api/v1/adapter/inspect)
                  v
    CheeseWAF 核心服务 (自托管, Go)
                  |
                  +-- Inline 同步安全决策 (allow / block / challenge)
                  +-- 异步 Telemetry / Postanalytics (/api/v1/adapter/telemetry)
```

- **自托管与 Sidecar 优先**：不依赖任何 SaaS 控制面或外部厂商服务；默认以网关或工作负载旁边的本地独立进程（`127.0.0.1:9080`）运行。
- **适配器保持极薄**：仅处理网关协议解析与响应语义适配，不复制任何检测器、规则解析、签名计算或管理状态；所有安全决策完全交由 CheeseWAF 核心处理。
- **默认 Fail-Closed（安全熔断）**：当 CheeseWAF 核心不可用或超时时，适配器默认返回 `503 Service Unavailable`，严禁在未显式配置时静默放行流量。
- **有界请求体（Bounded Body）机制**：默认不向核心转发请求体；仅在策略明确开启时以受控上限（默认 64 KB）转发。超过上限时标记 `BodyTruncated=true`；若核心返回 `allow` 或超时，适配器严格返回 HTTP `413 Request Entity Too Large`。
- **安全认证与网络边界**：网关调用适配器时使用专用的 `X-CheeseWAF-Adapter-Token` 请求头进行校验（严禁通过 `Authorization: Bearer` 传递），并严格校验 `CHEESEWAF_ADAPTER_TRUSTED_PROXY_CIDRS`。

## 契约边界 (Inspection Contract v1) {#contract}

适配器基于 `contracts/inspection/v1` 契约与 CheeseWAF 核心通信：

- **Inline 检查接口**：默认路径为 `/api/v1/adapter/inspect`，接收标准化请求元数据、客户端上下文、TLS 指纹和有界请求体，在设定的时间预算（默认 100ms）内返回决策。
- **核心决策动作**：
  - `allow`：放行请求并转发至上游业务。
  - `block`：阻断请求并返回安全拦截页面或特定状态码。
  - `challenge`：触发人机验证（如 JavaScript 挑战或 CAPTCHA）。
  - `log`：放行请求并记录告警（归一化为观察模式）。
- **异步 Telemetry 接口**：默认路径为 `/api/v1/adapter/telemetry`，限速且尽力而为（Best-Effort）接收事件，不阻塞实时流量链路。

## 网关接入配置示例 {#gateways}

### 1. NGINX `auth_request` 接入

在 NGINX 中利用 `ngx_http_auth_request_module` 模块将子请求交由 `adapterd` 授权：

```nginx
# 业务站点配置
location / {
    auth_request /cheesewaf_auth;
    auth_request_set $waf_status $upstream_status;

    # 授权通过后正常转发上游
    proxy_pass http://backend_cluster;
}

# 适配器授权内部端点
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

### 2. Envoy `ext_authz` 接入

在 Envoy 过滤器链中配置 HTTP 外部鉴权过滤器：

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
当 Envoy 报告 `x-envoy-auth-partial-body: true` 时，适配器会将契约标记为不完整；若核心未明确阻断，适配器仍会强制返回 HTTP 413，避免大包截断绕过检查。
{{% /pageinfo %}}

## 适配器运行与环境变量参考 {#env}

```bash
# 启动本地适配器守护进程
adapterd --listen 127.0.0.1:9080 --core-url http://127.0.0.1:8080
```

| 环境变量 / 命令行参数 | 默认值 | 说明 |
| --- | --- | --- |
| `CHEESEWAF_ADAPTER_LISTEN` / `--listen` | `127.0.0.1:9080` | 适配器本地监听端口与地址 |
| `CHEESEWAF_CORE_URL` / `--core-url` | **必填** | 自托管 CheeseWAF 数据平面或核心检查服务地址 |
| `CHEESEWAF_CORE_INSPECT_PATH` | `/api/v1/adapter/inspect` | 核心 inline 检查 API 路径 |
| `CHEESEWAF_CORE_TELEMETRY_PATH` | `/api/v1/adapter/telemetry` | 核心异步 telemetry 汇报接口 |
| `CHEESEWAF_CORE_HEALTH_PATH` | `/healthz` | 核心健康就绪探测接口（用于 `/readyz` 状态透传） |
| `CHEESEWAF_CORE_TOKEN` | 空 | 适配器向 CheeseWAF 核心通信使用的 Bearer 凭据 |
| `CHEESEWAF_ADAPTER_TOKEN` | 空 | 网关调用适配器所需的专用认证令牌（通过 `X-CheeseWAF-Adapter-Token` 传递） |
| `CHEESEWAF_ADAPTER_TRUSTED_PROXY_CIDRS` | `127.0.0.1/32,::1/128` | 允许透传真实客户端 IP 的对端 CIDR 白名单 |
| `CHEESEWAF_ADAPTER_REQUEST_TIMEOUT` | `100ms` | 单次 inline 检查决策的最长超时时间 |
| `CHEESEWAF_ADAPTER_FAIL_MODE` | `closed` | 核心不可用时的动作：`closed` (返回 503) 或 `open` (返回 204 放行) |
| `CHEESEWAF_ADAPTER_FORWARD_BODY` | `false` | 是否开启请求体转发（开启后受最大字节限制） |
| `CHEESEWAF_ADAPTER_MAX_BODY_BYTES` | `65536` | 请求体最大捕获字节上限（64 KB） |
| `CHEESEWAF_ADAPTER_FORWARD_SENSITIVE_HEADERS` | `false` | 是否显式允许向核心转发包含 Authorization/Cookie 的敏感头 |

## 演进规划 {#roadmap}

1. **协议完善**：扩展流式 Envoy `ext_proc` 适配器，支持大容量请求体流式检测与响应修改。
2. **Kubernetes 集成**：推出轻量级 Kubernetes Sidecar Controller，基于 Pod Annotation 自动完成适配器注入与流量路由。
3. **生态兼容**：完成与 Kong、Apache APISIX、Traefik 等主流云原生 API 网关的官方适配。
