---
title: 问题反馈与安全报告
linkTitle: 反馈与支持
weight: 210
description: 提交功能建议、日常缺陷反馈及严重安全漏洞的沟通渠道与响应规范。
---

CheeseSec 鼓励社区参与和技术反馈。根据问题性质的不同，请选用相应的沟通渠道：

## 常规交流与缺陷反馈 {#general-feedback}

### 1. GitHub Issues

对于软件运行缺陷（Bug）、异常报错、功能改进建议或技术文档错漏，推荐直接在对应的 GitHub 项目仓库中提交 Issue：

| 项目领域 | 仓库与反馈地址 | 适用场景 |
| --- | --- | --- |
| **核心程序与引擎** | [LaokeQwQ/CheeseWAF Issues](https://github.com/LaokeQwQ/CheeseWAF/issues) | WAF 服务端、数据平面转发、语义引擎、CLI 工具与 Web 控制台相关问题 |
| **网关适配器** | [LaokeQwQ/CheeseWAF-Adapters Issues](https://github.com/LaokeQwQ/CheeseWAF-Adapters/issues) | NGINX `auth_request`、Envoy `ext_authz` 及 `adapterd` 守护进程问题 |
| **插件生态与规范** | [LaokeQwQ/CheeseSec_Plugin Issues](https://github.com/LaokeQwQ/CheeseSec_Plugin/issues) | CRP 插件规范、元数据清单与发布注册相关问题 |
| **技术文档** | [LaokeQwQ/CheeseSec_Docs Issues](https://github.com/LaokeQwQ/CheeseSec_Docs/issues) | 官方文档内容纠错、结构优化与翻译对齐建议 |

{{% pageinfo color="info" %}}
**提交建议**：提交 Issue 时，请尽量附带操作系统环境、软件版本号（`cheesewaf version`）、部署方式（Linux 服务或 Docker）及最小可复现步骤。请注意脱敏，切勿在公开 Issue 中包含数据库凭据、API Token 或明文私钥。
{{% /pageinfo %}}

### 2. 邮件交流

对于不便通过公开 Issue 讨论的一般性问题、技术交流或部署咨询，可通过电子邮件直接沟通：

- **联系邮箱**：`coqimax@gmail.com`

---

## 严重缺陷与安全漏洞报告 {#security-reporting}

CheeseSec 高度重视软件安全。若在 CheeseWAF 核心系统或其生态组件中发现安全漏洞、防护绕过或严重稳定性缺陷，请遵循**负责任的漏洞披露原则（Responsible Disclosure）**，避免在公开公共渠道（如 GitHub Issues、社交网络或公开群聊）中直接发布漏洞细节。

### 专有安全邮箱 {#security-contact}

- **漏洞报告专用邮箱**：`sec@cheesesec.com`

### 适用报告范围

包括但不限于以下威胁场景：
- 远程代码执行（RCE）或任意命令执行缺陷
- 管理平面鉴权绕过、权限越权或 JWT/Session 校验失效
- AST 语义检测引擎或核心防护规则的通用绕过（Bypass）手段
- 内存溢出、死锁或非预期资源耗尽引发的高危拒绝服务（DoS）
- 敏感配置、凭据或未脱敏数据的泄露隐患

### 安全报告建议包含的信息

为协助安全团队快速复核并定位问题，发送报告时建议包含以下要素：
1. **漏洞简述与影响面**：漏洞类型、影响的模块或接口，以及评估危害等级。
2. **受影响版本**：受影响的 Release 版本号或 Git Commit 哈希。
3. **概念验证（PoC）**：清晰、完整的重现步骤，包括请求报文、测试脚本或关键配置。
4. **利用条件与前置要求**：触发漏洞所需的前置配置项、权限要求或网络拓扑。
5. **修复建议（可选）**：如有可行的缓解规避措施或补丁思路，欢迎一同提供。

### 响应与处置流程

1. **报告确认**：安全团队在收到 `sec@cheesesec.com` 来信后，将及时给予确认并建立专门跟踪通道。
2. **复现与定级**：技术团队在独立安全环境中验证 PoC，确认威胁影响并确定修复优先级。
3. **补丁发布与披露**：完成代码修复并经过充分测试后，团队将发布安全补丁版本及相应安全公告（Security Advisory）。在此之前，请协助保持漏洞信息的保密性。
