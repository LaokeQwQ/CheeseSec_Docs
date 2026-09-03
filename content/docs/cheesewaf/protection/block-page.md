---
title: Block Pages & HTML Sanitization
linkTitle: Block Pages
weight: 70
description: Configure responsive block page templates, upload custom HTML designs, SanitizeBlockPageHTML anti-XSS policy, and Trace ID request tracking.
---

When an inbound request is blocked by IP reputation, ACLs, Bot defense, or the AST semantic engine, CheeseWAF renders a structured block page response. Managed under `block_page`, templates can be visually previewed, edited, and deployed within the **Block Pages** view in the Web Console.

## Basic Configuration {#config}

```yaml
block_page:
  template_id: "minimal"
  custom_enabled: false
  custom_html: ""
```

## Template Lifecycle & Sandboxed Previews {#templates}

- **Built-In Modern Designs**: Enumerate built-in response templates via `GET /api/block-pages/templates`.
- **Sandboxed Rendering**: Preview custom templates safely in an isolated iframe (`POST /api/block-pages/preview`) prior to publishing globally.
- **Custom HTML Uploads**: Call `POST /api/block-pages/upload` to upload custom branding, or revert to defaults via `DELETE /api/block-pages/custom`.

## HTML Sanitization Standards (`SanitizeBlockPageHTML`) {#sanitization}

To prevent custom block pages from introducing Stored XSS or phishing vectors, CheeseWAF enforces strict sanitization on all custom HTML inputs before persistence:

### 1. Tag Whitelist

Only safe layout and typographic tags are permitted:
- **Structure**: `html`, `head`, `body`, `title`, `main`, `section`, `header`, `footer`, `div`, `span`
- **Typography**: `h1`–`h6`, `p`, `strong`, `em`, `b`, `i`, `small`, `pre`, `code`, `br`, `hr`
- **Lists & Tables**: `ul`, `ol`, `li`, `table`, `thead`, `tbody`, `tfoot`, `tr`, `th`, `td`
- **Assets & Style**: `a`, `img`, `style`, `meta`

### 2. Active Script & Event Stripping

- **Zero Scripts**: All `<script>` elements and HTML comments are completely removed.
- **Event Handler Neutralization**: Attributes prefixed with `on` (e.g., `onclick`, `onload`, `onerror`) are excised.
- **Form Action Protection**: `formaction`, `action`, and `method` attributes are stripped to prevent credential-harvesting forms.
- **Redirect Prevention**: `<meta>` elements only permit the `charset` attribute; `http-equiv="refresh"` and arbitrary header injections are rejected.

### 3. CSS Style Sanitization

- `@import` rules inside `<style>` tags or inline `style` attributes are stripped.
- Risky CSS primitives such as `javascript:`, `vbscript:`, `expression(`, `behavior:`, and `-moz-binding` are removed.

### 4. URL Scheme Controls

- The `href` and `src` attributes are strictly restricted to `http`, `https`, `mailto`, and `tel`.
- `<img>` elements additionally support embedded Base64 image payloads (`data:image/*;base64,...`); arbitrary data URIs are discarded.

## Traceability & Operational Guidelines {#trace-id}

- **Global Trace ID Correlation**: Block pages dynamically display a unique request `traceId`. When users report false positives, operators can correlate the exact rule evaluation chain under [Monitoring & Logs](../../monitor/).
- **Information Leakage Prevention**: Custom block templates should avoid revealing backend hostnames, private IPs, or internal technology stacks to external clients.
