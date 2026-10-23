---
title: Deployment & Installation
linkTitle: Deployment & Install
weight: 20
description: Choose a CheeseWAF deployment path, prepare the host, and verify the first running service.
---

Use this page to choose a deployment path. For a fresh Linux server, start with the one-line installer or the verified release archive; systemd remains the path used by the quick start.

{{< nav-cards cols="2" >}}
{{< nav-card title="Linux (recommended)" link="/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="One-line installer or verified archive, a shared application root or FHS layout, and a systemd service." />}}
{{< nav-card title="Docker" link="/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="Compose deployment for evaluation or environments already managed by Docker." />}}
{{< nav-card title="Windows" link="/docs/cheesewaf/install/windows/" icon="fa-brands fa-windows" desc="CLI, portable archive, or NSIS desktop installation with a local controller." />}}
{{< nav-card title="macOS" link="/docs/cheesewaf/install/macos/" icon="fa-brands fa-apple" desc="DMG desktop application or portable command-line archive." />}}
{{< /nav-cards >}}

## Prepare {#prepare}

| Item | Minimum or default | Why it matters |
| --- | --- | --- |
| Operating system | Supported 64-bit Linux for the recommended path | The release archive and systemd installer target Linux hosts. |
| CPU and memory | 1–2 cores and 2 GB RAM can run the lightweight profile | The setup wizard recommends a conservative profile on small hosts. |
| Disk | Space for the archive, Web assets, runtime data, and logs | Keep runtime data outside the source/template directory. |
| Privilege | `root` or an administrator with `sudo` | The installer creates the `cheesewaf` service account and systemd unit. |
| Network | Administration path to `9443`; data-plane path to `8080` | Keep management and business traffic on separate access policies. |
| Browser | A browser that can reach the management listener | Required for the Web setup wizard and Console. |
| Release integrity | Matching archive and `SHA256SUMS` from the official source, with GitHub as the backup download source | Verify before extracting or running the binary; stop on checksum or signature errors. |

The one-line installer enables HTTPS and binds the management listener on all interfaces, then gates first setup with a one-time token and a generated security entry. Restrict `9443` to trusted administration networks before exposing it. The shipped configuration template and the setup wizard default to `0.0.0.0:9443` with `server.admin_public: true`; a configuration that omits the `server` keys falls back to the loader default `127.0.0.1:9443`. A public listener still requires management TLS, a valid certificate, and a restricted source network.

On small hosts, use the lightweight profile: the setup wizard recommends `low` when the host has at most 2 logical cores or 2 GB RAM; a probe timeout, cancellation, or failure also falls back to `low`. `storage.profile: production` refuses to start until the production wiring is complete and does not silently fall back to SQLite.

## Choose an installation mode {#modes}

- **Setup / single node:** the one-line installer, a verified archive with systemd, or Docker. Use this for a first deployment, evaluation, and a small self-hosted service.
- **Deploy / production:** Start from the Linux or Docker guide, then add a trusted certificate, an external access policy, backups, log retention, and a tested upgrade path. See [Operations](../operations/).
- **Offline / air-gapped:** Download the release archive, checksums, and signed resource packages on a connected machine, transfer them through your approved channel, and follow the offline section of the Linux guide.

## Release files {#release-files}

Start with the [official CheeseSec website](https://cheesesec.com/) for release downloads. The [Linux installer](linux/) prefers official release metadata and files, with [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases) as the backup for failed downloads. Checksum or signature verification failures stop installation and must not trigger a source switch. Select the artifact that matches the target platform and architecture:

| Artifact pattern | Target |
| --- | --- |
| `cheesewaf-amd64-linux-*.tar.gz` | Linux x86_64 |
| `cheesewaf-arm64-linux-*.tar.gz` | Linux ARM64 |
| `cheesewaf-loong64-linux-*.tar.gz` | Linux LoongArch |
| `cheesewaf-amd64-darwin-*` / `cheesewaf-arm64-darwin-*` | macOS Intel / Apple Silicon |
| `cheesewaf-*-windows-*` | Windows executable, ZIP, or setup package |

Every Linux archive must include the `cheesewaf` binary, `web/dist`, `configs/`, the systemd unit, and `install-linux.sh`. Stop and download the archive again if one of these items is missing.

## After installation {#after-install}

1. Start the service and confirm the process owns the expected listener.
2. Open the HTTPS setup URL printed by the installer, complete `/setup`, and create the first administrator.
3. Add one test site and send test traffic through the data-plane listener.
4. Keep the management port restricted to trusted administration networks until TLS, access control, backups, and upgrade procedures are verified.

Continue with [Quick Start](../tutorial/).
