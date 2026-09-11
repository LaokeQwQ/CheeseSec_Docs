---
title: System Setup & Initialization
linkTitle: Setup
weight: 10
description: Initialize CheeseWAF via the browser Web wizard or the cheesewaf setup terminal command with hardware probing, profiling, and credential configuration.
---

Following a fresh installation, CheeseWAF requires initial administrator provisioning and hardware baseline profiling. CheeseWAF provides both a **Terminal CLI Wizard** and a **Web GUI Wizard**.

## Option 1: Terminal Setup Wizard (Recommended) {#cli-setup}

Run the interactive setup command directly in your terminal:

```bash
cheesewaf setup
```

### 1. Automated Hardware Probing & Profiling

The wizard inspects host resources (logical CPU cores, visible RAM, and an 8 MiB sequential write test) and recommends a runtime profile:

- **`low`**: Recommended for hosts with ≤2 logical cores, ≤2048 MB RAM, or a failed disk write test. A 2-core / 2 GB host belongs in this tier (alias: `minimal`).
- **`medium`**: Requires ≥3 logical cores, ≥4096 MB RAM, and a passing disk write test (alias: `balanced`).
- **`high`**: Requires ≥4 logical cores, ≥8192 MB RAM, and sequential writes of at least 50 MB/s (alias: `performance`).
- **`smart`**: A manually selected adaptive profile matching `web_attack: smart`; it is not a fixed result of the hardware probe.
- **`custom`**: Allows manual tuning of performance and security thresholds.

The probe runs for at most 30 seconds. If it times out, is cancelled, or the Web probe request fails, the wizard recommends the conservative `low` tier. In non-interactive mode, `--skip-probe` also selects `low` unless an explicit `--profile` is provided.

### 2. Guided Credentials & Transactional Safety

- **Username**: Enter a username of 3–32 ASCII characters. It must start with an ASCII letter, end with an ASCII letter or digit, and contain only ASCII letters, digits, `.`, `_`, and `-`. Non-ASCII characters, Unicode whitespace, control characters (`Cc`), and format/invisible characters (`Cf`) are rejected; the server preserves the exact value and does not trim or lowercase it.
- **Password**: New passwords need at least 10 characters and at least 3 of 4 classes: uppercase, lowercase, non-repeating digits, and special characters. Common or simple patterns are rejected, and the password cannot equal or contain the username. The Web review step shows that a password is set; it never displays the password, a password hash, a system master key, or an administrator credential digest.
- **Optional integrations**: The interactive terminal wizard can apply selected GeoIP, Prometheus `/metrics`, and VictoriaLogs settings when it commits the configuration. The Web wizard records integration choices in the setup draft for review; it does not apply them to the live configuration. Configure supported integrations after setup from the relevant System Settings, Storage, or Monitoring pages. The PostgreSQL option is an asynchronous access-log sink, not the management database.
- **Transactional Cleanliness**: Configuration, database, certificate, and administrator state are accumulated in memory and are committed only at the final step. Aborting does not leave partial setup state. The selected CLI language is a separate user preference and may be persisted in `data/cli.lang`; this file is not the runtime configuration or management database.

### 3. Headless Scripted Automation

For CI/CD pipelines or cloud-init automation, use non-interactive command-line flags:

```bash
cheesewaf setup --yes \
  --username admin \
  --password-stdin < /etc/cheesewaf/secrets/admin_pass.txt \
  --admin-listen 127.0.0.1:9443 \
  --skip-probe
```

> **Note**: In automated mode, `--yes` strictly requires `--password-stdin` to guarantee that the administrator password satisfies the credential policy. Upon completion, the wizard prints the canonical `http://` or `https://` panel URL according to the current administrative TLS state.

## Option 2: Browser Web Wizard {#web-setup}

{{% steps %}}

### 1. Open the Setup URL

- **Standalone or non-Docker local machine**: Open `http://127.0.0.1:9443/setup` in your browser.
- **Remote Server (non-Docker)**: Navigate to the configured admin URL (for example, `https://10.0.0.10:9443/setup`) when that listener is reachable and TLS is enabled (accept the self-signed certificate prompt on first visit, if applicable).
- **Docker Compose**: The default Compose file binds the admin port only to the Docker host's loopback interface (`127.0.0.1:9443`). Open `https://127.0.0.1:9443/setup` on that host. From another machine, set `CHEESEWAF_SSH_TARGET` to your SSH target and run `ssh -N -L 9443:127.0.0.1:9443 "$CHEESEWAF_SSH_TARGET"`, then use the same local URL; change the port binding explicitly if direct exposure is required.

The startup log never prints the setup token or the complete URL. It shows only the base setup URL (for example, `http://127.0.0.1:9443/setup`), the protected runtime file path (`setup.url`), and an opaque receipt.

The complete setup URL is stored in `setup.url`, a mode `0600` file with a 10-minute validity period. After setup completes, the setup token is revoked; expired `setup.url` files are cleaned up.

The setup token remains required in `X-CheeseWAF-Setup-Token` until setup completes, when it is revoked. If `CHEESEWAF_SETUP_TOKEN` was set before startup, keep that value out of logs and shell history. The browser reads `setup_token` from the URL fragment, clears it from the address bar, and sends it only in that header.

If you open bare `/setup`, paste the token from the protected file. It remains in page memory and is cleared after submission. Never put the token in a query parameter or include it in tickets, screenshots, or logs.

### 2. Create Root Administrator Account

Follow the on-screen steps:
1. Enter a username that follows the canonical username rule above.
2. Enter a password of at least 10 characters that satisfies at least 3 of the 4 password classes and does not contain the username.
3. Review the summary. It shows the username, that the password is set, the environment check, and selected integrations; it does not display the password, a password hash, a system master key, or an administrator credential digest.

### 3. Configure Admin Network Boundaries

- In standalone production environments, keep `server.admin_listen` bound to the loopback interface (`127.0.0.1:9443`).
- If public access is required, ensure `server.admin_tls` is enabled with a valid certificate and restrict ingress using IP allowlists.

{{% /steps %}}

Upon completing initialization, navigating to the admin endpoint redirects to the Web Console login view. Local credentials can subsequently be managed using `waf-cli` or `cheesewaf user`.

{{% pageinfo color="info" %}}
The generated configuration may contain an `update.ota.server` value, but OTA is disabled by default and the current binary has no updater worker. It cannot download or install rules or binaries through OTA; keep `update.ota.enabled: false`.
{{% /pageinfo %}}
