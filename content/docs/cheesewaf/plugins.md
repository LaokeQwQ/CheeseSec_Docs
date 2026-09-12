---
title: Plugins & CRP Specification
linkTitle: Plugins & CRP
weight: 105
description: CheeseSec plugin distribution model, CRP v1 offline resource package format, Ed25519 signature verification, staging lifecycle, and extension boundaries.
---

The CheeseSec plugin model uses an offline-first design to eliminate external runtime dependencies and supply chain risks. All extensions are published, verified, staged, and distributed through strictly bounded **CRP (CheeseWAF Resources Package)** archives. Specifications and trust policies are maintained in [CheeseSec_Plugin](https://github.com/LaokeQwQ/CheeseWAF-Plugins) and [CheeseSec_Plugin_Docs](https://github.com/LaokeQwQ/CheeseSec_Plugin_Docs).

## CRP v1 Archive Layout {#crp-spec}

The CheeseWAF CRP v1 parser requires resource packages to be standard ZIP archives containing **only** the following three entries. Any extra files or unknown directories cause immediate admission rejection (Hard Reject):

```text
my-plugin-v1.0.0.crp (ZIP archive)
├── manifest.json              # Package metadata manifest
├── artifact/                  # Single payload directory
│   └── payload.bin            # Binary payload artifact
└── signatures/
    └── manifest.json          # Offline Ed25519 signature bundle
```

### Manifest Schema Reference

The `manifest.json` file uses strict schema validation and rejects unknown JSON properties:

| Field Name | Type | Description |
| --- | --- | --- |
| `api_version` | String | Manifest specification version (fixed to `crp/v1`) |
| `kind` | String | Resource package type (`detector`, `model`, or `ruleset`) |
| `name` | String | Human-readable plugin name |
| `plugin_id` | String | Globally unique plugin identifier |
| `version` | String | Semantic version string (e.g., `1.0.0`) |
| `namespace` | String | Plugin namespace (`official`, `enterprise`, or `community`) |
| `publisher` | String | Publisher entity name |
| `source` | String | Distribution source ID (must exist in trusted source registry) |
| `source_root` | String | Identifier of the bound signature trust root |
| `release_sequence` | Integer | Monotonically increasing sequence number (rollback rejected) |
| `digests` | Object | Multi-algorithm digests of the archive (SHA-256, SHA-1, MD5) |
| `artifact` | Object | Artifact descriptor containing `name`, `size`, and digests |

## Signature Verification & Offline Admission {#security}

CRP archives require multi-party threshold signatures using Ed25519:

- **Trust Roots & Source Registry**: Admission verifies public key fingerprints and validity windows against `policy/trust-roots.json` and `policy/source-registry.json`. No outbound CRL or OCSP network calls are made.
- **Signature Thresholds**: Defined by `policy/trust-levels.json`, requiring official packages to meet threshold criteria (such as 2-of-3 quorum signatures).
- **Air-Gapped Operation**: In air-gapped environments, the daemon verifies complete cryptographic integrity locally as long as trust roots are installed.

## Command-Line Operations {#cli}

CheeseWAF provides dedicated subcommands for offline verification and local staging:

### 1. Verify Package (`crp verify`)

Validates archive format, digest consistency, and signatures without installing, executing, or accessing the network:

```bash
cheesewaf crp verify \
  --package ./plugin.crp \
  --trust-roots ./trust-roots.json \
  --sources ./sources.json \
  --now 2026-09-08T12:00:00Z
```

### 2. Stage Package (`crp stage`)

Persists verified packages into protected, content-addressed staging slots (restricted to owner-only read/write permissions, without activating):

```bash
cheesewaf crp stage \
  --package ./plugin.crp \
  --trust-roots ./trust-roots.json \
  --sources ./sources.json \
  --runtime-dir /var/lib/cheesewaf/crp-runtime \
  --now 2026-09-08T12:00:00Z
```

### 3. Explicit Temporary HTTPS Probe (`temporary-online probe`)

For constrained environments requiring remote connectivity testing, CheeseWAF provides an explicit, single-use HTTPS probe. This command requires administrator password stdin, TLS leaf certificate pinning, and records metadata-only audit logs to `<data-dir>/audit/netlease.jsonl`:

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

## Distribution Endpoints {#endpoints}

- **Catalog Service**: `https://store.cheesesec.com` (read-only metadata)
- **OTA Index Service**: `https://ota.cheesesec.com` (read-only release indices)
- **Immutable Resource Store**: `https://res.cheesesec.com` (read-only SHA-256 content-addressed artifacts)

## Offline Analytics Boundary (DuckDB) {#duckdb}

DuckDB is planned strictly as an optional sidecar or CLI extension for offline log querying. **It is never included in the real-time request forwarding path.** Access logs are streamed asynchronously into Parquet files, which the DuckDB process reads as immutable snapshots. DuckDB does not share database handles with the CheeseWAF daemon or act as a cluster coordinator.
