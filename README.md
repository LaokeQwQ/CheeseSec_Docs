# CheeseSec Docs

Documentation site for CheeseSec products.
The first product tree is [CheeseWAF](https://github.com/LaokeQwQ/CheeseWAF).

Production URL: `https://docs.cheesesec.com/`

[English](README.md) · [简体中文](README.zh.md)

## Stack

- [Hugo Extended](https://gohugo.io/) 0.160.1 or newer. This tree was built with **0.165.0**.
- Theme: [OINK](https://github.com/pgsty/oink) `v0.4.1` (vendored in `_vendor/`)
- No Node.js, npm, or PostCSS in this repository

## Local preview

```bash
hugo server --disableFastRender
```

English is the default language (`/`).
Chinese is under `/zh/`.

Production build:

```bash
hugo --gc --minify
```

Output is `public/`. Do not commit that directory.

`enableGitInfo` is on, so pages can show last-modified dates from git.

## Cloudflare Pages (fill these in)

Connect GitHub repo `LaokeQwQ/CheeseSec_Docs`. Suggested project name: `cheesesec-docs`.

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Build command | `hugo --gc --minify` |
| Build output directory | `public` |
| Root directory | `/` (repository root) |
| `HUGO_VERSION` | `0.165.0` (set on Production **and** Preview; 0.164.0 also meets OINK’s floor) |
| `GO_VERSION` | `1.26.6` or newer (matches `go.mod`) |
| `SKIP_DEPENDENCY_INSTALL` | `1` |

`baseURL` in `hugo.yaml` is `https://docs.cheesesec.com/`.

Preview builds should override the URL:

```bash
hugo --gc --minify --baseURL "$CF_PAGES_URL"
```

Do **not** publish a preview artifact that used `$CF_PAGES_URL` to production.
Rebuild production with the canonical domain.

After the first successful deploy, attach the custom domain `docs.cheesesec.com` in the Pages project. Point the DNS CNAME to the concrete `<project>.pages.dev` hostname shown by that Pages project; do not use the literal `*.pages.dev` text.

## Related

- Product: https://github.com/LaokeQwQ/CheeseWAF
- Marketing site: https://github.com/LaokeQwQ/CheeseSec_pages

## Documentation and production-build constraints

- CheeseWAF commands, configuration keys, ports, onboarding-token flow, and security defaults must be validated against the current source and UI before publishing the corresponding English and Chinese pages.
- CheeseWAF's `@agent-eyes/agent-eyes`, code-inspector, and `codex-acp` are local development/test tooling only. They must never appear in product release packages, production images, or production examples.
- Source-build instructions must use the repository's `bash scripts/ci/build-web.sh` and a runtime configuration copy rather than writing setup state into the tracked template.
