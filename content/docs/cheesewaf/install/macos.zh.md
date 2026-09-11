---
title: macOS 部署
linkTitle: macOS
weight: 40
description: 使用 DMG 镜像安装 CheeseWAF 桌面应用，或使用 tar.gz 压缩包以命令行方式运行。
---

在 macOS 系统下，CheeseWAF 支持桌面图形包与命令行压缩包两种运行方式：

初始化向导会根据本机资源推荐档位。逻辑核数不超过 2 或内存不超过 2 GB 时使用 `low`；探测失败或超时也会回退到 `low`。管理面默认只监听 `127.0.0.1:9443`。

## 1. DMG 桌面安装包 {#dmg}

适用于本地开发调试与桌面工作站环境：

1. 根据芯片架构下载安装包：Apple Silicon（M 系列芯片）选择 `cheesewaf-arm64-darwin-*.dmg`，Intel 芯片选择 `cheesewaf-amd64-darwin-*.dmg`。
2. 双击打开 DMG 镜像，将 **CheeseWAF** 拖拽至 **Applications（应用程序）** 文件夹。
3. 从启动台或应用程序文件夹中启动 CheeseWAF。

{{% pageinfo color="info" %}}
**Gatekeeper 安全验证说明**：只有在构建环境具备 Developer ID 身份和 Apple 公证凭据时，发行包才会完成签名与公证。打包脚本在缺少这些凭据时会明确回退为 ad-hoc 签名且不做公证。部署前请根据发布时提供的签名元数据核对确切文件。若使用 ad-hoc 开发包触发系统拦截，请对应用图标点按右键选择「打开」并在提示框中确认。
{{% /pageinfo %}}

程序启动后将拉起基于浏览器的本地控制器服务（监听回环地址 `http://127.0.0.1:17943/`），支持一键启动/停止主服务、查看运行状态及快速直达 Web 管理控制台。默认运行时数据目录为 `~/Library/Application Support/CheeseWAF`。

## 2. 命令行压缩包（tar.gz） {#tarball}

适用于纯终端操作或无图形界面环境：

```bash
# 解压对应架构的压缩包
tar -xzf cheesewaf-arm64-darwin-*.tar.gz
cd cheesewaf-*

# 运行终端初始化向导
./cheesewaf setup

# 启动 WAF 守护服务
./cheesewaf serve --config ./data/config/cheesewaf.yaml --data-dir ./data
```

如果首次 Web 初始化尚未完成，进程输出只显示基础 `/setup` 地址、受保护的 `data/setup.url` 路径和不含秘密的随机回执。请在 10 分钟有效期内从权限为 `0600` 的文件读取完整地址。初始化完成后，Token 会被撤销；过期的 `setup.url` 文件会被清理。

服务启动后，使用浏览器访问 `http://127.0.0.1:9443/` 进入 Web 管理控制台登录页。
