---
title: 初始化
linkTitle: 初始化
weight: 10
description: 在 /setup 创建第一个管理员，并收紧管理监听。
---

{{% steps %}}

### 打开向导 {#open-wizard}

本机安装打开 `http://127.0.0.1:9443/setup`。
Docker 打开 `https://<主机>:9443/setup`，并接受自签名证书。

进程如果打印了初始化令牌，向导问的时候贴进去。

### 创建管理员 {#create-admin}

设置用户名，以及符合控制台密码策略的密码。
向导出示的密钥全部存好。
CheeseWAF 不会再明文打印它们。

### 确认监听 {#confirm-listener}

单机安装时，把 `server.admin_listen` 留在回环地址。
只有配了 TLS，并且前面还有网络访问控制，才把 `server.admin_public` 设成 `true`。

{{% /steps %}}

初始化完成后，同一个地址变成登录页。
命令行还可以用 `waf-cli`（TUI）或 `cheesewaf user`。
