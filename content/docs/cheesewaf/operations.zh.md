---
title: 系统运维与安全加固
linkTitle: 运维
weight: 180
description: 账号管理、TOTP 双因素认证（2FA）、NTP 时钟同步、OTA 规则更新与系统参数维护。
---

本章介绍 CheeseWAF 在生产环境下的日常运维操作与安全加固规范。在 Web 控制台中进入 **用户管理**、**系统管理** 与 **检查更新** 模块。

## 1. 用户管理与 TOTP 双因素认证（2FA） {#users}

- **账号增删改查**：调用 `GET/POST /api/users` 与 `PUT /api/users/{id}` 进行用户管理，或在终端中使用 `cheesewaf user` 命令。
- **最小权限原则**：建议为日常审计人员单独创建 `readonly` 只读角色，避免共享超级管理员账号。
- **TOTP 双因素认证**：支持基于时间的一次性密码（TOTP）。通过 `/api/users/{id}/2fa/setup` 生成密钥与二维码，并调用 `enable`、`disable` 或 `recover` 进行生命周期管理。

## 2. NTP 时钟同步与状态校准 {#time}

JWT 签名校验、TOTP 动态验证码计算以及集群节点共识均强依赖系统时钟的准确性：

- **查询时钟源**：调用 `GET /api/system/time-sync` 查询当前 NTP 时钟源与偏差。
- **强制同步**：调用 `POST /api/system/time-sync/sync` 触发即时时钟对齐。
- **重新优选**：调用 `POST /api/system/time-sync/reselect` 重新探测并选择延迟最低的 NTP 节点。

## 3. OTA 自动化更新机制 {#updates}

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

- **规则自动更新**：开启 `auto_update_rules: true` 后，系统会定期从官方更新服务器拉取最新的语义威胁特征库与威胁情报。
- **二进制更新安全**：在生产环境中，建议将 `auto_update_binary` 设为 `false`，通过受控的发布流程进行软件升级。
- **数字签名校验**：`verify_signature` 必须始终保持 `true`，以确保更新包未被篡改。

## 4. 系统信息与版本查询 {#system}

- 调用 `GET /api/system` 与 `PUT /api/system` 读写全局运行时系统参数。
- 调用 `GET /api/version` 获取当前运行版本的 Git Commit Hash、构建环境与发布通道。

关于数据持久化、配置导出与磁盘回收，请参考 [存储与调度管理](../storage/)。
