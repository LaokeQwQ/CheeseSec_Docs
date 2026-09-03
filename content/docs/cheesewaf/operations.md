---
title: Operations & Security Hardening
linkTitle: Operations
weight: 180
description: User administration, TOTP two-factor authentication (2FA), NTP time synchronization, OTA rule updates, and supply chain signature verification.
---

This section outlines standard operational procedures and hardening requirements for running CheeseWAF in production. Corresponding UI modules in the Web Console include **Users**, **System**, and **Updates**.

## 1. User Administration & CLI Credentials {#users}

- **Web Console & REST API**: Administer accounts programmatically via `GET/POST /api/users` and `PUT /api/users/{id}`.
- **Command-Line Operations (`cheesewaf user`)**:
  ```bash
  # Recommended for scripts: read the password from stdin (avoid shell history/process listings)
  cheesewaf user password admin --password-stdin < secret.txt

  # One-off shell use only: explicit password (choose exactly one input mode)
  read -r -s -p 'New password: ' CHEESEWAF_NEW_PASSWORD; printf '\n'
  cheesewaf user password admin --password "$CHEESEWAF_NEW_PASSWORD"

  # Auto-generate a strong password and disable TOTP 2FA (emergency recovery)
  cheesewaf user password admin --generate --reset-2fa

  # Ensure an admin user exists and read password from stdin (useful for automated scripts)
  cheesewaf user ensure-admin admin --password-stdin < secret.txt

  # Rename a local user
  cheesewaf user rename old_admin new_admin
  ```
- **Principle of Least Privilege**: Create dedicated `readonly` accounts for operational auditing to avoid sharing root administrative credentials.
- **Two-Factor Authentication (2FA/TOTP)**: Configure TOTP using `/api/users/{id}/2fa/setup` to generate seeds and QR codes; manage state via `enable`, `disable`, and `recover`.

## 2. Support Bundle Packaging & CLI Localization {#cli-maintenance}

- **Support Bundle Archiving**: When troubleshooting issues, package all runtime logs into a standardized, timestamped ZIP archive:
  ```bash
  cheesewaf logs pack --dir /tmp --name cheesewaf-support.zip
  ```
- **CLI Interface Language**:
  ```bash
  # Display current language and supported options
  cheesewaf lang show

  # Persistently set CLI locale (supports en and zh-CN)
  cheesewaf lang set en
  ```

## 3. NTP Time Synchronization {#time}

JWT signature verification, TOTP token calculations, and cluster consensus rely on synchronized clocks:

- **Query Clock Sources**: Call `GET /api/system/time-sync` to inspect offsets and active NTP servers.
- **Force Resynchronization**: Call `POST /api/system/time-sync/sync` to trigger immediate alignment.
- **Reselect Lowest-Latency Peer**: Call `POST /api/system/time-sync/reselect` to discover and switch to the lowest-latency NTP pool.

## 4. OTA Automated Updates {#updates}

```yaml
update:
  ota:
    enabled: false
    server: ""
    channel: "stable"
    check_interval: 6h
    auto_update_rules: true
    auto_update_binary: false
    verify_signature: true
```

- **Automated Signature Updates**: When `auto_update_rules: true` is set, the daemon regularly checks for updated threat intelligence feeds and detection signatures.
- **Controlled Binary Upgrades**: In enterprise environments, keep `auto_update_binary: false` and deploy binaries through controlled configuration management.
- **Cryptographic Verification**: `verify_signature` must remain `true` to ensure update packages are signed and intact.

## 5. Software Supply Chain Security & Integrity {#supply-chain}

All official CheeseWAF binaries and container images comply with rigorous supply-chain security standards:

- **Software Bill of Materials (SBOM)**: Every release includes standard CycloneDX and SPDX SBOMs generated via Syft, detailing all upstream dependencies and license metadata.
- **Cosign Container Signatures**: Container images on Docker Hub and GitHub Packages are cryptographically signed using Sigstore/Cosign. Verify authenticity prior to deployment via `cosign verify`.
- **Windows Authenticode Signatures**: Windows installers and executables carry official Authenticode certificates, ensuring Windows SmartScreen does not trigger warnings.
- **SHA256 Checksums**: Every release artifact provides a signed `checksums.txt` file. Verify with `sha256sum -c checksums.txt`.
