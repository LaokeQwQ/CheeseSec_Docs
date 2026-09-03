---
title: 系统运维与安全加固
linkTitle: 运维
weight: 180
description: 本地账号管理、TOTP 双因素认证（2FA）、NTP 时钟同步、OTA 规则更新与软件供应链签名校验规范。
---

本章介绍 CheeseWAF 在生产环境下的日常运维操作与安全加固规范。在 Web 控制台中对应 **用户管理**、**系统管理** 与 **检查更新** 模块。

## 1. 用户管理与 CLI 凭据运维 {#users}

- **Web 控制台与 REST API**：调用 `GET/POST /api/users` 与 `PUT /api/users/{id}` 进行管理员账号增删改查。
- **命令行运维工具（`cheesewaf user`）**：
  ```bash
  # 为指定用户重置密码（交互式输入）
  cheesewaf user password admin

  # 自动生成随机高强度密码并重置/禁用 TOTP 2FA（应急救砖）
  cheesewaf user password admin --generate --reset-2fa

  # 确保初始管理员存在并从标准输入注入密码（适合自动化部署脚本）
  cheesewaf user ensure-admin admin --password-stdin < secret.txt

  # 重命名本地管理员账号
  cheesewaf user rename old_admin new_admin
  ```
- **最小权限原则**：建议为日常审计监控人员创建 `readonly` 只读角色，避免共享超级管理员账号。
- **TOTP 双因素认证（2FA）**：支持标准 TOTP 认证。调用 `/api/users/{id}/2fa/setup` 生成密钥与绑定二维码，并调用 `enable`、`disable` 或 `recover` 进行生命周期管理。

## 2. 日志支持包与 CLI 语言管理 {#cli-maintenance}

- **一键打包服务日志（Support Bundle）**：在遇到难以定位的异常时，执行以下命令即可一键将全部运行时日志导出为规范命名的 ZIP 支持包，便于快速交接或提交安全工单：
  ```bash
  cheesewaf logs pack --dir /tmp --name cheesewaf-support.zip
  ```
- **CLI 界面语言配置**：
  ```bash
  # 查询当前语言与支持列表
  cheesewaf lang show

  # 持久化设置默认 CLI 语言（支持 en 与 zh-CN）
  cheesewaf lang set zh-CN
  ```

## 3. NTP 时钟同步与状态校准 {#time}

JWT 签名校验、TOTP 动态验证码计算以及集群节点共识均强依赖系统时钟的准确性：

- **查询时钟源**：调用 `GET /api/system/time-sync` 查询当前 NTP 时钟源与偏差。
- **强制同步**：调用 `POST /api/system/time-sync/sync` 触发即时时钟对齐。
- **重新优选**：调用 `POST /api/system/time-sync/reselect` 重新探测并选择延迟最低的 NTP 节点。

## 4. OTA 自动化更新机制 {#updates}

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

## 5. 软件供应链安全与发布完整性校验 {#supply-chain}

CheeseWAF 遵循严格的软件供应链安全规范，所有官方发布的二进制程序与容器镜像均经过多重加密与签名验证：

- **软件物料清单（SBOM）**：每个发布版本均随附由 Syft 自动生成的标准 CycloneDX / SPDX 格式 SBOM，清晰列出所有依赖项版本与许可证信息。
- **容器镜像 Cosign 签名**：Docker Hub 与 GitHub Packages 上的官方镜像均使用 Sigstore / Cosign 进行无钥密码学签名，部署前可通过 `cosign verify` 验证镜像真实性。
- **Windows Authenticode 数字签名**：Windows NSIS 安装程序与单文件可执行文件均带有官方代码签名证书，确保在 Windows 环境下不触发 SmartScreen 恶意软件拦截。
- **SHA256 校验和**：所有二进制资产均提供 `checksums.txt` 校验和文件，下载后建议执行 `sha256sum -c checksums.txt` 验证文件完整性。
