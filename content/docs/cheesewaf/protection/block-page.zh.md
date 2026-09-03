---
title: 拦截响应页与 HTML 安全清洗
linkTitle: 拦截页
weight: 70
description: 配置内置拦截页模板、自定义 HTML 响应页、SanitizeBlockPageHTML 存储型 XSS 防御与请求追踪编号（Trace ID）机制。
---

当客户端请求被 IP 黑名单、ACL 访问控制、Bot 挑战或 AST 语义引擎阻断时，CheeseWAF 将向客户端返回结构化的拦截响应页面。配置位于 `block_page`，可在 Web 控制台的 **拦截页** 模块进行可视化预览、模板切换与源码定制。

## 基础配置示例 {#config}

```yaml
block_page:
  template_id: "minimal"
  custom_enabled: false
  custom_html: ""
```

## 模板管理与实时预览 {#templates}

- **内置现代模板**：通过 API `GET /api/block-pages/templates` 可查询系统预设的现代拦截模板。
- **沙箱安全预览**：在控制台中可调用 `POST /api/block-pages/preview` 在沙箱窗口中实时渲染拦截效果，确认无误后再执行全局发布。
- **自定义 HTML 替换**：支持调用 `POST /api/block-pages/upload` 上传企业品牌定制的 HTML 源码，或通过 `DELETE /api/block-pages/custom` 清除并恢复默认模板。

## 自定义 HTML 安全清洗规范（`SanitizeBlockPageHTML`） {#sanitization}

为了防止管理员误上传或遭受供应链投毒导致自定义拦截页引入存储型 XSS（Stored XSS）与恶意跳转风险，CheeseWAF 在保存与渲染自定义 HTML 时，强制经过内置的 `SanitizeBlockPageHTML` 净化引擎处理：

### 1. 标签与结构白名单

仅允许安全的语义排版与布局标签：
- **容器与结构**：`html`、`head`、`body`、`title`、`main`、`section`、`header`、`footer`、`div`、`span`
- **排版与文本**：`h1`~`h6`、`p`、`strong`、`em`、`b`、`i`、`small`、`pre`、`code`、`br`、`hr`
- **列表与表格**：`ul`、`ol`、`li`、`table`、`thead`、`tbody`、`tfoot`、`tr`、`th`、`td`
- **媒体与链接**：`a`、`img`、`style`、`meta`

### 2. 主动脚本与事件剥离

- **杜绝内联脚本**：所有 `<script>` 标签与注释节点会被完全剔除。
- **剥离 DOM 事件处理器**：所有以 `on` 开头的属性（如 `onclick`、`onload`、`onerror` 等）一律强制清除。
- **禁用表单劫持**：严格过滤 `formaction`、`action` 与 `method` 属性，防止伪造表单收集受害者凭据。
- **防恶意重定向**：`<meta>` 标签仅允许安全的 `charset` 属性，严格过滤 `http-equiv="refresh"` 等强制跳转指令。

### 3. CSS 样式净化与外部引用拦截

- `<style>` 标签及内联 `style` 属性中，严格过滤 `@import` 外部样式加载。
- 自动屏蔽包含 `javascript:`、`vbscript:`、`expression(`、`behavior:` 及 `-moz-binding` 等危险 CSS 表达式。

### 4. URL 协议安全限制

- 对于 `href` 与 `src` 属性，仅允许 `http`、`https`、`mailto`、`tel` 协议。
- 对于 `<img>` 标签，额外允许安全的 Base64 图片数据（`data:image/*;base64,...`），严禁非图片类型的数据 URI。

## 请求追踪与安全规范 {#trace-id}

- **全局追踪编号（Trace ID）**：拦截页面中会自动嵌入唯一的请求追踪标识符。终端用户遇到误报反馈时，运维人员可直接在 [监控与日志](../../monitor/) 中根据该编号精准定位原始请求上下文与命中规则链。
- **敏感信息保护**：在编写自定义 HTML 拦截模板时，请勿泄露真实源站名称、内网 IP 地址或内部技术栈拓扑等敏感信息。
