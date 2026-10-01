---
title: Commercial Platform Architecture
linkTitle: Commercial Architecture
weight: 130
description: CheeseWAF control plane, data plane, plugins, CRP, offline mode, diagnostics, and recovery boundaries.
---

This document outlines the architecture specifications for CheeseWAF commercial platforms, covering control planes, data planes, plugin security standards, and air-gapped operations.

## Data Plane and Control Plane

The architecture strictly decouples traffic inspection from administrative management:
- **WAF Data Plane**: Handles request inspection, reverse proxying, and evaluation against the active policy snapshot. This document makes no numeric latency or throughput guarantee.
- **Dedicated Control Plane (`cheesewaf-control`)**: The current command can connect to PostgreSQL and native-raft and exposes loopback-bound health, readiness, status, and proposal endpoints. It is not yet a complete remote management API or the main WAF's high-availability control plane. See [Standalone Control Runtime](../control-plane-runtime/) for its runtime boundary.
- **State Storage**: The code includes PostgreSQL, Redis, and native-raft adapters. Production mode requires explicit dependencies and fails closed when they are missing; the adapters alone do not prove a completed multi-node deployment or disaster-recovery drill.

## Security Plugins & CRP Specification

CRP (CheeseWAF Resources Package) defines the distribution format for offline security rules:
- **Trust Roots & Signatures**: Supports official Vendor Roots and enterprise private roots using Ed25519 threshold signatures (such as 2-of-3 signatures).
- **Verification & Staging**: The CLI provides `crp verify` and `crp stage` commands to validate digests, check release sequences, and stage assets into content-addressed runtime paths.
- **Activation & Rollback**: Production CRP routes use PostgreSQL authorization, native-raft fencing, and an mTLS sidecar; operations fail closed when required dependencies are missing. This does not mean every plugin has an executable runtime.
- **OTA Status**: The current OTA client validates a read-only HTTPS index and retains last-known-good file state. A candidate does not trigger download, installation, or activation.

DuckDB analysis is a planned plugin extension: the host supplies the engine, and an asynchronous one-shot job reads verified, redacted Parquet snapshots and emits only `analysis-record/v1`. It must stay outside the request path and cannot change WAF policy directly. CheeseWAF has no DuckDB job runtime or audit exporter yet; integration still requires input verification, an OS sandbox, and resource limits.

## Air-gapped Operations & Ephemeral Egress

In air-gapped or restricted VPC environments, offline policies deny unsolicited outbound connections while preserving data plane routing to upstreams:
- The `cheesewaf temporary-online probe` utility provides an ephemeral HTTPS broker with administrator approval, IP/TLS certificate pinning, and audit logging.
- Outbound access requires explicit operator confirmation and time-bounded leases.

## Diagnostics & Operational Safety

- Diagnostic payloads enforce schema validation and redaction to prevent sensitive business information from leaving the cluster.
- Administrative workflows adhere to safe operational principles: explicit confirmation for high-risk actions, reduced prompts within active sessions, and re-confirmation upon environment changes.
