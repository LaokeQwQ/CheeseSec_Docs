---
title: 添加第一个站点
linkTitle: 第一个站点
weight: 20
description: 给 CheeseWAF 配上域名和上游，防护等级先用 3。
---

在控制台打开 **站点** → **新建站点**。

{{% steps %}}

### 域名 {#domain}

填写客户端已经在用的主机名，例如 `app.example.com`。
CheeseWAF 用 `sites[].domains` 匹配。

### 上游 {#upstream}

填写源站地址，例如 `10.0.0.10:8000`。
多个上游时走站点的 `loadbalance` 策略（默认 `round_robin`）。

### 防护等级 {#paranoia}

第一个生产站点用 **3**。
等级 3 会阻断独立攻击值，夹杂命中先放行，再交给 ALAP 审查。

### 保存 {#save}

保存站点。
进程会热加载站点列表，不用整进程重启。

{{% /steps %}}

把 DNS 或本机 hosts 指到 CheeseWAF 数据平面地址。
先确认流量还能回到源站，再考虑升档。

细节见 [站点与反向代理](../../sites/)。
