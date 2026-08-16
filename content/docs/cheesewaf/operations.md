---
title: System Operations & Account Security
linkTitle: Operations
weight: 180
description: Administrator credentials, TOTP two-factor authentication (2FA), NTP time synchronization, and OTA automated software updates.
---

CheeseWAF provides comprehensive administrative and operational capabilities to ensure long-term stability and account security. Configure these settings visually under **Users**, **System**, and **Updates** in the Web console.

## 1. User Accounts & Multi-Factor Authentication (2FA) {#users}

- **User Lifecycle**: Manage administrative and operator accounts via `GET/POST /api/users` and `PUT /api/users/{id}`.
- **Two-Factor Authentication (TOTP)**: Users can configure TOTP authenticator apps (such as Google Authenticator) via `/api/users/{id}/2fa/setup`, `enable`, `disable`, and `recover`.
- **Terminal User Management**: Manage accounts, passwords, and 2FA secrets directly in the terminal using `cheesewaf user`.

{{% pageinfo color="tip" %}}
Do not share root administrator credentials among team members. Provision dedicated user accounts assigned the `readonly` role for operational staff who only require log querying and dashboard viewing privileges.
{{% /pageinfo %}}

## 2. NTP Time Synchronization {#time}

Accurate system time is critical for TOTP two-factor verification, JWT token timestamp validation (`exp`/`nbf`), and distributed cluster consensus:

- **Check Clock Status**: Query current clock synchronization state via `GET /api/system/time-sync`.
- **Clock Source Reselection**: Trigger clock source reselection via `POST /api/system/time-sync/reselect`.
- **Manual Force Sync**: Trigger immediate time synchronization via `POST /api/system/time-sync/sync`.

If users encounter unexpected "Invalid Token" or TOTP verification failures, verify host NTP synchronization before troubleshooting other components.

## 3. Automated OTA Software Updates {#updates}

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

- **Rule Hot-Updates**: Setting `auto_update_rules: true` allows the daemon to automatically download updated threat signatures and intelligence feeds without service restarts.
- **Binary Upgrades**: Keep `auto_update_binary: false` in production environments until the update channel and distribution server are thoroughly verified.
- **Cryptographic Verification**: Always enforce `verify_signature: true` to prevent unauthorized firmware or tampering.

## 4. System Settings & Version Queries {#system}

- **System Preferences**: Read and update runtime parameters via `GET /api/system` and `PUT /api/system`.
- **Version Query**: Query software build version, release channel, and Git commit hash via `GET /api/version`.

For automated backup routines and disk space reclamation, see [Storage Sinks & Task Scheduling](../storage/).
