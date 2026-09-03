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

The wizard inspects host resources (CPU cores, available RAM, and storage mounts) and recommends an optimal runtime profile:

- **`minimal`**: Configured for 1–2 CPU cores and <2GB RAM edge devices or small VMs; minimizes memory buffers.
- **`balanced`**: Tailored for standard 4–8 CPU cores and 4–16GB RAM production servers; balances parsing throughput and connection concurrency.
- **`performance`**: Configured for 16+ core high-throughput servers; allocates full worker pools and aggressive caches.

### 2. Guided Credentials & Transactional Safety

- **Credentials**: Prompts for an administrator username and enforces strict password complexity checks.
- **Optional Telemetry**: Conveniently toggle GeoIP updates, Prometheus `/metrics` exposition, or VictoriaLogs log streaming.
- **Transactional Cleanliness**: All inputs are accumulated in memory. **If you abort at any prompt, nothing is written to disk**, leaving zero partial or corrupt configuration files.

### 3. Headless Scripted Automation

For CI/CD pipelines or cloud-init automation, use non-interactive command-line flags:

```bash
cheesewaf setup --yes \
  --username admin \
  --password-stdin < /etc/cheesewaf/secrets/admin_pass.txt \
  --profile balanced \
  --admin-listen 127.0.0.1:9443 \
  --skip-probe
```

## Option 2: Browser Web Wizard {#web-setup}

{{% steps %}}

### 1. Open the Setup URL

- **Local Machine**: Open `http://127.0.0.1:9443/setup` in your browser.
- **Remote Server or Docker**: Navigate to `https://<server-ip>:9443/setup` (accept the self-signed TLS certificate prompt on first visit).

### 2. Create Root Administrator Account

Follow the on-screen steps:
1. Provide a strong master password (must contain uppercase, lowercase, numbers, and symbols).
2. Save the displayed system master key and recovery credentials securely.

### 3. Configure Admin Network Boundaries

- In standalone production environments, keep `server.admin_listen` bound to the loopback interface (`127.0.0.1:9443`).
- If public access is required, ensure `server.admin_tls` is enabled with a valid certificate and restrict ingress using IP allowlists.

{{% /steps %}}

Upon completing initialization, navigating to the admin endpoint redirects to the Web Console login view. Local credentials can subsequently be managed using `waf-cli` or `cheesewaf user`.
