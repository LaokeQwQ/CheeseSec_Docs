---
title: Docker Compose 部署
linkTitle: Docker
weight: 20
description: 使用 Docker Compose 编排部署 CheeseWAF，支持容器只读根文件系统与非 root 安全运行。
---

本方案适用于容器化云原生基础设施。仓库提供经过加固的 Dockerfile 与 Compose 示例，示例会在本地构建镜像；除非另行核对镜像来源，否则不要把 `cheesewaf:dev` 当作厂商签名或已发布到可信仓库的镜像。运行时默认使用专用非 root 用户（UID `10001`）并启用只读根文件系统。

容器资源由宿主机和容器限制共同决定。逻辑核数不超过 2 或内存不超过 2 GB 时，初始化向导会推荐 `low`；探测失败或超时也会回退到 `low`。Compose 示例只把管理端口绑定到宿主机回环地址 `127.0.0.1:9443`。`storage.profile: production` 当前仍会因生产接线不完整而拒绝启动，不会回退到 SQLite。

## 编排配置（Compose 文件） {#compose-file}

参考项目仓库中的 `deploy/docker/docker-compose.yml`：

```yaml
services:
  cheesewaf:
    image: cheesewaf:dev
    build:
      context: ../..
      dockerfile: deploy/docker/Dockerfile
    user: "10001:10001"
    restart: unless-stopped
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=32m,mode=1777,noexec,nosuid,nodev
    ports:
      - "8080:8080"
      - "127.0.0.1:9443:9443"
    volumes:
      - cheesewaf-data:/var/lib/cheesewaf
      - cheesewaf-logs:/var/log/cheesewaf
    healthcheck:
      test: ["CMD", "/usr/local/bin/cheesewaf-entrypoint", "healthcheck"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  cheesewaf-data:
  cheesewaf-logs:
```

{{% pageinfo color="info" %}}
本地自行构建镜像时，构建上下文（context）须指向 CheeseWAF 项目的根目录，以确保 Web 前端源码（`web/`）与后端 Go 模块均能正常参与多阶段构建。
示例中的 `8080:8080` 会把数据平面监听器发布到 Docker 宿主机所有网卡。请配置明确的防火墙/反向代理策略，或将其绑定到受控网卡；只有管理端口默认绑定宿主机回环地址。
{{% /pageinfo %}}

## 启动与初始化 {#start}

执行以下命令在后台启动容器并观察日志：

```bash
docker compose -f deploy/docker/docker-compose.yml up -d
docker compose -f deploy/docker/docker-compose.yml logs -f cheesewaf
```

容器首次启动时会自动在持久化目录生成初始管理员配置，并为管理平面签发自签名证书。本 Compose 文件将管理端口仅绑定到 Docker 宿主机回环地址（`127.0.0.1:9443`），请在宿主机浏览器中打开 `https://127.0.0.1:9443/setup`。从其他机器访问时，请先将 `CHEESEWAF_SSH_TARGET` 设置为 SSH 目标，再执行 `ssh -N -L 9443:127.0.0.1:9443 "$CHEESEWAF_SSH_TARGET"` 建立隧道，之后仍使用同一回环地址；如需直接暴露端口，请显式修改绑定并配置相应的访问控制。亦可执行以下命令通过容器终端进行 CLI 初始化：

首次初始化尚未完成时，容器日志不会打印初始化 Token 或完整地址，只显示基础 `/setup` 地址、受保护的 `/var/lib/cheesewaf/setup.url` 路径和不含秘密的随机回执。请在 10 分钟有效期内从权限为 `0600` 的文件读取完整地址。初始化完成后，Token 会被撤销；过期的 `setup.url` 文件会被清理。

```bash
docker compose -f deploy/docker/docker-compose.yml exec -it cheesewaf \
  cheesewaf --config /var/lib/cheesewaf/config/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf setup
```

停止容器（`docker compose -f deploy/docker/docker-compose.yml down`）时，SQLite 数据、证书、自定义规则和日志会保存在命名卷 `cheesewaf-data` 与 `cheesewaf-logs` 中。配置 `storage.postgresql` 时，它接收外部访问日志；默认 `storage.profile: temporary` 下，Docker 卷仍保存管理数据库。预留的 `production` 配置当前会在启动时拒绝。
