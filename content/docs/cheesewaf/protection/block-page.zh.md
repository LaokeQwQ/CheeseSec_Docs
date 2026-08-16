---
title: 拦截页
linkTitle: 拦截页
weight: 70
description: 内置模板、自定义 HTML，以及预览窗口。
---

配置：`block_page`。
控制台：**拦截页**。
REST：`/api/block-pages/*`。

```yaml
block_page:
  template_id: "minimal"
  custom_enabled: false
  custom_html: ""
```

`GET /api/block-pages/templates` 列出内置模板。
`POST /api/block-pages/preview` 和 `/block-pages/preview` 窗口可以预览，不会直接发布。

用 `POST /api/block-pages/upload` 上传自定义 HTML。
用 `DELETE /api/block-pages/custom` 删掉它。

拦截页可以带 **追踪编号**。
打开 [日志详情](../../monitor/) 时，把这个编号交给运维。
自定义 HTML 里不要写源站主机名或内网 IP。
