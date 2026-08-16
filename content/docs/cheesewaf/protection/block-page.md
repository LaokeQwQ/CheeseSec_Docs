---
title: Block Response Pages
linkTitle: Block Pages
weight: 70
description: Configure built-in block templates, upload branded custom HTML pages, and utilize Trace ID tracking mechanisms.
---

When client requests are blocked by IP access controls, ACLs, Bot challenges, or the AST semantic engine, CheeseWAF renders a structured block response page. Configure settings under `block_page`, or manage templates visually in the Web console under **Block Pages**.

## Base Configuration {#config}

```yaml
block_page:
  template_id: "minimal"
  custom_enabled: false
  custom_html: ""
```

## Template Management & Live Sandbox Preview {#templates}

- **Built-in Templates**: Query pre-bundled responsive block templates via `GET /api/block-pages/templates`.
- **Sandbox Preview**: Invoke `POST /api/block-pages/preview` to render and inspect block layouts within an isolated preview modal before publishing globally.
- **Custom HTML**: Upload custom branded HTML templates via `POST /api/block-pages/upload`, or revert to factory defaults using `DELETE /api/block-pages/custom`.

## Request Trace ID & Security Best Practices {#trace-id}

- **Global Trace ID Embedding**: Block pages automatically embed a unique `traceId`. When users report false-positive blockages, operators can search this ID directly in [Monitoring & Logs](../../monitor/) to view exact rule trigger chains.
- **Data Leak Prevention**: When authoring custom HTML block templates, never hardcode origin server hostnames, internal IP addresses, or expose infrastructure topology.
