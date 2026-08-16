# CheeseSec 文档

CheeseSec 产品文档站。
第一棵产品文档树是 [CheeseWAF](https://github.com/LaokeQwQ/CheeseWAF)。

生产地址：`https://docs.cheesesec.com/`

[English](README.md) · [简体中文](README.zh.md)

## 技术栈

- [Hugo Extended](https://gohugo.io/) 0.160.1 或更新。本仓库用 **0.165.0** 构建通过。
- 主题：[OINK](https://github.com/pgsty/oink) `v0.4.1`（已放进 `_vendor/`）
- 这个仓库不需要 Node.js、npm 或 PostCSS

## 本地预览

```bash
hugo server --disableFastRender
```

默认语言是英文（`/`）。
中文在 `/zh/`。

生产构建：

```bash
hugo --gc --minify
```

产物在 `public/`。不要把这个目录提交进 git。

`enableGitInfo` 现在是关的，因为仓库还没有第一次提交。你推上去之后，如果要显示 git 的最后修改时间，可以把 `hugo.yaml` 里这项改成 `true`。

## Cloudflare Pages（控制台要填的项）

关联 GitHub 仓库 `LaokeQwQ/CheeseSec_Docs`。建议项目名：`cheesesec-docs`。

| 设置 | 值 |
| --- | --- |
| 生产分支 | `main` |
| 构建命令 | `hugo --gc --minify` |
| 构建输出目录 | `public` |
| 根目录 | `/`（仓库根） |
| `HUGO_VERSION` | `0.165.0`（Production **和** Preview 都要设；0.164.0 也满足 OINK 下限） |
| `GO_VERSION` | `1.24.4` 或更新（Hugo Module 需要） |
| `SKIP_DEPENDENCY_INSTALL` | `1` |

`hugo.yaml` 里的 `baseURL` 是 `https://docs.cheesesec.com/`。

预览构建应覆盖地址：

```bash
hugo --gc --minify --baseURL "$CF_PAGES_URL"
```

不要把用了 `$CF_PAGES_URL` 的预览产物直接发到生产。
生产必须用规范域名重新构建。

第一次部署成功后，在 Pages 项目里绑定自定义域名 `docs.cheesesec.com`（CNAME 到 `*.pages.dev` 主机名）。

## 相关仓库

- 产品：https://github.com/LaokeQwQ/CheeseWAF
- 营销站：https://github.com/LaokeQwQ/CheeseSec_pages
