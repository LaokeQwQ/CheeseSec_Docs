---
title: 快速上手
linkTitle: 快速上手
weight: 30
description: 三步快速完成 CheeseWAF 系统初始化、首个站点接入及大模型异步审查配置。
---

先执行 Linux 一键安装。脚本会询问语言、拉取并校验最新稳定版、生成公网 HTTPS 管理入口并输出短期初始化地址，然后按照以下三个核心步骤完成防护：

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | sudo bash
```

语言选择后，安装器会询问应用安装根目录。输入 `/opt/cheesewaf` 可将二进制、Web 资源、配置、数据和日志集中在同一目录；直接回车则使用标准 FHS 布局。自动化变量和路径约束请参考 [Linux 安装指南](../install/linux/)。

{{< nav-cards cols="1" >}}
{{< nav-card title="1. 系统初始化" link="/zh/docs/cheesewaf/tutorial/setup/" icon="fa-solid fa-key" desc="访问 /setup 向导，创建首个系统管理员账号，妥善保存初始化密钥并确认管理网络边界。" />}}
{{< nav-card title="2. 接入首个站点" link="/zh/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="配置对外业务域名、后端上游源站地址，设定初始防护等级为推荐的智能标准等级（3 级）。" />}}
{{< nav-card title="3. 接入大模型审查" link="/zh/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-robot" desc="配置兼容 OpenAI 或 Anthropic 协议的大模型接口，为 ALAP 启用异步智能研判与规则闭环沉淀。" />}}
{{< /nav-cards >}}

{{% pageinfo color="info" %}}
请妥善保管完整 HTTPS 初始化地址。URL fragment 中包含一次性 Token，浏览器会将它转换为 `X-CheeseWAF-Setup-Token` 请求头，初始化完成后立即撤销。目标服务器无法访问 GitHub 时，请从 [发行页](https://github.com/LaokeQwQ/CheeseWAF/releases) 下载带签名的发行包和校验文件，再按离线安装章节操作。

即使尚未配置大模型接入，CheeseWAF 的数据平面依然能基于内置 AST 语义引擎提供全量实时的攻击检测与阻断。未配置 `ai` 参数前，ALAP 异步审查队列将保持待机状态。
{{% /pageinfo %}}
