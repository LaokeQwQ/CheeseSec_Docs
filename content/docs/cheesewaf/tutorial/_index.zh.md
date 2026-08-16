---
title: 快速上手
linkTitle: 快速上手
weight: 30
description: 初始化 CheeseWAF，加上第一个站点，再为 ALAP 接上模型。
---

进程跑起来之后，做这三步。

{{< nav-cards cols="1" >}}
{{< nav-card title="1. 初始化" link="/zh/docs/cheesewaf/tutorial/setup/" icon="fa-solid fa-key" desc="打开 /setup，创建第一个管理员，保存生成的密钥。" />}}
{{< nav-card title="2. 添加站点" link="/zh/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="域名、上游、防护等级 3。" />}}
{{< nav-card title="3. 接模型" link="/zh/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-robot" desc="给 ALAP 配兼容 OpenAI 的接口。第一步可以先不配。" />}}
{{< /nav-cards >}}

没有模型，数据平面也能工作。
配好 `ai` 之前，ALAP 审查队列是空的。
