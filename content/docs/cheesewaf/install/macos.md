---
title: macOS
linkTitle: macOS
weight: 40
description: Install CheeseWAF from a DMG, or run the tar.gz CLI.
---

## DMG {#dmg}

1. Download `cheesewaf-*-darwin-arm64.dmg` (Apple Silicon) or `cheesewaf-*-darwin-amd64.dmg` (Intel).
2. Open the image and drag **CheeseWAF** into **Applications**.
3. Launch CheeseWAF from Launchpad or Applications.

The app starts the local controller.
Use it to start, stop, and open the Web console.

Runtime data is under `~/Library/Application Support/CheeseWAF`.

## CLI tarball {#tarball}

If you only want the command line:

```bash
tar -xzf cheesewaf-*-darwin-arm64.tar.gz
cd cheesewaf-*
./cheesewaf serve --config ./configs/cheesewaf.yaml --data-dir ./data
```

Then open `http://127.0.0.1:9443/setup`.
