---
title: Windows Deployment
linkTitle: Windows
weight: 30
description: "Three Windows deployment modes: Single-file CLI, Portable Zip archive, and NSIS graphical installer, plus native Windows Service integration and a loopback-only local controller."
---

CheeseWAF offers three distribution options for Windows, each utilizing the identical core engine and protection capabilities:

## 1. Single-File CLI & Native Windows Service {#cli}

Designed for rapid testing, automated scripts, or native Windows Service hosting:

```powershell
# Start WAF forwarder and management plane interactively
.\cheesewaf.exe serve --config .\data\config\cheesewaf.yaml --data-dir .\data

# Query running daemon status and PID lease
.\cheesewaf.exe status

# Gracefully terminate the running daemon
.\cheesewaf.exe stop
```

### Native Windows Service Awareness

`cheesewaf serve` includes native Windows Service state machine integration (`golang.org/x/sys/windows/svc`):
- When invoked by the Windows Service Control Manager (SCM), the process automatically identifies service mode, seamlessly handling SCM `Stop` and `Shutdown` signals with zero external service wrappers (like NSSM or WinSW).
- The default service name is `CheeseWAF`.

## 2. Portable Zip Archive {#zip}

The portable package bundles default configuration templates and compiled Web Console assets:

1. Extract `cheesewaf-amd64-windows-*.zip` to your target directory (e.g., `D:\CheeseWAF`).
2. Run terminal setup and start the server:

```powershell
# Run the interactive setup wizard on first launch
.\cheesewaf.exe setup

# Launch the WAF daemon
.\cheesewaf.exe serve --config .\data\config\cheesewaf.yaml --data-dir .\data
```

When first-install setup is pending, the process log shows only the base `/setup` URL, the protected `data\setup.url` path, and an opaque receipt. Read the complete URL from the mode `0600` file within its 10-minute validity period. After setup completes, the token is revoked; expired `setup.url` files are cleaned up.

## 3. NSIS Graphical Installer (Recommended) {#nsis}

Ideal for workstation or production servers requiring guided installation and Windows Service registration:

1. Run the `cheesewaf-amd64-windows-*-setup.exe` installer (use the `arm64` variant on Windows ARM64).
2. Follow the wizard prompts. The installer registers the `CheeseWAF` Windows service in manual (`start= demand`) mode; start or stop it explicitly from the Service Control Manager or with `sc.exe`.
3. Upon uninstallation, the `data\` directory containing your databases and certificates is retained by default to prevent accidental data loss.

## Local Helper Controller (GUI) {#gui}

`cheesewaf-gui` is a lightweight browser-based local controller for managing the lifecycle of the underlying service:

- **Network Security**: Strictly binds only to the local loopback address `127.0.0.1:17943`.
- **Key Features**: Service start/stop/restart, status and PID display, direct access to the Web Console, and a shortcut to the configuration directory.
- **Process Model**: The controller starts the local `cheesewaf serve` process when requested; it is not a second management backend.

```powershell
.\cheesewaf-gui.exe --config .\data\config\cheesewaf.yaml --data-dir .\data
```

Once started, open `http://127.0.0.1:17943/` in your browser to view the local desktop controller dashboard.
