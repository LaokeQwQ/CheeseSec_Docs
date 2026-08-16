---
title: Docker Compose 部署
linkTitle: Docker
weight: 20
description: 使用 Docker Compose 编排部署 CheeseWAF，支持容器只读根文件系统与非 root 安全运行。
---

本方案适用于容器化基础设施。CheeseWAF 官方镜像遵循安全加固规范，默认以非 root 用户（UID `10001`）运行，并启用只读根文件系统。

## 编排配置（Compose 文件） {#compose-file}

参考项目仓库中的 `deploy/docker/docker-compose.yml`：

```yaml
services:
  cheesewaf:
    image: cheesewaf:latest
    build:
      context: .
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
      - "9443:9443"
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
本地构建镜像时，构建上下文（context）须指向 CheeseWAF 项目的根目录。
{{% /pageinfo %}}

## 启动与初始化 {#start}

执行以下命令在后台启动服务并查看日志：

```bash
docker compose up -d
docker compose logs -f cheesewaf
```

容器在启动时会为管理平面自动生成自签名 TLS 证书，并在标准输出日志中打印首次初始化的 Token 令牌。使用浏览器访问 `https://<服务器IP>:9443/setup`，根据向导提示完成初始化。

执行 `docker compose down` 停止容器时，持久化命名卷 `cheesewaf-data`（保存 SQLite 数据库与站点配置）与 `cheesewaf-logs` 均会被完整保留。
