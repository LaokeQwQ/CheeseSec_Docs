---
title: Quick Start Guide
linkTitle: Quick Start
weight: 30
description: Install, initialize, verify, and protect one test site before moving to production.
---

This is the single-node path. It follows the same order as the product workflow: **Install → Setup → Verify → Onboard**.

## Short version {#short-version}

1. Run the official one-line Linux installer, or install the verified release archive when the host has no outbound access.
2. Open the HTTPS setup URL printed by the installer and create the first administrator.
3. Confirm that the service and readiness check are healthy.
4. Add a test site and send a request through the data-plane listener.

The Web Console and deterministic data-plane protection work without an LLM. Configure ALAP only after the basic request path is healthy.

## Step 1: Install {#install}

On a Linux host with `sudo`, run:

```bash
curl --proto '=https' --proto-redir '=https' -fsSL https://cheesesec.com/install.sh | sudo bash
```

The installer asks for a language and an optional application install root, downloads and verifies the latest stable release from the official source first, starts the systemd service when available, and prints the setup URLs. GitHub is used only when an official download fails; a checksum or signature verification failure stops installation. If the bootstrap script itself cannot be downloaded, use the [GitHub backup entry](../install/linux/#github-fallback). All downloads and redirects must use HTTPS. Enter `/opt/cheesewaf` to keep the binary, Web assets, configuration, data, and logs together, or press Enter for the standard FHS layout. Set `CHEESEWAF_RELEASE=vX.Y.Z[-beta]` when you need a specific release.

Keep the complete setup URL private. Its URL fragment contains a one-time token that the browser converts to the `X-CheeseWAF-Setup-Token` header; it is revoked after setup. If the server has no outbound access, download the matching release archive and checksum files on a connected machine and follow the offline section of the [Linux installation guide](../install/linux/#offline). For Docker, use the [Docker guide](../install/docker/).

## Step 2: Setup {#setup}

Open the `https://` URL printed by the installer. The setup route always uses the fixed `/setup` path:

```text
https://PUBLIC_IP:9443/setup#setup_token=ONE_TIME_TOKEN
```

Create the initial administrator and keep the management port restricted to trusted administration networks. The [System Initialization](setup/) page covers credential rules, setup-token handling, and the explicit requirements for public management access. If the URL is lost before an administrator exists, reset the token on the host:

```bash
sudo -u cheesewaf /usr/local/bin/cheesewaf \
  --config /etc/cheesewaf/cheesewaf.yaml \
  --data-dir /var/lib/cheesewaf \
  setup token reset --show
```

## Step 3: Verify {#verify}

Run the service and readiness checks from the [Linux installation guide](../install/linux/#verify). The expected state is:

```text
systemd: enabled and active
management: https://127.0.0.1:9443 ready
data plane: 127.0.0.1:8080 available for a test site
```

If a check fails, use the symptom table in [Linux Troubleshooting](../install/linux/#troubleshooting) before changing configuration.

## Step 4: Onboard {#onboard}

{{< nav-cards cols="2" >}}
{{< nav-card title="First Site" link="/docs/cheesewaf/tutorial/first-site/" icon="fa-solid fa-globe" desc="Configure the public domain, upstream origin, baseline policy, and a safe test request." />}}
{{< nav-card title="Connect Models" link="/docs/cheesewaf/tutorial/connect-llm/" icon="fa-solid fa-brain" desc="Optionally connect an OpenAI- or Anthropic-compatible API for asynchronous review." />}}
{{< /nav-cards >}}

Do not point production DNS at the WAF until the origin, health checks, access policy, logging, and rollback path have been tested.

{{% pageinfo color="info" %}}
CheeseWAF's Data Plane provides deterministic AST semantic protection immediately after startup, even without an LLM connected. Before configuring the `ai` block, the ALAP review queue simply remains idle.
{{% /pageinfo %}}

## Next steps {#next-steps}

- Read [Core Concepts](../concepts/) to understand data-plane and management-plane boundaries.
- Configure [Security Policies](../protection/) for ACLs, IP controls, challenges, and rate limits.
- Read [Operations](../operations/) before enabling public management, external storage, backups, or upgrades.
