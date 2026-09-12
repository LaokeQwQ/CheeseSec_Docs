---
title: 插件体系与 CRP 规范
linkTitle: 插件与 CRP
weight: 105
description: CheeseSec 插件分发体系、CRP v1 离线资源包结构、Ed25519 签名验证、暂存运行机制及生态扩展边界。
---

CheeseSec 插件体系采用安全优先的离线化设计。为了消除不可控依赖与供应链投毒风险，所有扩展组件均通过结构严格受限的 **CRP (CheeseWAF Resources Package)** 资源包进行发布、验签、暂存与分发。发布源与开发者规范由 [CheeseSec_Plugin](https://github.com/LaokeQwQ/CheeseSec_Plugin) 与 [CheeseSec_Plugin_Docs](https://github.com/LaokeQwQ/CheeseSec_Plugin_Docs) 维护。

## CRP v1 归档结构规范 {#crp-spec}

当前 CheeseWAF CRP v1 解析器要求资源包必须为标准 ZIP 归档，且内部**必须且仅允许**包含以下三类条目，包含任何多余文件或未知目录均会被硬阻断（Hard Reject）：

```text
my-plugin-v1.0.0.crp (ZIP 归档)
├── manifest.json              # 核心元数据清单
├── artifact/                  # 单一有效载荷文件
│   └── payload.bin            # 插件实体产物
└── signatures/
    └── manifest.json          # 离线 Ed25519 签名集合
```

### Manifest 元数据清单字段

`manifest.json` 采用严格白名单校验，拒绝未知字段。核心字段包括：

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `api_version` | String | 清单协议版本（固定为 `crp/v1`） |
| `kind` | String | 资源包类型（如 `detector`、`model`、`ruleset`） |
| `name` | String | 插件人类可读名称 |
| `plugin_id` | String | 全局唯一插件标识符 |
| `version` | String | 语义化版本号（如 `1.0.0`） |
| `namespace` | String | 命名空间（支持官方、企业及社区命名空间） |
| `publisher` | String | 实体发布者名称 |
| `source` | String | 发布来源标识（必须已注册于信任来源表） |
| `source_root` | String | 绑定的签名信任根标识 |
| `release_sequence` | Integer | 单调递增发布序号（禁止回退） |
| `digests` | Object | 包级别的多算法哈希摘要（SHA-256、SHA-1、MD5） |
| `artifact` | Object | 载荷声明（包含 `name`、`size` 及各算法摘要） |

## 签名验证与离线准入机制 {#security}

CRP 资源包采用离线多方阈值签名（Ed25519）：

- **信任根与来源注册**：准入引擎依据 `policy/trust-roots.json` 与 `policy/source-registry.json` 校验公钥指纹与签名有效期，不向公网发起证书吊销列表（CRL）或 OCSP 请求。
- **签名阈值判定**：根据 `policy/trust-levels.json` 要求官方包具备法定阈值签名（如 2-of-3 密钥多签）。
- **零网络准入**：在纯离线隔离环境中，只要信任根配置就绪，WAF 即可完成全套完整性与合法性校验。

## 命令行运维与本地操作 {#cli}

CheeseWAF 命令行工具提供了原子化的离线检验与安全暂存命令：

### 1. 离线验签 (`crp verify`)

校验本地 `.crp` 资源包的格式、哈希一致性及签名有效性（不安装、不执行、不联网）：

```bash
cheesewaf crp verify \
  --package ./plugin.crp \
  --trust-roots ./trust-roots.json \
  --sources ./sources.json \
  --now 2026-09-08T12:00:00Z
```

### 2. 离线暂存 (`crp stage`)

将通过校验的合规产物保存至本地受保护的内容寻址暂存槽位中（权限收紧为仅属主可读写，不自动激活）：

```bash
cheesewaf crp stage \
  --package ./plugin.crp \
  --trust-roots ./trust-roots.json \
  --sources ./sources.json \
  --runtime-dir /var/lib/cheesewaf/crp-runtime \
  --now 2026-09-08T12:00:00Z
```

### 3. 显式临时出站探测 (`temporary-online probe`)

针对必须进行远端联调的受限场景，CheeseWAF 提供唯一挂载的临时 HTTPS 探测通道。该命令要求管理员交互式输入密码，并绑定精确的 TLS 叶证书 Pin，所有网络进出均以结构化审计日志落盘：

```bash
cheesewaf temporary-online probe \
  --administrator admin \
  --password-stdin \
  --plugin-id my-plugin \
  --plugin-version 1.0.0 \
  --host updates.cheesesec.com \
  --leaf-pin sha256:abcd... \
  --ttl 60s
```

## 官方发布渠道与生态端点 {#endpoints}

- **插件目录服务**：`https://store.cheesesec.com` (只读元数据拉取)
- **OTA 索引端点**：`https://ota.cheesesec.com` (只读增量版本引索)
- **不可变对象存储**：`https://res.cheesesec.com` (基于 SHA-256 内容寻址的只读资源)

## 扩展分析边界（DuckDB） {#duckdb}

DuckDB 仅规划作为可选的离线分析与审计 CLI/Sidecar 扩展，**严禁引入实时 WAF 请求转发热路径**。日志数据由异步流管道写入 Parquet 文件，分析进程以只读快照形式读取，不与 CheeseWAF 核心共享数据库写句柄，亦不充当集群协调器。
