---
title: 快速上手
linkTitle: 快速上手
weight: 30
description: 三步快速完成 CheeseWAF 系统初始化、首个站点接入及大模型异步审查配置。
---

在完成服务安装与启动后，按照以下三个核心步骤即可快速建立完整的 Web 安全防护能力：

{{< nav-cards cols="1" >}}
{{< nav-card title="1. 系统初始化" link="/zh/docs/cheesewaf/tutorial/setup/" icon="fa-solid fa-key" desc="访问 /setup 向导，创建首个系统管理员账号，妥善保存初始化密钥并确认管理网络边界。" />}}
{{< nav-card title="2. 接入首个站点" link="/zh/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="配置对外业务域名、后端上游源站地址，设定初始防护等级为推荐的智能标准等级（3 级）。" />}}
{{< nav-card title="3. 接入大模型审查" link="/zh/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-robot" desc="配置兼容 OpenAI 或 Anthropic 协议的大模型接口，为 ALAP 启用异步智能研判与规则闭环沉淀。" />}}
{{< /nav-cards >}}

{{% pageinfo color="info" %}}
即使尚未配置大模型接入，CheeseWAF 的数据平面依然能基于内置 AST 语义引擎提供全量实时的攻击检测与阻断。未配置 `ai` 参数前，ALAP 异步审查队列将保持待机状态。
{{% /pageinfo %}}
