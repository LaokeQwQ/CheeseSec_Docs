---
title: macOS Deployment
linkTitle: macOS
weight: 40
description: Install CheeseWAF via DMG desktop image or run from a standalone command-line archive.
---

On macOS, CheeseWAF can be deployed either as a desktop application with a status bar controller or as a standalone terminal daemon:

## 1. DMG Desktop Installer {#dmg}

Ideal for local testing and workstation environments:

1. Download the disk image for your processor architecture: `cheesewaf-*-darwin-arm64.dmg` for Apple Silicon (M-series) or `cheesewaf-*-darwin-amd64.dmg` for Intel-based Macs.
2. Double-click the DMG image and drag **CheeseWAF** into the **Applications** folder.
3. Launch CheeseWAF from Launchpad or Applications.

Upon startup, the application runs the local controller in the menu bar, enabling one-click service start/stop, status inspection, and direct access to the Web console. Runtime configuration and data are stored under `~/Library/Application Support/CheeseWAF`.

## 2. Command-Line Archive (tar.gz) {#tarball}

Ideal for automated workflows or headless macOS instances:

```bash
# Unpack the archive matching your architecture
tar -xzf cheesewaf-*-darwin-arm64.tar.gz
cd cheesewaf-*

# Launch the daemon
./cheesewaf serve --config ./configs/cheesewaf.yaml --data-dir ./data
```

Once running, navigate to `http://127.0.0.1:9443/setup` in your browser to complete the initialization wizard.
