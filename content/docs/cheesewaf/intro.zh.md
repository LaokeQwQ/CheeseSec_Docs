---
title: CheeseWAF 怎么工作
linkTitle: 介绍
weight: 10
description: 数据平面和 ALAP 怎么分工，为什么请求不会同步送给模型，以及一个二进制里有什么。
---

传统基于正则的 WAF 依赖很大的特征库。
维护贵，编码和包装也容易绕过。

每个请求都同步调用大语言模型，会加上藏不住的网络延迟。

CheeseWAF 把工作拆开。

## 两个平面 {#two-planes}

### 数据平面 {#data-plane}

接收 HTTP、HTTPS 或 HTTP/3 的进程按这个顺序处理：

1. IP、地理位置、客户端软指纹
2. Bot 挑战、限流、排队室
3. 对解码后的参数值做语义分析
4. 反向代理到配置的上游

这条路径必须快。
它不会等远程模型。

### 管理平面 {#control-plane}

管理监听上有：

- `/setup` 初始化向导
- Web 控制台
- `/api` 下的 REST 接口
- 可选的 Prometheus 指标

不要把 `server.admin_public` 打开，除非同时开了 TLS，并且限制谁能访问这个端口。

### ALAP {#alap}

客户端已经拿到响应之后，CheeseWAF 可以把这些样本入队：

- 防护等级 5 下被阻断的独立命中
- 等级 2～4 下放行的夹杂命中
- 引擎标成待审查的其他边界样本

后台 worker 调用你配置的模型。
运维人员（或自动采纳）再决定写成长期规则，还是归档丢掉。

见 [ALAP 与审查队列](../alap/)。

## 一起交付的东西 {#what-ships}

| 部件 | 作用 |
| --- | --- |
| `cheesewaf` | 转发进程。默认命令是 `serve` |
| `waf-cli` | 同一个二进制或软链接。默认命令是 TUI 面板 |
| `cheesewaf-gui` | Windows / macOS 上只监听回环的桌面控制器 |
| Web 控制台 | 管理平面提供的 React 界面 |
| SQLite | 默认存储，无 CGO（`modernc.org/sqlite`） |

起步不需要 Redis、Nginx 或外部数据库。

## 相关页面 {#related}

- [流量路径](../concepts/pipeline/)
- [防护等级](../concepts/paranoia/)
- [安装](../install/)
