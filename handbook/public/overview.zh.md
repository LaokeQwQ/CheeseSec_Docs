{"title": "CheeseSec 插件", "linkTitle": "插件", "weight": 20}

CheeseSec 插件是面向整个 CheeseSec 生态的独立产品，提供统一的插件发现与开发方式。

每个插件支持的宿主、版本和能力，以插件说明与对应宿主文档为准。安装前请同时核对这两部分信息。共享目录不表示所有 CheeseSec 产品都已支持插件安装或运行。

## 浏览插件

直接访问[插件商店](https://store.cheesesec.com/)即可查看已发布插件，无须登录。只有实际发布的条目才可供使用；示例或空目录不代表可安装插件。

程序可以读取 [v1 插件目录](https://store.cheesesec.com/v1/catalog/index.json)和 [v1 stable 更新索引](https://ota.cheesesec.com/v1/channels/stable/index.json)。

## 开发插件

先选择支持插件的宿主，再按该宿主的要求准备包格式与能力声明。插件应提供明确的兼容性信息和使用说明，安装前必须校验包签名。

面向 CheeseWAF 宿主开发时，请阅读其[插件与 CRP 文档](/zh/docs/cheesewaf/plugins/)。这些宿主专用说明不代表其他 CheeseSec 产品具有相同兼容性。
