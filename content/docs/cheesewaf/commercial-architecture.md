---
title: Commercial Platform Architecture
linkTitle: Commercial Architecture
weight: 130
description: CheeseWAF control plane, data plane, plugins, CRP, offline mode, diagnostics, and recovery boundaries.
---

This page records the target architecture for future commercial capabilities. It is not a description of services shipped by the current binary. The current runtime uses SQLite for management state, optional PostgreSQL log sinking, memory-only Bot challenges, and a builtin single-node cluster path; configured etcd has no backend coordinator and fails closed.

The CRP package parser/importer and local RuntimeStore now provide a verified local stage/promote/rollback/reopen contract. The CLI exposes `crp verify` and stage-only `crp stage`; `crp activate` and `crp rollback` also exist, but fail closed unless the protected control-plane and sidecar adapters are supplied. They are not yet a complete plugin execution, server startup, cluster distribution, or OTA lifecycle. CWEDP/NetLease transport is implemented as an independently tested package boundary; main-service, node-registration, installation, and production orchestration remain future integration work.

## Data plane and control plane

The WAF data plane performs bounded low-latency inspection, proxying, and policy snapshot evaluation. A future `cheesewaf-control` service is intended to own approvals, Tokens, CRP, permissions, audit, and desired state. The current standalone command boundary, probes, and fail-closed startup behavior are documented in [Standalone Control Runtime](../control-plane-runtime/). Plugins, external persistence, and lease services are not active runtime dependencies today.

The target design uses PostgreSQL for durable management data, native-raft for membership, epochs, fencing, desired configuration, and rollback references, and Redis for short-lived leases and cache. None of these target roles replaces the current SQLite management store yet.

## Plugins and CRP

The target package model uses a CheeseSec Vendor Root and threshold signatures. The 2-of-3, 3-of-5, enterprise namespace, and default trust rules are proposals, not enforced by the current runtime.

The target CRP importer validates format, digests, signatures, namespace, source, and version; the local CLI now exposes verification/staging with explicit trust roots and source registrations. Revocation/transparent-log enforcement and server-side activation are not currently exposed as a production runtime import path.

The current Ansible exporter provisions CheeseWAF infrastructure only. The internal CWEDP protocol/broker, PostgreSQL resume store, broker-bound HTTP/file transport, and NetLease boundary cover HELLO/CAPABILITIES negotiation, offline-source selection, source quarantine, bounded chunk resume, idempotency, direct-IP dialing, TLS/mTLS/NodeID/leaf pinning, and MD5/SHA-1/SHA-256 verification. They are not wired into the main `serve` process, node registration, plugin installation, or production orchestration. CRP installation, upgrade, rollback, and end-to-end OTA distribution are therefore not performed by the current exporter or server.

The cross-repository handoff is explicit: Ansible may bootstrap infrastructure, the CheeseWAF control plane, and a distribution agent. It must not install, upgrade, roll back, sign, promote, or rewrite plugin CRPs. Authenticated, self-negotiating CWEDP owns that lifecycle; peers, mirrors, OTA endpoints, and Ansible bundles are transport sources only and cannot change a manifest, signature set, source root, release sequence, or promotion state.

DuckDB is an optional, disabled-by-default sidecar or CLI for cross-cluster analysis and audit. It reads asynchronously written Parquet and stays outside inline authorization, the WAF request path, PostgreSQL, native-raft, and Redis.

## Offline mode

The target offline mode would keep management extensions from initiating external connections while allowing the data plane to reach configured origins. The current binary has no separate plugin egress controller.

The local `cheesewaf temporary-online probe` already provides a one-shot HTTPS broker with administrator confirmation, direct-IP TLS pinning, bounded accounting, and metadata audit. Plugin/control-plane lease issuance, `serve` startup wiring, durable lease lifecycle, and host-level egress enforcement are still not exposed as a production API.

## Diagnostic upload

The target design limits diagnostic uploads to an asynchronous, redacted API. The current runtime has no plugin upload endpoint, so these rules are prospective.

Envelope encryption, object storage delivery, and resumable queues are planned safeguards; they are not active services in the current binary.

## Operations

- High-risk actions require an explicit first confirmation; repeated prompts can be reduced within the same authorization scope, while material changes require re-confirmation.
- Object storage, transparency logs, SIEM, KMS, LLM, or Redis failures change the related management task state only.
- A verified last-known-good version continues to run; high-risk new actions enter pending or staged when evidence is insufficient.
- Confirmations, network leases, uploads, replication, receipts, deletion, revocation, and recovery are auditable.
