---
title: 命令行与 TUI 交互
linkTitle: 命令行
weight: 150
description: cheesewaf 与 waf-cli 统一二进制分发命令、全局参数、子命令集及 TUI 终端界面使用说明。
---

CheeseWAF 采用单一二进制（BusyBox 模式）设计，通过调用文件名自动识别运行模式：

| 可执行文件名 | 默认行为与说明 |
| --- | --- |
| `cheesewaf` | 默认执行 `serve` 命令，启动 WAF 数据平面反代与控制平面管理服务 |
| `waf-cli` | 默认启动交互式终端图形面板（TUI，即 canonical 的 `cli` 命令；`panel` 为兼容别名） |

## 全局命令行参数 {#global-flags}

```text
-c, --config string     指定配置文件路径（默认 ./data/config/cheesewaf.yaml）
    --data-dir string   指定运行数据目录（默认 ./data）
    --lang string       界面语言偏好（en 或 zh-CN）
```

界面多语言匹配优先级为：命令行 `--lang` 参数 > 环境变量 `CHEESEWAF_LANG` > 数据目录已保存配置 > 操作系统系统区域设置。

## 子命令参考列表 {#commands}

| 子命令 | 功能说明 |
| --- | --- |
| `serve` | 启动 WAF 服务（数据平面转发 + 控制平面 API 与 Web 控制台） |
| `setup` | 引导式或无交互命令行初始化向导，配置系统画像与初始管理员凭证 |
| `rules` | 站点自定义正则规则批量导入、导出与模板生成 |
| `cli` | 启动交互式 TUI 终端控制台（兼容别名：`panel`） |
| `status` | 查询本地服务进程运行状态与 PID 租约 |
| `healthcheck` | 执行健康检查探测（不健康时返回非 0 退出码，常用于 Docker 容器探针与出站 TLS 诊断） |
| `stop` | 安全终止正在运行的本地服务进程 |
| `restart` | 重启本地服务进程 |
| `user` | 本地管理员账号密码重置、重命名及 2FA 凭据维护 |
| `cluster` | 集群主控初始化、工作节点加入、证书轮换、令牌管理与协同指令 |
| `logs` | 将服务日志打包导出为 ZIP 支持包（`logs pack`） |
| `lang` | 查询或持久化设置 CLI 默认语言（`lang show` / `lang set`） |
| `version` | 打印当前软件版本、构建 Git Commit、发布通道与编译时间 |

## 核心子命令与参数详解 {#subcommands-detail}

### 1. 系统初始化向导（`setup`） {#cmd-setup}

支持交互式向导与适合脚本自动化的无人值守模式：

```bash
# 交互式向导（包含硬件探测、硬件画像评定与密码设置）
cheesewaf setup

# 无人值守自动化初始化
cheesewaf setup --yes \
  --username admin \
  --password-stdin < /path/to/password.txt \
  --profile smart \
  --admin-listen 127.0.0.1:9443 \
  --skip-probe
```

常用参数包括：
- `-y, --yes`：跳过所有交互式确认提示直接提交。
- `--username` / `--password-stdin`：初始超级管理员账号与从标准输入读取的强密码。
- `--profile`：硬件适配画像（可选 `smart`、`low`、`medium`、`high`、`custom`，兼容别名 `minimal`、`balanced`、`performance`）。
- `--admin-listen`：指定管理平面监听地址（默认 `127.0.0.1:9443`）。
- `--skip-probe` / `--skip-external`：跳过 CPU/内存/磁盘自动探测或跳过外部遥测（GeoIP/Prometheus/VictoriaLogs）配置。

### 2. 自定义规则导入与导出（`rules`） {#cmd-rules}

支持以 YAML 或 JSON 格式全量替换或导出指定站点的 `custom_rules`，规则导入成功后会自动向本地运行中服务发送信号以触发平滑热重载：

```bash
# 生成标准自定义规则 YAML 模板
cheesewaf rules example --format yaml --file rules-template.yaml

# 验证并全量导入自定义规则至指定站点
cheesewaf rules import --site site-demo --file my-rules.yaml

# 导出指定站点的自定义规则为 JSON
cheesewaf rules export --site site-demo --format json --file exported-rules.json
```

### 3. 本地用户管理（`user`） {#cmd-user}

```bash
# 为指定用户重置密码（推荐从标准输入读取，避免密码出现在 shell 历史、环境变量或进程参数中）
cheesewaf user password admin --password-stdin < secret.txt
# 直接使用 --password 安全性较低，密码可能出现在 shell 历史、环境变量或进程参数中
cheesewaf user password admin --password 'replace-with-new-password'

# 自动生成高强度临时密码并禁用 TOTP 2FA（常用于应急恢复）
cheesewaf user password admin --generate --reset-2fa

# 确保管理员账号存在（不存在则自动创建，存在则更新密码）
cheesewaf user ensure-admin admin --password-stdin < secret.txt

# 重命名本地用户名
cheesewaf user rename old_admin new_admin
```

### 4. 集群节点管理（`cluster`） {#cmd-cluster}

```bash
# 将当前节点初始化为集群主控节点（该命令仅写入配置，不生成 CA）
cheesewaf cluster init

# 签发新的工作节点加入令牌（有效期默认 15 分钟）
cheesewaf cluster token create --ttl 15m

# 查看或吊销加入令牌
cheesewaf cluster token list
export CHEESEWAF_TOKEN_ID='token-id-to-revoke'
cheesewaf cluster token revoke "$CHEESEWAF_TOKEN_ID"

export CHEESEWAF_CONTROLLER='https://10.0.0.1:9443'
export CHEESEWAF_JOIN_TOKEN='one-time-join-token'
export CHEESEWAF_NODE_ID='node-worker-02'
export CHEESEWAF_ADVERTISE_ADDR='10.0.0.2:9444'
export CHEESEWAF_CONTROLLER_CA='/etc/cheesewaf/certs/admin-ca.crt'

# 工作节点使用一次性令牌加入，CLI 会在本地生成密钥与 CSR
cheesewaf cluster join \
  --controller "$CHEESEWAF_CONTROLLER" \
  --token "$CHEESEWAF_JOIN_TOKEN" \
  --node-id "$CHEESEWAF_NODE_ID" \
  --advertise-addr "$CHEESEWAF_ADVERTISE_ADDR" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA"

export CHEESEWAF_API_TOKEN='management-token-with-write-cluster'

# 请求替换集群 mTLS 文件（需已有本地证书路径；写入后按需 reload/restart）
cheesewaf cluster cert rotate \
  --controller "$CHEESEWAF_CONTROLLER" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA" \
  --api-token-env CHEESEWAF_API_TOKEN

# 查询集群拓扑与仲裁健康状态
cheesewaf cluster status

# 导出集群声明式对象（命令输出 YAML，可重定向保存）
cheesewaf cluster export > cluster-export.yaml

# 启动当前节点的心跳监控循环（目标为 HTTPS/mTLS 集群互联端口）
export CHEESEWAF_INTERCONNECT_CONTROLLER='https://10.0.0.1:9444'
cheesewaf cluster monitor-node --controller "$CHEESEWAF_INTERCONNECT_CONTROLLER" --interval 10s
```

`cluster join` 与 `cert rotate` 的 `--ca-file` 用于校验控制器 **9443 HTTPS 管理端**，不是加入响应返回的集群 CA。若控制器证书链已受系统信任可省略；私有 CA 场景请预置管理端 CA。加入时 CLI 会在本地生成密钥/CSR，接收集群 CA 与节点证书并写入数据目录。证书轮换要求节点已有配置的证书路径，且令牌来源必须三选一（`--api-token`、`--api-token-file` 或 `--api-token-env`）；写入文件后需按服务流程 reload/restart 才会生效。

`cluster monitor-node` 通常向 HTTPS `:9444` 集群互联端点发送心跳，并使用本地配置的集群 CA/证书/私钥。自定义 `--controller` 也必须是 HTTPS 互联地址；`--insecure-skip-verify` 仅限隔离实验室使用。

{{% pageinfo color="info" %}}
- `cheesewaf user` 拥有命令别名 `cheesewaf users`，用法完全一致。
- `cheesewaf healthcheck` 为服务探针隐藏命令（常用于容器健康检查探针），不展示在 `--help` 列表中。
- 交互式终端 TUI 面板主命令为 `cheesewaf cli`，同时支持别名 `cheesewaf panel`。
{{% /pageinfo %}}

### 5. 日志支持包打包（`logs`） {#cmd-logs}

```bash
# 将当前数据目录下的全部服务日志打包为带时间戳的 ZIP 归档
cheesewaf logs pack

# 指定输出目录与归档文件名
cheesewaf logs pack --dir /tmp --name support-bundle.zip
```

### 6. 多语言设置（`lang`） {#cmd-lang}

```bash
# 查询当前生效语言与支持的语言列表
cheesewaf lang show

# 持久化设置 CLI 语言为简体中文或英文
cheesewaf lang set zh-CN
cheesewaf lang set en
```

## 常用操作示例 {#examples}

```bash
# 指定自定义配置文件与数据目录启动
cheesewaf serve --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf

# 检查运行状态与 PID 租约
cheesewaf status

# 启动交互式 TUI 终端面板
waf-cli

# 容器探针与网络就绪性诊断
cheesewaf healthcheck
```

{{% pageinfo color="info" %}}
在 Windows 环境下若需直接使用 `waf-cli` 命令名称，可将 `cheesewaf.exe` 复制或创建别名为 `waf-cli.exe`。
{{% /pageinfo %}}
