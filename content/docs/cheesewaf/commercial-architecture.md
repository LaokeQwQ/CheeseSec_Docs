---
title: Commercial Platform Architecture
linkTitle: Commercial Architecture
weight: 130
description: CheeseWAF control plane, data plane, plugins, CRP, offline mode, diagnostics, and recovery boundaries.
---

This document outlines the architecture specifications for CheeseWAF commercial platforms, covering control planes, data planes, plugin security standards, and air-gapped operations.

## Data Plane and Control Plane

The architecture strictly decouples traffic inspection from administrative management:
- **WAF Data Plane**: Dedicated to high-throughput inspection, reverse proxy forwarding, and local policy snapshot evaluation with minimal latency.
- **Dedicated Control Plane (`cheesewaf-control`)**: Orchestrates cluster topology, policy updates, and cluster-wide state convergence, exposing loopback-bound health, readiness, and proposal endpoints. See [Standalone Control Runtime](../control-plane-runtime/) for runtime details.
- **State Storage & Clustering**: Production deployments support external PostgreSQL for durable management state, native-raft for cluster consensus and topology synchronization, and Redis for distributed leases and ephemeral caching. Missing production dependencies fail closed to ensure state integrity.

## Security Plugins & CRP Specification

CRP (CheeseWAF Resources Package) defines the distribution format for offline security rules:
- **Trust Roots & Signatures**: Supports official Vendor Roots and enterprise private roots using Ed25519 threshold signatures (such as 2-of-3 signatures).
- **Verification & Staging**: The CLI provides `crp verify` and `crp stage` commands to validate digests, check release sequences, and stage assets into content-addressed runtime paths.
- **Activation & Rollback**: Production CRP workflows leverage policy snapshots, native-raft fencing, and mTLS verification to ensure zero-downtime, tamper-proof activations and atomic rollbacks.
- **Release & Updates**: Validates signed package indices over read-only HTTPS, preserving cryptographic verification and deterministic staging.

DuckDB serves as an offline analytics extension, executing asynchronous one-shot jobs over redacted Parquet audit snapshots to output structured `analysis-record/v1` entries, operating completely out-of-band to prevent interference with real-time request processing.

## Air-gapped Operations & Ephemeral Egress

In air-gapped or restricted VPC environments, offline policies deny unsolicited outbound connections while preserving data plane routing to upstreams:
- The `cheesewaf temporary-online probe` utility provides an ephemeral HTTPS broker with administrator approval, IP/TLS certificate pinning, and audit logging.
- Outbound access requires explicit operator confirmation and time-bounded leases.

## Diagnostics & Operational Safety

- Diagnostic payloads enforce schema validation and redaction to prevent sensitive business information from leaving the cluster.
- Administrative workflows adhere to safe operational principles: explicit confirmation for high-risk actions, reduced prompts within active sessions, and re-confirmation upon environment changes.
