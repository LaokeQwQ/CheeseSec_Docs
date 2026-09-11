---
title: 系统运维与安全加固
linkTitle: 运维
weight: 180
description: 本地账号管理、TOTP 双因素认证（2FA）、NTP 时钟同步、更新能力状态与软件供应链签名校验规范。
---

本章介绍 CheeseWAF 在生产环境下的日常运维操作与安全加固规范。在 Web 控制台中对应 **用户管理**、**系统管理** 与 **检查更新** 模块。

当前唯一可运行的管理存储配置是 `storage.profile: temporary`，用户、Session 和管理状态保存在内置 SQLite 中。`storage.profile: production` 只是未来管理存储路径的预留配置；管理 PostgreSQL、Coordinator 和 native-raft 集群 / epoch 后端尚未接入启动单元，因此当前二进制会拒绝这个配置。

`storage.postgresql` 只是可选的异步访问日志 Sink，不是管理数据库。可以测试已配置的 `storage.redis` 端点是否可连接，但 Bot challenge 状态仍使用进程内存后端，`protection.bot.challenge_backend: redis` 会被拒绝。`cheesewaf crp verify` 做有界离线验证，`cheesewaf crp stage` 可以把已验证的本地包写入 staged 槽位。`cheesewaf crp activate` 和 `cheesewaf crp rollback` 命令已经存在，但必须连接受保护的控制面/sidecar 适配器；缺少依赖时会 fail-closed。本地 RuntimeStore 尚未接入插件执行、服务启动、集群分发、晋级审批或 OTA 下载。

当前 CWEDP/NetLease 包已经包含 broker-bound HTTP/file transport、一次性租约校验、直接 IP 拨号、TLS/mTLS/NodeID/leaf pin、Range 续传和来源隔离，但尚未挂载到主 `serve`、节点注册或完整的插件安装/OTA 生命周期。本地 `cheesewaf temporary-online probe` 是独立的一次性运维工具，不是生产插件出站 API。

## 1. 用户管理与 CLI 凭据运维 {#users}

- **统一用户名规则**：初始化向导、Web 控制台、REST API、CLI、存储层、人类用户 JWT claims 和登录 CAPTCHA receipt 使用同一套用户名格式。用户名长度为 3–32 个 ASCII 字符，必须以 ASCII 字母开头、以 ASCII 字母或数字结尾，只能包含 ASCII 字母、数字、`.`、`_` 和 `-`。非 ASCII 字符、Unicode 空白字符、控制字符（`Cc`）和格式/不可见字符（`Cf`）都会被拒绝。服务端保留原始输入，不会自动去除空格或转小写，因此 `admin` 和 ` admin ` 是两个不同的字符串，后者无效。
- **角色输入规则**：用户 `role` 必须精确匹配当前 `apisec.permissions` 中已配置的角色键（通常为 `admin` 或 `readonly`）。空角色、未知角色、`*`/`:` 权限表达式，以及包含首尾或嵌入 Unicode 空白、控制字符（`Cc`）或格式/不可见字符（`Cf`）的角色都会被拒绝。服务端不会自动去空格或改大小写；账号字段不合法时分别返回 `USERNAME_INVALID` 或 `ROLE_INVALID`。
- **Web 控制台与 REST API**：调用 `GET/POST /api/users` 与 `PUT /api/users/{id}` 管理账号。Web 用户管理、初始化向导和登录使用同一套校验规则。
- **命令行运维工具（`cheesewaf user`）**：
  ```bash
  # 推荐脚本方式：从标准输入读取密码，避免写入 shell 历史或进程列表
  cheesewaf user password admin --password-stdin < secret.txt

  # 仅适合一次性人工操作：显式密码（必须三选一）
  read -r -s -p 'New password: ' CHEESEWAF_NEW_PASSWORD; printf '\n'
  cheesewaf user password admin --password "$CHEESEWAF_NEW_PASSWORD"

  # 自动生成随机高强度密码并重置/禁用 TOTP 2FA（应急恢复）
  cheesewaf user password admin --generate --reset-2fa

  # 确保初始管理员存在并从标准输入注入密码（适合自动化部署脚本）
  cheesewaf user ensure-admin admin --password-stdin < secret.txt

  # 重命名本地管理员账号
  cheesewaf user rename old_admin new_admin

  # 按不可变用户 ID 修复历史非法用户名
  cheesewaf user repair-username USER_ID recovered_admin --reason 'Historical whitespace in imported account'
  ```
- 当前用户名已经符合规则时，应使用 `user rename`，旧用户名和新用户名都必须通过同一套校验。命令会更新账号并撤销该账号全部未撤销的 Session，但不会写入历史用户名修复审计记录；它不能按用户名选中历史非法账号。只有 `repair-username` 会把用户名更新、撤销 Session 和写入审计记录放在同一个事务中。
- 只有历史用户名不符合当前规则时，才能使用 `user repair-username`，例如 ` admin `。该命令必须提供 `--reason` 和准确的不可变用户 ID。用户不存在、当前用户名已经合法，或目标用户名已被其他账号占用时，命令都会拒绝执行，也不会合并账号。用户名更新、撤销该用户全部未撤销的管理端 Session 和追加审计记录在同一个 SQLite 事务中提交。用户 ID、密码哈希、角色、TOTP 启用状态和 TOTP 密钥都会保留。审计记录包含当前操作系统用户 ID、填写的原因、旧用户名、新用户名、撤销的 Session 数量和时间。两个路径都不会自动去除空格或转小写。
- 请使用拥有 CheeseWAF 数据目录权限的操作系统账号运行修复命令。审计中的操作者来自当前操作系统用户 ID；换用其他账号运行会改变这条证据。
- **密码策略**：新密码至少需要 10 个字符，并满足大写字母、小写字母、不重复数字、特殊字符 4 类中的至少 3 类。常见密码和简单模式（包括连续数字、键盘序列）会被拒绝。密码不能等于用户名，也不能包含用户名。优先使用 `--password-stdin`；直接使用 `--password` 可能把密码写入 shell 历史或进程列表。
- **最小权限原则**：建议为日常审计监控人员创建 `readonly` 只读角色，避免共享超级管理员账号。
- **TOTP 双因素认证（2FA）**：支持标准 TOTP 认证。调用 `/api/users/{id}/2fa/setup` 生成密钥与绑定二维码，并调用 `enable`、`disable` 或 `recover` 进行生命周期管理。
- 管理 API Token 的显示备注属于元数据，不是账号用户名，不套用账号用户名规则。不要把 Token 备注当作人类用户身份。管理 API Token 默认有效期为 90 天，最长 365 天；运行中的服务通过合并清理 worker 删除过期或连续 180 天无活动的 Token，并尝试写入审计和管理员通知。
- Web 系统页面包含不过期 Token 的二次确认弹窗，但在确认适配器配置完成前该选项保持禁用。当前运行时尚未接入 `ApprovalGate`、当前密码/TOTP 校验和 10 秒警告阅读等待，因此创建不过期 Token 会返回 `API_TOKEN_CONFIRMATION_UNAVAILABLE`。

如需查找用户 ID，请使用 SQLite CLI 的只读模式，并且只选择 ID 和带引号的用户名，不读取密码哈希或 TOTP 密钥：

```bash
DB=/var/lib/cheesewaf/cheesewaf.db
sqlite3 -readonly "$DB" \
  'SELECT id, quote(username) AS username FROM users ORDER BY username;'
```

`quote(username)` 会让用户名前后的空格在结果中可见。不要使用 `SELECT *`，也不要把这段输出粘贴到工单或日志中。

## 2. 备份和迁移 SQLite 管理存储 {#sqlite-maintenance}

执行用户名修复或升级二进制前，先根据 `storage.sqlite.path` 确认当前数据库和父目录。常见默认路径是本地运行时的 `./data/cheesewaf.db`，以及 Linux 服务的 `/var/lib/cheesewaf/cheesewaf.db`。不要把这些命令指向版本库中的 `configs/cheesewaf.yaml` 模板。

运行中的 SQLite 通常使用 WAL 模式。CheeseWAF 运行时不要只复制主 `.db` 文件；最新提交可能仍在 `-wal` 文件中，这样得到的副本可能无法恢复。在线备份可以在服务继续运行时读取一致性快照：

```bash
DB=/var/lib/cheesewaf/cheesewaf.db
BACKUP_DIR=/var/backups/cheesewaf
test -f "$DB" || { echo "database not found: $DB" >&2; exit 1; }
install -d -m 700 "$BACKUP_DIR"
df -h "$BACKUP_DIR"
du -h "$DB"
BACKUP="$BACKUP_DIR/cheesewaf-before-maintenance-$(date -u +%Y%m%dT%H%M%SZ).db"
test ! -e "$BACKUP" || { echo "backup path already exists: $BACKUP" >&2; exit 1; }
sqlite3 -readonly "$DB" ".backup '$BACKUP'"
chmod 600 "$BACKUP"
test -s "$BACKUP" || { echo "backup is empty: $BACKUP" >&2; exit 1; }
integrity=$(sqlite3 -readonly "$BACKUP" 'PRAGMA integrity_check;')
test "$integrity" = ok || { echo "backup integrity check failed: $integrity" >&2; exit 1; }
sha256sum "$BACKUP" > "$BACKUP.sha256"
sha256sum -c "$BACKUP.sha256"
```

完整性检查必须返回 `ok`，最后的校验和命令必须报告 `OK`；任一检查失败都应立即停止。请把备份放在受保护的位置，并按保留策略复制到异机。备份包含敏感的管理数据，不能上传到工单或粘贴到聊天中。开始前检查磁盘空间；备份期间关注 WAF 健康状态和磁盘延迟。CheeseWAF 的单一二进制同时提供数据平面和管理平面，停止它可能中断防护和业务流量。

如果无法在线备份，只能通过服务管理器停止确切的 CheeseWAF 写入进程，并确认没有其他 CheeseWAF 进程继续写入，再复制包含相邻 `-wal` 和 `-shm` 文件的一致数据库集合。重启服务前，用 `PRAGMA integrity_check;` 验证副本。不要使用会停止大量无关进程的命令。

当前二进制会按顺序执行 SQLite 迁移，当前 Schema 版本为 5。3 到 4 的迁移会创建只追加的 `user_username_repairs` 审计表，4 到 5 的迁移会为 `users` 和 `admin_sessions` 增加 `credential_epoch`。账号安全信息变化时会递增用户 epoch，活动 Session 必须匹配当前 epoch。这些迁移不会自动去除空格、转小写、合并或改写现有账号。只支持旧 Schema 的二进制打开新数据库时，会因 `newer SQLite schema version` 拒绝运行。

如果需要降级，请恢复升级前的备份，并在核对服务路径和数据路径后再启动旧二进制。不要手工修改 `PRAGMA user_version`。如果用户名修复成功后必须撤销，请在计划维护窗口恢复修复前备份；`repair-username` 会刻意拒绝把合法用户名改回非法格式。

## 3. 日志支持包与 CLI 语言管理 {#cli-maintenance}

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

## 4. NTP 时钟同步与状态校准 {#time}

JWT 签名校验、TOTP 动态验证码计算以及集群节点共识均强依赖系统时钟的准确性：

- **查询时钟源**：调用 `GET /api/system/time-sync` 查询当前 NTP 时钟源与偏差。
- **强制同步**：调用 `POST /api/system/time-sync/sync` 触发即时时钟对齐。
- **重新优选**：调用 `POST /api/system/time-sync/reselect` 重新探测并选择延迟最低的 NTP 节点。

## 5. OTA 能力状态 {#updates}

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

- **当前运行边界**：这些配置键为 OTA 更新器预留，但当前二进制没有更新 Worker。控制台的「检查更新」页面会报告 `NOT_IMPLEMENTED`；通过系统 API 开启 OTA 会被 `OTA_UPDATES_UNAVAILABLE` 拒绝。
- **配置安全**：在更新 Worker 交付前，请保持 `enabled: false`。启用时，配置校验仍会检查服务器地址、通道、间隔和签名设置。
- **未来行为**：`auto_update_rules`、`auto_update_binary` 和 `verify_signature` 描述计划中的签名更新策略，不表示当前会下载或安装规则、二进制。

## 6. 软件供应链安全与发布完整性校验 {#supply-chain}

只使用实际发布版本提供的元数据。运行时不会自动生成或验证发行签名：

- **SBOM**：如果发行版本提供 CycloneDX 或 SPDX SBOM，请将它与部署记录一起保存，并核对其中的版本和摘要是否与收到的文件一致。
- **容器签名**：如果发行版本提供 Cosign 签名，请在部署前针对确切的镜像引用进行验证。
- **Windows 签名**：如果 Windows 安装包带有 Authenticode 元数据，请在实际安装机器上核对签名者和证书链。
- **校验和**：如果发行版本提供校验和文件，请使用 `sha256sum -c checksums.txt` 或对应平台的工具校验确切文件。
