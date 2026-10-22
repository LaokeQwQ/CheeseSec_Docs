{"title": "CheeseSec 插件", "linkTitle": "插件", "weight": 20}

CheeseSec 插件是面向整个 CheeseSec 生态的独立产品，提供统一的插件发现与开发方式。

每个插件支持的宿主、版本和能力，以插件说明与对应宿主文档为准。安装前请同时核对这两部分信息。共享目录不表示所有 CheeseSec 产品都已支持插件安装或运行。

## 浏览插件

直接访问[插件商店](https://store.cheesesec.com/)即可查看已发布插件，无须登录。只有实际发布的条目才可供使用；示例或空目录不代表可安装插件。

程序可以读取 [v1 插件目录](https://store.cheesesec.com/v1/catalog/index.json)和 [v1 stable 更新索引](https://ota.cheesesec.com/v1/channels/stable/index.json)。

## Hello CheeseSec 示例

`Hello CheeseSec 0.1.0` 演示插件启动、健康检查、模式晋升和停止，不检测攻击、不采集数据，也不提供防护能力。

商店分别提供 Linux amd64 与 macOS arm64 两个包。仅支持相应平台和兼容的 CheeseWAF 进程插件宿主；其他 CheeseSec 产品须实现兼容宿主后才能运行。上架和下载不代表自动安装或激活。

包使用 Ed25519 双签名。安装前核对商店中包的 SHA-256、签名以及宿主要求；从可信渠道确认发布公钥，不能仅因包与公钥来自同一下载站就信任未知发布者。

[浏览并下载示例](https://store.cheesesec.com/) · [下载可重复构建的源码](https://res.cheesesec.com/sha256/e088a10aee6e24ca728f15584477a440a35df433e1712dced8671f476aaba4d3/hello-cheesesec-source-0.1.0.tar.gz)

## 开发插件

先选择支持插件的宿主，再按该宿主的要求准备包格式与能力声明。插件应提供明确的兼容性信息和使用说明，安装前必须校验包签名。

面向 CheeseWAF 宿主开发时，请阅读其[插件与 CRP 文档](/zh/docs/cheesewaf/plugins/)。这些宿主专用说明不代表其他 CheeseSec 产品具有相同兼容性。
