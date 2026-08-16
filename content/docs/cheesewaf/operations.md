---
title: Operations
linkTitle: Operations
weight: 180
description: Users, 2FA, time sync, OTA updates, and system maintenance.
---

Console: **Users**, **System**, **Updates**.

## Users {#users}

`GET/POST /api/users`, `PUT /api/users/{id}`.
Each user can enable TOTP: `/api/users/{id}/2fa/setup`, `enable`, `disable`, `recover`.

CLI: `cheesewaf user`.

Do not share the first admin password.
Create a `readonly` role account for people who only need logs.

## Time sync {#time}

`GET /api/system/time-sync` shows the current clock source.
`POST /api/system/time-sync/reselect` picks again.
`POST /api/system/time-sync/sync` syncs now.

JWT and TOTP break when the host clock is wrong.
Fix time before you debug “invalid token”.

## Updates {#updates}

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

Keep `auto_update_binary` false until you trust the OTA server and the public key.
`verify_signature` must stay true.

## System {#system}

`GET /api/system` and `PUT /api/system` read and write system settings.
`GET /api/version` prints the running version.

See also [Storage and scheduler](../storage/) for backup and cleanup.
