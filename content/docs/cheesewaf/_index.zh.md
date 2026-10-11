---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: 面向自托管场景的 Web 应用防火墙，提供单二进制数据面、管理控制台和异步威胁审查。
---

CheeseWAF 是一个自托管反向代理 WAF。确定性的请求检测运行在数据面，可选的大模型审查在请求链路之外异步执行，因此正常业务流量不依赖外部模型才能提供防护。

{{% pageinfo color="info" %}}
最短可用路径是：执行 Linux 一键安装，打开脚本输出的 HTTPS 初始化地址，完成 `/setup`，再接入一个测试站点。发行包请从 [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) 获取；项目协议见 [源码仓库中的 Apache License 2.0](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE)。
{{% /pageinfo %}}

## 选择入口 {#start-here}

根据当前任务选择文档：

{{< nav-cards cols="2" >}}
{{< nav-card title="快速上手" link="/zh/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="完成安装、控制台初始化、服务检查，并接入一个测试站点。" />}}
{{< nav-card title="Linux（推荐）" link="/zh/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="使用一键脚本或校验后的发行包安装，并以 systemd 服务运行。" />}}
{{< nav-card title="Docker" link="/zh/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="使用明确的端口和数据挂载，部署隔离的测试或 Compose 环境。" />}}
{{< nav-card title="生产运维" link="/zh/docs/cheesewaf/operations/" icon="fa-solid fa-shield-halved" desc="检查网络边界、存储、备份、升级和离线运行要求。" />}}
{{< /nav-cards >}}

## 五分钟路径 {#five-minute-path}

1. 准备受支持的 Linux 主机、`sudo` 权限、足够的磁盘空间，以及访问 `9443` 管理端口的方式。
2. 执行一键安装。脚本会下载并校验最新稳定版，在可用时安装 systemd 服务，并输出 HTTPS 初始化地址。服务器无法访问 GitHub 时，改走 [Linux 安装指南](install/linux/) 中经过校验的离线安装流程。
3. 打开脚本输出的 HTTPS 地址，创建首个管理员。一次性 Token 不要留在工单、截图、Shell 历史或日志中。
4. 继续阅读[快速上手](tutorial/)，先接入测试站点，再切换生产 DNS。

安装器会创建专用的 `cheesewaf` 系统用户，复制 Web 控制台资源；仅当运行时配置不存在时才复制配置模板；启用管理面 HTTPS；并默认将 systemd 单元安装到 `/etc/systemd/system`。它不会覆盖已有配置。

## 功能范围 {#capabilities}

- **数据面：** 反向代理、请求规范化、AST 语义检测、ACL、IP 与指纹控制、限流和 Bot 挑战。
- **管理面：** Web 控制台、REST API、CLI/TUI 工作流、初始化向导、RBAC、审计记录和健康探针。
- **异步审查：** 可选的 ALAP 异步审查，用于处理边界样本；审查队列在请求链路之外，不能当作实时拦截路径。
- **存储选择：** 默认 `temporary` 档位使用本地运行时存储。生产环境必须显式提供所需外部存储，不得静默回退。
- **适配器与插件：** adapterd 可接入现有网关；CRP 用于签名离线资源包。启用第三方包前请先阅读[插件与 CRP](plugins/)。
- **离线运行：** 可使用发行包、校验文件、签名资源和本地运行时数据，在不依赖外部模型的情况下维护数据面。

## 默认网络边界 {#default-listeners}

| 平面 / 服务 | 默认地址 | 用途 |
| --- | --- | --- |
| 数据面 | `http://127.0.0.1:8080` | 业务流量检测与反向代理 |
| 管理面 | `https://PUBLIC_IP:9443/setup` → `https://PUBLIC_IP:9443/SECURITY_ENTRY` | 初始化固定使用 `/setup` 和一次性 Token；完成后由生成的安全入口签发访问 Cookie 并跳转登录 |
| 集群面 | `https://127.0.0.1:9444` | 启用集群时使用的可选 mTLS 节点互联 |
| 本地控制器 | `http://127.0.0.1:17943` | Windows 与 macOS 桌面辅助控制器 |

一键安装器会把管理监听绑定到所有网卡并启用 HTTPS，用一次性 Token 和生成的安全入口保护首次初始化。开放端口前，应把 `9443` 限制在受信管理网络内。发布模板和初始化向导默认使用 `0.0.0.0:9443`，并启用 `server.admin_public: true`。完全省略 `server` 相关键时，才回退到加载器的兜底值 `127.0.0.1:9443`。公开管理面仍必须启用管理 TLS、配置有效证书，并配套外部访问控制。不要把 `/setup` 或管理端口直接暴露到公网来替代这些控制。

## 继续阅读

{{< nav-cards cols="2" >}}
{{< nav-card title="核心概念" link="/zh/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="了解请求生命周期、管理边界、存储档位和执行顺序。" />}}
{{< nav-card title="安全防护" link="/zh/docs/cheesewaf/protection/" icon="fa-solid fa-lock" desc="配置语义检测、ACL、IP 控制、挑战和限流。" />}}
{{< nav-card title="网关适配器" link="/zh/docs/cheesewaf/adapters/" icon="fa-solid fa-network-wired" desc="通过带认证的适配器契约接入 NGINX 或 Envoy。" />}}
{{< nav-card title="配置参考" link="/zh/docs/cheesewaf/config/" icon="fa-solid fa-sliders" desc="查询支持的配置键、默认值、校验规则和运行时边界。" />}}
{{< /nav-cards >}}
