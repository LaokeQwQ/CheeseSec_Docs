# CheeseSec 官方文档站

本仓库为 CheeseSec 安全产品的官方文档源码库，首期收录 [CheeseWAF](https://github.com/LaokeQwQ/CheeseWAF) 企业级 Web 应用防火墙的产品与运维手册。

- **生产站点**：[https://docs.cheesesec.com/](https://docs.cheesesec.com/)
- **语言切换**：[English](README.md) · [简体中文](README.zh.md)

## 技术栈与依赖

- **静态站点生成器**：[Hugo Extended](https://gohugo.io/) 0.160.1 或更高版本（推荐使用 **0.165.0** 构建）。
- **文档主题**：[OINK](https://github.com/pgsty/oink) `v0.4.1`（已固化于 `_vendor/` 目录，无需额外拉取）。
- **轻量化设计**：文档构建无需依赖 Node.js、npm 或 PostCSS 环境。

## 本地开发与预览

使用 Hugo 启动本地调试服务：

```bash
hugo server --disableFastRender
```

- 默认英文文档：`http://localhost:1313/`
- 简体中文文档：`http://localhost:1313/zh/`

生产环境静态文件编译：

```bash
hugo --gc --minify
```

编译产物将输出至 `public/` 目录。请注意，该目录已被 `.gitignore` 忽略，请勿将其提交至 Git 仓库。

## Cloudflare Pages 部署配置

在 Cloudflare Pages 控制台中关联 GitHub 仓库 `LaokeQwQ/CheeseSec_Docs`，建议项目名称设置为 `cheesesec-docs`，并配置以下构建参数：

| 配置项 | 参数值 | 说明 |
| --- | --- | --- |
| **生产分支** | `main` | 主分支触发生产部署 |
| **构建命令** | `hugo --gc --minify` | 生产静态编译命令 |
| **构建输出目录** | `public` | 产物目录 |
| **根目录** | `/` | 仓库根路径 |
| **`HUGO_VERSION`** | `0.165.0` | 环境变量（Production 与 Preview 环境均需设置） |
| **`GO_VERSION`** | `1.24.4` | Hugo 模块解析所需的最低 Go 版本 |
| **`SKIP_DEPENDENCY_INSTALL`** | `1` | 跳过默认依赖安装 |

### 预览环境构建说明

`hugo.yaml` 中的生产 `baseURL` 默认配置为 `https://docs.cheesesec.com/`。针对 Cloudflare Pages 的 Preview 预览环境，可通过覆盖 `baseURL` 进行构建：

```bash
hugo --gc --minify --baseURL "$CF_PAGES_URL"
```

部署完成后，在 Cloudflare Pages 项目设置中绑定自定义域名 `docs.cheesesec.com`（添加指向 `*.pages.dev` 的 CNAME 记录即可）。

## 生态与相关仓库

- **产品源码**：[LaokeQwQ/CheeseWAF](https://github.com/LaokeQwQ/CheeseWAF)
- **品牌官网**：[LaokeQwQ/CheeseSec_pages](https://github.com/LaokeQwQ/CheeseSec_pages)
