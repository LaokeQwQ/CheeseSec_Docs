---
title: Operations & Security Hardening
linkTitle: Operations
weight: 180
description: User administration, TOTP two-factor authentication (2FA), NTP time synchronization, update capability status, and supply chain signature verification.
---

This section outlines standard operational procedures and hardening requirements for running CheeseWAF in production. Corresponding UI modules in the Web Console include **Users**, **System**, and **Updates**.

The only currently runnable management profile is `storage.profile: temporary`, which stores users, sessions, and management state in embedded SQLite. `storage.profile: production` is reserved for a future management path and currently fails closed because the management PostgreSQL, Coordinator, and native-raft cluster/epoch backend are not wired into the startup unit.

`storage.postgresql` is an optional asynchronous access-log sink; it is not the management database. A configured `storage.redis` endpoint may be connectivity-tested, but bot challenge state still uses the in-process memory backend, and `protection.bot.challenge_backend: redis` is rejected. `cheesewaf crp verify` performs bounded offline verification, while `cheesewaf crp stage` persists a verified local package in a staged slot. `cheesewaf crp activate` and `cheesewaf crp rollback` exist, but require protected control-plane/sidecar adapters and fail closed when those dependencies are absent. The local RuntimeStore is not connected to plugin execution, server startup, cluster distribution, promotion approvals, or OTA downloading.

The current CWEDP/NetLease packages include broker-bound HTTP/file transport, one-shot lease checks, direct-IP dialing, TLS/mTLS/NodeID/leaf pinning, Range resume, and source quarantine. These packages are not yet mounted into the main `serve` process, node registration, or a complete plugin installation/OTA lifecycle. The local `cheesewaf temporary-online probe` is a separate one-shot operator tool; it is not the production plugin egress API.

## 1. User Administration & CLI Credentials {#users}

- **One identity rule**: Setup, the Web Console, REST API, CLI, storage, human JWT claims, and login CAPTCHA receipts use the same username form. Usernames are 3–32 ASCII characters, start with an ASCII letter, end with an ASCII letter or digit, and contain only ASCII letters, digits, `.`, `_`, and `-`. Non-ASCII characters, Unicode whitespace, control characters (`Cc`), and format/invisible characters (`Cf`) are rejected. The server preserves the exact input and never trims or lowercases usernames, so `admin` and ` admin ` are different strings and the latter is invalid.
- **Role input**: A user `role` must exactly match a configured key in `apisec.permissions` (normally `admin` or `readonly`). Empty or unknown roles, `*`/`:` permission expressions, and roles containing leading, trailing, or embedded Unicode whitespace, control characters (`Cc`), or format/invisible characters (`Cf`) are rejected. The server does not trim or case-normalize roles; invalid account fields return `USERNAME_INVALID` or `ROLE_INVALID`.
- **Web Console & REST API**: Administer accounts programmatically via `GET/POST /api/users` and `PUT /api/users/{id}`. The same validation applies to Web Users, Setup, and login.
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

  # Repair a historical non-canonical username by immutable user ID
  cheesewaf user repair-username USER_ID recovered_admin --reason 'Historical whitespace in imported account'
  ```
- Use `user rename` when the current username is already canonical. Both the old and new values must pass the canonical rule. The CLI updates that account and revokes all of its unrevoked sessions, but it does not create a historical-repair audit record; this path cannot select a historical non-canonical username. Only `repair-username` bundles the username change, session revocation, and audit insert in one transaction.
- Use `user repair-username` only for a historical non-canonical username such as ` admin `. It requires `--reason` and an exact immutable user ID. It rejects a missing user, a canonical current username, or a target username owned by another account. It never merges accounts. The username update, revocation of every unrevoked admin session for that user, and append-only audit record commit in one SQLite transaction. The user ID, password hash, role, TOTP enabled state, and TOTP secret remain unchanged. The audit records the current OS user ID, supplied reason, old and new usernames, revoked-session count, and time. Neither path silently trims or lowercases a username.
- Run the repair as the same OS account that owns the CheeseWAF data. The audit actor is derived from the current OS user ID; running the command through an unrelated account changes that evidence.
- **Password policy**: New passwords need at least 10 characters and at least 3 of 4 classes: uppercase, lowercase, non-repeating digits, and special characters. Common or simple patterns, including sequential or keyboard-like patterns, are rejected. A password cannot equal or contain the username. Prefer `--password-stdin`; direct `--password` values can enter shell history or process listings.
- **Principle of Least Privilege**: Create dedicated `readonly` accounts for operational auditing to avoid sharing root administrative credentials.
- **Two-Factor Authentication (2FA/TOTP)**: Configure TOTP using `/api/users/{id}/2fa/setup` to generate seeds and QR codes; manage state via `enable`, `disable`, and `recover`.
- A management API token's display note is metadata, not an account username. It is not validated with the account username rule and must not be used as the authenticated human identity. Management API Tokens default to 90 days and allow at most 365 days; the running service removes expired or 180-day-inactive tokens in a coalesced cleanup worker and attempts an audit entry plus administrator notification.
- The Web System page contains a second-confirmation dialog for non-expiring Tokens, but the option is disabled until the confirmation verifier is configured. The current runtime does not yet connect `ApprovalGate`, current-password/TOTP verification, or the 10-second warning delay; non-expiring creation therefore returns `API_TOKEN_CONFIRMATION_UNAVAILABLE`.

To find a user ID without reading password hashes or TOTP secrets, use the SQLite CLI in read-only mode and select only the ID and a quoted username:

```bash
DB=/var/lib/cheesewaf/cheesewaf.db
sqlite3 -readonly "$DB" \
  'SELECT id, quote(username) AS username FROM users ORDER BY username;'
```

`quote(username)` makes leading or trailing spaces visible. Do not use `SELECT *`, and do not paste this output into tickets or logs.

## 2. Back Up and Migrate the SQLite Management Store {#sqlite-maintenance}

Before a username repair or binary upgrade, resolve the active database from `storage.sqlite.path` and confirm that the file and its parent directory are the expected runtime paths. The usual defaults are `./data/cheesewaf.db` for a local run and `/var/lib/cheesewaf/cheesewaf.db` for a Linux service. Do not point these commands at the tracked `configs/cheesewaf.yaml` template.

An active SQLite database normally uses WAL mode. Do not copy only the main `.db` file while CheeseWAF is running; recent commits may still be in `-wal`, and the copy may not be restorable. An online backup reads a consistent snapshot while the service continues to run:

```bash
DB=/var/lib/cheesewaf/cheesewaf.db
BACKUP_DIR=/var/backups/cheesewaf
test -f "$DB" || { echo "database not found: $DB" >&2; exit 1; }
install -d -m 700 "$BACKUP_DIR"
df -h "$BACKUP_DIR"
du -h "$DB"
BACKUP="$BACKUP_DIR/cheesewaf-before-maintenance-$(date -u +%Y%m%dT%H%M%SZ).db"
test ! -e "$BACKUP" || { echo "backup path already exists: $BACKUP" >&2; exit 1; }
sqlite3 -readonly "$DB" ".backup '$BACKUP'"
chmod 600 "$BACKUP"
test -s "$BACKUP" || { echo "backup is empty: $BACKUP" >&2; exit 1; }
integrity=$(sqlite3 -readonly "$BACKUP" 'PRAGMA integrity_check;')
test "$integrity" = ok || { echo "backup integrity check failed: $integrity" >&2; exit 1; }
sha256sum "$BACKUP" > "$BACKUP.sha256"
sha256sum -c "$BACKUP.sha256"
```

The integrity check must return `ok`, and the final checksum command must report `OK`. Stop if either check fails. Keep the backup in a protected location and copy it off-host according to the retention policy. The backup contains sensitive management data; never upload it to a ticket or paste it into a chat. Check free disk space before starting, and monitor WAF health and disk latency during the backup. The single CheeseWAF binary serves both the data plane and management plane, so stopping it can interrupt protection and traffic.

If an online backup is not possible, stop only the exact CheeseWAF writer through its service manager, confirm that no CheeseWAF process is writing, and copy a consistent database set including any adjacent `-wal` and `-shm` files. Validate the copy with `PRAGMA integrity_check;` before restarting the service. Do not use a broad process-stop command.

The current binary applies ordered SQLite migrations when it opens the store. The current schema is version 5. Migration 3 to 4 creates the append-only `user_username_repairs` audit table, and migration 4 to 5 adds `credential_epoch` to `users` and `admin_sessions`. Security changes advance the user epoch, and active sessions must match the current epoch. These migrations do not trim, lowercase, merge, or otherwise rewrite existing accounts. A binary that supports only an older schema rejects a newer database with `newer SQLite schema version`.

For a downgrade, restore and validate the backup taken before the upgrade, then start the older binary only after the exact service and data paths have been checked. Do not lower `PRAGMA user_version` by hand. If a username repair succeeds but must be undone, restore the pre-repair backup during a planned maintenance window; `repair-username` intentionally refuses to turn a canonical username back into an invalid one.

## 3. Support Bundle Packaging & CLI Localization {#cli-maintenance}

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

## 4. NTP Time Synchronization {#time}

JWT signature verification, TOTP token calculations, and cluster consensus rely on synchronized clocks:

- **Query Clock Sources**: Call `GET /api/system/time-sync` to inspect offsets and active NTP servers.
- **Force Resynchronization**: Call `POST /api/system/time-sync/sync` to trigger immediate alignment.
- **Reselect Lowest-Latency Peer**: Call `POST /api/system/time-sync/reselect` to discover and switch to the lowest-latency NTP pool.

## 5. OTA Capability Status {#updates}

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

- **Current runtime boundary**: The configuration keys are reserved for the OTA updater, but the current binary has no updater worker. The Updates page reports `NOT_IMPLEMENTED`, and enabling OTA through the system API is rejected with `OTA_UPDATES_UNAVAILABLE`.
- **Configuration safety**: Keep `enabled: false` until an updater worker is shipped. The validator still checks the server URL, channel, interval, and signature settings when OTA is enabled.
- **Future behavior**: `auto_update_rules`, `auto_update_binary`, and `verify_signature` describe the intended signed-update policy; they do not mean that rule or binary downloads run today.

## 6. Software Supply Chain Security & Integrity {#supply-chain}

Use only the release metadata that is actually published for the version you are deploying. The runtime does not create or verify a release signature on your behalf:

- **SBOM**: If the release publishes a CycloneDX or SPDX SBOM, retain it with the deployment record and compare the listed version and digest to the artifact you received.
- **Container signatures**: If the release publishes a Cosign signature, verify it against the exact image reference before deployment.
- **Windows signatures**: If a Windows package includes Authenticode metadata, verify the signer and certificate chain on the machine that will install it.
- **Checksums**: If the release publishes a checksum file, verify the exact artifact with `sha256sum -c checksums.txt` or the platform equivalent.
