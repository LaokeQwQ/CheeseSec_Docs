---
title: Install
linkTitle: Install
weight: 20
description: Choose a CheeseWAF package for Linux, Docker, Windows, or macOS.
---

Pick one install path. Do not mix an NSIS install with a hand-copied Linux tree on the same host unless you know which process owns the ports.

{{< nav-cards cols="2" >}}
{{< nav-card title="Linux" link="/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="systemd unit, system user, /etc/cheesewaf." />}}
{{< nav-card title="Docker" link="/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="Compose, read-only root, non-root UID 10001." />}}
{{< nav-card title="Windows" link="/docs/cheesewaf/install/windows/" icon="fa-brands fa-windows" desc="Single exe, zip, or NSIS. Local controller on loopback." />}}
{{< nav-card title="macOS" link="/docs/cheesewaf/install/macos/" icon="fa-brands fa-apple" desc="DMG app or tar.gz CLI." />}}
{{< /nav-cards >}}

## Release files {#release-files}

Download **Alpha** pre-releases, or take the same files from Actions artifacts.

| File | Platform |
| --- | --- |
| `cheesewaf-*-linux-amd64.tar.gz` | Linux x86_64 |
| `cheesewaf-*-linux-arm64.tar.gz` | Linux ARM64 |
| `cheesewaf-*-linux-loong64.tar.gz` | Linux LoongArch |
| `cheesewaf-*-darwin-amd64.tar.gz` / `.dmg` | macOS Intel |
| `cheesewaf-*-darwin-arm64.tar.gz` / `.dmg` | macOS Apple Silicon |
| `cheesewaf-*-windows-amd64.exe` | Windows x86_64 CLI |
| `cheesewaf-*-windows-arm64.exe` | Windows ARM64 CLI |
| `cheesewaf-*-windows-amd64.zip` | Windows x86_64 portable tree |
| `cheesewaf-*-windows-arm64.zip` | Windows ARM64 portable tree |
| `CheeseWAF-*-windows-*-setup.exe` | Windows NSIS installer |

After install, continue with [Quick start](../tutorial/).
