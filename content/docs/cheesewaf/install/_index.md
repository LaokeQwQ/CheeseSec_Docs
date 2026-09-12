---
title: Deployment & Installation
linkTitle: Deployment & Install
weight: 20
description: Comprehensive deployment guides and installation options for CheeseWAF across Linux, Docker, Windows, and macOS.
---

CheeseWAF can be deployed as a system service, containerized workload, or standalone binary across all major platforms. Choose the deployment method that aligns with your infrastructure:

{{< nav-cards cols="2" >}}
{{< nav-card title="Linux" link="/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="Configure a systemd daemon, dedicated unprivileged system user, and /etc/cheesewaf layout." />}}
{{< nav-card title="Docker" link="/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="Deploy with Docker Compose featuring a read-only root filesystem and unprivileged non-root execution." />}}
{{< nav-card title="Windows" link="/docs/cheesewaf/install/windows/" icon="fa-brands fa-windows" desc="Run via single-file CLI, portable Zip archive, or GUI NSIS installer with a local helper controller." />}}
{{< nav-card title="macOS" link="/docs/cheesewaf/install/macos/" icon="fa-brands fa-apple" desc="Install as a desktop DMG application or run via portable tar.gz command-line archive." />}}
{{< /nav-cards >}}

## Release Package Matrix & Distribution Strategy {#release-files}

Beginning with stable releases (v0.3.9+), CheeseWAF enforces a **server-first** distribution model: stable releases prioritize certified Linux server packages accompanied by Sigstore cryptographic signatures and SBOM attestations. Windows and macOS desktop packages are provided as optional operator-side builds.

Pre-compiled production binaries can be downloaded directly from GitHub Releases:

| Release Package | Target Platform & Architecture |
| --- | --- |
| `cheesewaf-amd64-linux-*.tar.gz` | Linux x86_64 architecture |
| `cheesewaf-arm64-linux-*.tar.gz` | Linux ARM64 architecture |
| `cheesewaf-loong64-linux-*.tar.gz` | Linux LoongArch architecture |
| `cheesewaf-amd64-darwin-*.tar.gz` / `.dmg` | macOS Intel architecture |
| `cheesewaf-arm64-darwin-*.tar.gz` / `.dmg` | macOS Apple Silicon architecture |
| `cheesewaf-amd64-windows-*.exe` | Windows x86_64 standalone executable |
| `cheesewaf-arm64-windows-*.exe` | Windows ARM64 standalone executable |
| `cheesewaf-amd64-windows-*.zip` | Windows x86_64 portable ZIP archive |
| `cheesewaf-arm64-windows-*.zip` | Windows ARM64 portable ZIP archive |
| `cheesewaf-amd64-windows-*-setup.exe` | Windows x86_64 NSIS graphical installer |
| `cheesewaf-arm64-windows-*-setup.exe` | Windows ARM64 NSIS graphical installer |

Following installation, proceed to [Quick Start](../tutorial/) to complete system initialization and onboard your first reverse proxy site.
