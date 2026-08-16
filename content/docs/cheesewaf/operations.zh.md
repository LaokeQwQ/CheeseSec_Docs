---
title: 运维
linkTitle: 运维
weight: 180
description: 用户、双因素、时间同步、OTA 更新和系统维护。
---

控制台：**用户**、**系统**、**更新**。

## 用户 {#users}

`GET/POST /api/users`，`PUT /api/users/{id}`。
每个用户可以打开 TOTP：`/api/users/{id}/2fa/setup`、`enable`、`disable`、`recover`。

命令行：`cheesewaf user`。

不要共享第一个管理员密码。
只看日志的人，单独建一个 `readonly` 角色账号。

## 时间同步 {#time}

`GET /api/system/time-sync` 显示当前时钟源。
`POST /api/system/time-sync/reselect` 重新选择。
`POST /api/system/time-sync/sync` 立刻同步。

主机时间不对时，JWT 和 TOTP 都会坏。
先把时间修好，再去查「令牌无效」。

## 更新 {#updates}

```yaml
update:
  ota:
    enabled: false
    server: ""
    channel: "stable"
    check_interval: 6h
    auto_update_rules: true
    auto_update_binary: false
    verify_signature: true
```

在你信任 OTA 服务器和公钥之前，保持 `auto_update_binary` 为 false。
`verify_signature` 必须保持 true。

## 系统 {#system}

`GET /api/system` 和 `PUT /api/system` 读写系统设置。
`GET /api/version` 打印正在运行的版本。

备份和清理见 [存储与调度](../storage/)。
