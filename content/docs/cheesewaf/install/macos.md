---
title: macOS Deployment
linkTitle: macOS
weight: 40
description: Install CheeseWAF on macOS via graphical DMG package or lightweight tar.gz command-line archive.
---

CheeseWAF supports two primary deployment mechanisms on macOS:

## 1. DMG Graphical Installer {#dmg}

Ideal for local testing, development, and desktop workstations:

1. Download the DMG matching your CPU architecture: `cheesewaf-arm64-darwin-*.dmg` for Apple Silicon (M-series), or `cheesewaf-amd64-darwin-*.dmg` for Intel Macs.
2. Open the DMG image and drag **CheeseWAF** into your **Applications** folder.
3. Launch CheeseWAF from Launchpad or Spotlight.

{{% pageinfo color="info" %}}
**Gatekeeper Guidance**: Official releases are signed and notarized by Apple. If running an ad-hoc developer build that triggers macOS security prompts, Control-click the app icon, select "Open", and confirm the prompt.
{{% /pageinfo %}}

Upon launching, the DMG application runs a lightweight browser-based local controller bound to loopback at `http://127.0.0.1:17943/`. It provides process start/stop/restart controls, status monitoring, and shortcuts to the Web Console and configuration directory. Default runtime data is saved under `~/Library/Application Support/CheeseWAF`.

## 2. Command-Line Archive (tar.gz) {#tarball}

Ideal for headless servers, developer terminal workflows, or automated scripts:

```bash
# Extract the archive
tar -xzf cheesewaf-arm64-darwin-*.tar.gz
cd cheesewaf-*

# Run terminal setup wizard
./cheesewaf setup

# Launch the WAF daemon
./cheesewaf serve --config ./data/config/cheesewaf.yaml --data-dir ./data
```

Once initialized, navigate to `http://127.0.0.1:9443/` to log into the Web Console.
