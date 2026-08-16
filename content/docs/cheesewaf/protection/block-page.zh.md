---
title: 拦截响应页
linkTitle: 拦截页
weight: 70
description: 配置内置拦截页模板、上传自定义 HTML 响应页及请求追踪编号（Trace ID）机制。
---

当客户端请求被 IP 黑名单、ACL、Bot 挑战或 AST 语义引擎阻断时，CheeseWAF 将返回结构化的拦截响应页面。配置位于 `block_page`，可在 Web 控制台的 **拦截页** 模块进行可视化预览与管理。

## 基础配置示例 {#config}

```yaml
block_page:
  template_id: "minimal"
  custom_enabled: false
  custom_html: ""
```

## 模板管理与实时预览 {#templates}

- **内置模板**：通过 API `GET /api/block-pages/templates` 可查询系统预设的现代拦截模板。
- **安全预览机制**：在控制台中可调用 `POST /api/block-pages/preview` 在沙箱窗口中实时渲染拦截效果，确认无误后再执行全局发布。
- **自定义 HTML**：支持调用 `POST /api/block-pages/upload` 上传企业品牌定制的 HTML 源码，或通过 `DELETE /api/block-pages/custom` 清除并恢复默认模板。

## 请求追踪与安全规范 {#trace-id}

- **全局追踪编号（Trace ID）**：拦截页面中会自动嵌入唯一的请求追踪标识符。终端用户遇到误报反馈时，运维人员可直接在 [监控与日志](../../monitor/) 中根据该编号精准定位原始请求上下文与命中规则链。
- **敏感信息保护**：在编写自定义 HTML 拦截模板时，请勿泄露源站/真实服务器名称/内网 IP 地址或暴露技术栈内部拓扑等敏感信息。
