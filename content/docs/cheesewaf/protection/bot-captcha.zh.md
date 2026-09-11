---
title: Bot 挑战与人机验证码
linkTitle: Bot 与验证码
weight: 40
description: 配置无感 JavaScript 挑战、PoW 工作量证明、滑块与图形验证码、管理端登录防护及排队室削峰机制。
---

现代网络中的复杂请求中，往往可能伴随着AI爬虫、撞库攻击及自动化扫描工具等恶意流量，CheeseWAF 提供了多层次的人机识别与流量挑战机制。可通过 Web 控制台的 **Bot 挑战** 与 **验证码实验室** 进行可视化调试，或通过 `protection.bot` 与 `console.login.captcha` 进行配置。

## 业务流量挑战配置 {#traffic}

```yaml
protection:
  bot:
    enabled: false
    js_challenge: true
    captcha: true
    captcha_type: "slider"
    cookie_name: "cheesewaf_js_clearance"
    path_prefixes: ["/login", "/register", "/api/order"]
    exempt_path_prefixes: ["/health", "/static"]
    suspicious_user_agents: ["curl", "sqlmap", "nuclei"]
```

| 配置参数 | 说明 |
| --- | --- |
| `js_challenge` | 启用无感 JavaScript 挑战，验证通过后下发 Clearance Cookie |
| `captcha` | 在 JS 挑战基础上叠加显式人机验证码 |
| `captcha_type` | 验证码形态，支持 `PoW`（工作量证明）、`Slider`（滑动拼图）或 `Image`（图形字符） |
| `cookie_name` | 验证通过后写入客户端的 Cookie 名称，默认为 `cheesewaf_js_clearance` |
| `path_prefixes` | 强制触发挑战的 URI 路径前缀列表 |
| `exempt_path_prefixes` | 豁免挑战的白名单路径前缀（如健康检查接口 `/health`） |
| `suspicious_user_agents` | 子串包含匹配的可疑客户端标识（User-Agent 包含该值即命中），命中后升级为人机验证 |

{{% pageinfo color="warning" %}}
不要把挑战签名的 `secret` 值提交到版本库。配置为空或仍是已知占位符时，初始化/启动流程会按部署方式生成强随机运行时密钥，并写入受保护的运行时配置或运行时密钥文件；不能假定它只存在于内存中。请严格保护运行时路径和文件权限。
{{% /pageinfo %}}

## 验证码类型与交互形式 {#kinds}

- **工作量证明（PoW / Altcha）**：客户端后台在浏览器中执行哈希碰撞计算并通过请求头 `X-CheeseWAF-Altcha` 提交结果，对合法用户完全无感且大幅增加攻击者并发成本。
- **滑动拼图（Slider）**：包含几何轨迹分析与最短拖动时间校验（由 `slider_captcha_*` 参数定义），有效防御机械脚本。
- **图形验证码（Image）**：支持自定义字符长度、图片尺寸及语音辅助验证次数限制。
- **实验性行为验证**：包括轨迹绘制、刮刮卡与图标点选等实验室题型，建议在控制台 **验证码实验室** 中验证业务适配性后再推向生产。

通过 `/api/captcha/assets` 端点支持上传企业定制背景图与图标素材。

## 管理端登录防护 {#login}

配置项 `console.login.captcha` 专用于保护 **Web 管理控制台登录入口**（与数据平面业务隔离），支持滑块验证码与二次 PoW 校验。

源码模板默认开启管理端登录滑块验证码（`console.login.captcha.enabled: true`）。因此初始化完成后首次登录时，除用户名和密码外还必须完成浏览器中的人机验证。测试环境如需关闭，可在运行时配置副本中设置 `console.login.captcha.enabled: false` 并重启；生产环境不建议为了绕过验收而关闭该保护。

此外，可启用 `console.login.security_entry` 为管理登录配置隐藏的混淆路径与前置 Cookie 密钥，防止管理端被公网自动化探测。

## 排队室机制（Waiting Room） {#waiting-room}

通过配置 `waiting_room: true` 并设定 `waiting_room_max_active` 活跃用户上限，可在突发秒杀或流量激增时将超出承载能力的客户端优雅调度至排队等待页面。排队室只有在全局 `protection.policy.bot_cc` 未设为 `off` 且其 action 为 `challenge` 时才会生效；仅打开站点级排队室开关并不足够。详见 [流量限流](../ratelimit/)。
