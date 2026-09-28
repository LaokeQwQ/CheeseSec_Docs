---
title: Commercial Platform Architecture
linkTitle: Commercial Architecture
weight: 130
description: CheeseWAF control plane, data plane, plugins, CRP, offline mode, diagnostics, and recovery boundaries.
---

This document outlines the architecture specifications for CheeseWAF commercial platforms, covering control planes, data planes, plugin security standards, and air-gapped operations.

## Data Plane and Control Plane

The architecture strictly decouples traffic inspection from administrative management:
- **WAF Data Plane**: Dedicated to high-throughput, low-latency inspection, reverse proxying, and active policy snapshot evaluation, ensuring continuous uptime and sub-millisecond mitigation.
- **Dedicated Control Plane (`cheesewaf-control`)**: Orchestrates approvals, token verification, CRP packages, RBAC permissions, and cluster state synchronization. Operational guidance is documented in [Standalone Control Runtime](../control-plane-runtime/).
- **High-Availability Storage**: Production deployments use external PostgreSQL for persistent management state, native-raft for cluster consensus, and Redis for distributed leases and volatile caching.

## Security Plugins & CRP Specification

CRP (CheeseWAF Resources Package) defines the distribution format for offline security rules:
- **Trust Roots & Signatures**: Supports official Vendor Roots and enterprise private roots using Ed25519 threshold signatures (such as 2-of-3 signatures).
- **Verification & Staging**: The CLI provides `crp verify` and `crp stage` commands to validate digests, check release sequences, and stage assets into content-addressed runtime paths.
- **Infrastructure Orchestration**: Ansible provisions underlying hosts and bootstraps distribution agents, while CWEDP protocols govern package validation, rollback protection, and promotion.

DuckDB serves as an optional offline analytics utility for asynchronous Parquet audit logs, operating strictly outside the inline request path.

## Air-gapped Operations & Ephemeral Egress

In air-gapped or restricted VPC environments, offline policies deny unsolicited outbound connections while preserving data plane routing to upstreams:
- The `cheesewaf temporary-online probe` utility provides an ephemeral HTTPS broker with administrator approval, IP/TLS certificate pinning, and audit logging.
- Outbound access requires explicit operator confirmation and time-bounded leases.

## Diagnostics & Operational Safety

- Diagnostic payloads enforce schema validation and redaction to prevent sensitive business information from leaving the cluster.
- Administrative workflows adhere to safe operational principles: explicit confirmation for high-risk actions, reduced prompts within active sessions, and re-confirmation upon environment changes.
