---
title: Bot 挑战与验证码
linkTitle: Bot 与验证码
weight: 40
description: JS 放行、PoW、滑块、图形验证码、登录验证码和排队室。
---

控制台：**Bot 挑战**。设计挑战的人还可以用 **验证码实验室**。
配置：`protection.bot` 和 `console.login.captcha`。

示例里 `protection.bot.enabled` 默认是 `false`。
站点能完成浏览器挑战之后，再打开它。

## 流量挑战 {#traffic}

| 键 | 作用 |
| --- | --- |
| `js_challenge` | 下发 JS 放行 Cookie |
| `captcha` | JS 之后再加验证码 |
| `captcha_type` | `pow`、`image` 或 `slider` |
| `cookie_name` | 默认 `cheesewaf_js_clearance` |
| `path_prefixes` | 哪些路径要挑战 |
| `exempt_path_prefixes` | 跳过，示例含 `/health` |
| `suspicious_user_agents` | 对 curl、sqlmap、nuclei 等更严 |

不要把 `secret` 写进 git。
让进程在数据目录里生成。

## 挑战种类 {#kinds}

- **PoW / Altcha。** 默认请求头是 `X-CheeseWAF-Altcha`。
- **滑块。** 几何和最短拖动时间在 `slider_captcha_*`。
- **图形。** 长度、尺寸、语音次数限制。
- **行为包。** 曲线描绘、刮开、点图标等实验室类型。先在实验室验证，再放到生产流量上。

自定义素材上传到 `/api/captcha/assets`。
配额和远程源测试在同一页控制台。

## 登录验证码 {#login}

`console.login.captcha` 保护的是 **管理端** 登录，不是数据平面。
示例用滑块，可选再加 PoW。

`console.login.security_entry` 可以用秘密路径和 Cookie 把登录页藏起来。

## 排队室 {#waiting-room}

`waiting_room` 加上 `waiting_room_max_active`，人太多时先排队，而不是立刻丢掉。
另见 [限流](../ratelimit/)。
