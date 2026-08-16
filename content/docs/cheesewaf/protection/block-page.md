---
title: Block pages
linkTitle: Block pages
weight: 70
description: Built-in templates, custom HTML, and a preview window.
---

Config: `block_page`.
Console: **Block pages**.
REST: `/api/block-pages/*`.

```yaml
block_page:
  template_id: "minimal"
  custom_enabled: false
  custom_html: ""
```

`GET /api/block-pages/templates` lists built-in templates.
`POST /api/block-pages/preview` and the `/block-pages/preview` window show the rendered page without publishing it.

Upload custom HTML with `POST /api/block-pages/upload`.
Delete it with `DELETE /api/block-pages/custom`.

A block page can include a **trace id**.
Give that id to the operator when you open a [log detail](../../monitor/).
Do not put origin hostnames or internal IPs in custom HTML.
