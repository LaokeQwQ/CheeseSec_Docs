---
title: 独立控制面运行时
linkTitle: 控制面运行时
weight: 140
description: 独立 cheesewaf-control 进程的公开命令参数、本地状态接口和当前限制。
---

`cheesewaf-control` 是提供本地状态服务的独立命令。它不检测 WAF 流量，不托管 Web 控制台，也不替代 `cheesewaf serve`。

{{% pageinfo color="warning" %}}
这个命令不提供完整的高可用部署、空集群初始化、远程节点注册、插件安装或 OTA 更新。主 WAF 服务仍使用自己的配置和受支持的存储模式。
{{% /pageinfo %}}

## 命令参数 {#command}

进程只接受命令行选项，不接受位置参数。请先运行 `cheesewaf-control --help`，核对已安装版本支持的参数。

```text
cheesewaf-control \
  --profile production \
  --cluster-id cluster-a \
  --node-id node-a \
  --data-dir /var/lib/cheesewaf/control \
  --listen 127.0.0.1:9450 \
  --raft-listen 127.0.0.1:9451 \
  --mode join \
  --ca-file /etc/cheesewaf/control/ca.pem \
  --cert-file /etc/cheesewaf/control/node.pem \
  --key-file /etc/cheesewaf/control/node-key.pem \
  --postgres-dsn '<由受保护的密钥来源提供>' \
  --timeout 15s
```

| 参数 | 默认值 | 规则 |
| --- | --- | --- |
| `--profile` | `production` | 只接受 `production`。 |
| `--cluster-id` | 空 | 必填；不接受空白、控制字符或不可见格式字符。 |
| `--node-id` | 自动生成 | 可选的节点身份；自动生成时保存在 `--data-dir` 下。 |
| `--data-dir` | 空 | 必填的持久目录，必须限制访问权限。 |
| `--listen` | `127.0.0.1:9450` | 本地 HTTP 地址，必须是回环 `host:port`。 |
| `--raft-listen` | `127.0.0.1:9451` | 共识监听地址，必须是不同的回环 `host:port`。 |
| `--mode` | `join` | 只能是 `bootstrap` 或 `join`；默认值不会初始化集群。 |
| `--ca-file` | 空 | 必填的 PEM CA 文件，必须是受保护的普通文件。 |
| `--cert-file` | 空 | 必填的节点证书 PEM；显式设置节点身份时，证书身份必须匹配。 |
| `--key-file` | 空 | 必填的私钥 PEM；应只允许所有者读取（`0600`），不得写入日志或源码仓库。 |
| `--postgres-dsn` | 空 | 必填的管理数据库连接，不会出现在状态 JSON 中。 |
| `--timeout` | `15s` | 必须为正数，超时会停止启动。 |

两个监听地址都只允许使用回环地址。连接远程数据库时必须启用并校验证书的 TLS。管理数据库连接与主 WAF 服务可选的访问日志存储 `storage.postgresql.dsn` 不同。

以上路径和身份只是示例。运行前应准备有效凭据及所需服务状态；仅执行这条示例命令不能创建可用的 HA 部署。

## 启动状态 {#startup}

命令会先校验配置与所需依赖，再报告就绪状态。启动失败时输出 `control-plane startup failed closed` 并退出。应先解决提示的配置或依赖问题，再重新启动。进程正在运行或存活探针返回成功，不代表它已经可以接受写入。

## 本地状态接口 {#endpoints}

状态服务供本机 supervisor 和探针通过 `--listen` 使用。

| 方法 | 路径 | 响应 |
| --- | --- | --- |
| `GET` | `/healthz` | 返回 `200` 和当前状态文档；存活不代表就绪。 |
| `GET` | `/readyz` | 只有可以接受写入时返回 `200`，否则返回 `503`。 |
| `GET` | `/status` | 返回 `200`，提供有长度限制的状态和就绪信息。 |
| `POST` | `/proposals` | 未就绪时返回 `503`；当前命令在就绪后仍返回 `501`，表示该操作不可用。其他方法返回 `405`。 |

状态响应不包含凭据、数据库连接字符串或私有文件路径。这些接口不是远程集群管理 API。

## 启动模式 {#modes}

`bootstrap` 和 `join` 用于选择启动模式，都不提供完整的集群管理流程。当前命令不能初始化空的生产集群或注册远程节点，也没有控制器地址或加入令牌参数。不能据此认定生产多节点 HA 已经可用。

## 主 WAF 服务 {#serve}

WAF 流量和 Web 控制台仍由 `cheesewaf serve` 提供。启动 `cheesewaf-control` 不会迁移主服务的存储，也不会改变主服务支持的功能。主服务的公开配置和当前限制见[集群](../cluster/)。
