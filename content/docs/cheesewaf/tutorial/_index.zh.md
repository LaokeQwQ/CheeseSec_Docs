---
title: 快速上手
linkTitle: 快速上手
weight: 30
description: 完成安装、初始化、验证，并在切换生产前接入一个测试站点。
---

本页针对单机路径，顺序与产品工作流一致：**安装 → 初始化 → 验证 → 接入**。

## 最短路径 {#short-version}

1. 执行 Linux 一键安装；服务器无法访问 GitHub 时，安装经过校验的发行包。
2. 打开安装器输出的 HTTPS 初始化地址，创建首个管理员。
3. 确认服务和就绪探针正常。
4. 接入一个测试站点，经数据面监听器发送请求。

Web 控制台和确定性数据面防护不依赖大模型即可运行。基础请求链路正常后，再配置 ALAP 异步审查。

## 第一步：安装 {#install}

在具备 `sudo` 权限的 Linux 主机上执行：

```bash
curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | sudo bash
```

安装器会询问语言和可选的应用安装根目录，下载并校验最新稳定版，在可用时启动 systemd 服务，并输出初始化地址。输入 `/opt/cheesewaf` 可将二进制、Web 资源、配置、数据和日志集中在同一目录；直接回车则使用标准 FHS 布局。需要指定版本时设置 `CHEESEWAF_RELEASE=vX.Y.Z[-beta]`。

请妥善保管完整初始化地址。URL fragment 中包含一次性 Token，浏览器会将它转换为 `X-CheeseWAF-Setup-Token` 请求头，初始化完成后立即撤销。目标服务器无法访问 GitHub 时，请从[发行页](https://github.com/LaokeQwQ/CheeseWAF/releases)下载发行包和校验文件，再按 [Linux 安装指南](../install/linux/)的离线章节操作。Docker 部署请阅读 [Docker 指南](../install/docker/)。

## 第二步：初始化 {#setup}

打开安装器输出的 `https://` 地址。初始化路由固定为 `/setup`：

```text
https://PUBLIC_IP:9443/setup#setup_token=ONE_TIME_TOKEN
```

创建首个管理员，并把管理端口限制在受信管理网络内。[系统初始化](setup/)详细说明用户名和密码规则、一次性 Token 处理，以及公开管理面需要满足的条件。如果管理员尚未创建就丢失了地址，可在服务器上重置 Token：

```bash
sudo -u cheesewaf /usr/local/bin/cheesewaf \
  --config /etc/cheesewaf/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf \
  setup token reset --show
```

## 第三步：验证 {#verify}

按 [Linux 安装指南](../install/linux/#verify)执行服务和就绪检查。预期状态如下：

```text
systemd：已启用且 active
管理面：https://127.0.0.1:9443 已就绪
数据面：127.0.0.1:8080 可用于测试站点
```

如果检查失败，先根据 [Linux 故障排查表](../install/linux/#troubleshooting)按症状处理，不要直接修改大量配置。

## 第四步：接入 {#onboard}

{{< nav-cards cols="2" >}}
{{< nav-card title="首个站点" link="/zh/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="配置业务域名、上游源站、初始防护策略，并发送安全测试请求。" />}}
{{< nav-card title="接入大模型" link="/zh/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-brain" desc="可选接入兼容 OpenAI 或 Anthropic 的接口，启用异步审查。" />}}
{{< /nav-cards >}}

在源站、健康检查、访问控制、日志和回滚流程完成验证前，不要把生产 DNS 切换到 WAF。

{{% pageinfo color="info" %}}
即使尚未配置大模型接入，CheeseWAF 的数据平面依然能基于内置 AST 语义引擎提供即时的攻击检测与阻断。未配置 `ai` 参数前，ALAP 异步审查队列将保持待机状态。
{{% /pageinfo %}}

## 下一步 {#next-steps}

- 阅读[核心概念](../concepts/)，了解数据面与管理面的边界。
- 在[安全防护](../protection/)中配置 ACL、IP 控制、挑战和限流。
- 在启用公网管理、外部存储、备份或升级前，先阅读[运维](../operations/)。
