---
title: Windows
linkTitle: Windows
weight: 30
description: Single-file CLI, portable zip, or NSIS installer. The GUI controller listens on loopback only.
---

Windows has three shapes. They are not three different WAFs.

## A. Single-file CLI {#cli}

1. Download `cheesewaf-*-windows-amd64.exe` or the `arm64` file.
2. Run:

```powershell
.\cheesewaf-*-windows-amd64.exe serve --config .\cheesewaf.yaml --data-dir .\data
.\cheesewaf-*-windows-amd64.exe status
.\cheesewaf-*-windows-amd64.exe stop
```

The forwarding process does not need the installer.
The Web UI assets live in `web/dist` next to the executable in zip / DMG / tar packages.

## B. Portable zip {#zip}

1. Unpack `cheesewaf-*-windows-amd64.zip` to a directory such as `D:\CheeseWAF`.
2. Run:

```powershell
.\cheesewaf.exe serve --config .\configs\cheesewaf.yaml --data-dir .\data
.\cheesewaf.exe status
.\cheesewaf.exe stop
```

## C. NSIS installer {#nsis}

1. Run `CheeseWAF-*-windows-amd64-setup.exe` or the `arm64` setup.
2. Follow the wizard.
3. Uninstall keeps `data\` by default.

The installer may register a Windows service (`sc.exe create CheeseWAF …`). Treat that as best-effort.

## Local controller {#gui}

`cheesewaf-gui` is **not** a second admin console.
It only starts, stops, and opens the real management UI.

- Bind address: `127.0.0.1:17943`
- Shows PID and running state
- Opens the Web console and the config folder
- Optional current-user autostart (`HKCU\Run`)

```powershell
.\cheesewaf-gui.exe --config .\configs\cheesewaf.yaml --data-dir .\data
```

The browser opens `http://127.0.0.1:17943/`.
