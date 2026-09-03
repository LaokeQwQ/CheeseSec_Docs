---
title: Windows Deployment
linkTitle: Windows
weight: 30
description: "Three Windows deployment modes: Single-file CLI, Portable Zip archive, and NSIS graphical installer, plus native Windows Service integration and local controller usage."
---

CheeseWAF offers three distribution options for Windows, each utilizing the identical core engine and protection capabilities:

## 1. Single-File CLI & Native Windows Service {#cli}

Designed for rapid testing, automated scripts, or native Windows Service hosting:

```powershell
# Start WAF forwarder and management plane interactively
.\cheesewaf.exe serve --config .\configs\cheesewaf.yaml --data-dir .\data

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

1. Extract `cheesewaf-*-windows-amd64.zip` to your target directory (e.g., `D:\CheeseWAF`).
2. Run terminal setup and start the server:

```powershell
# Run the interactive setup wizard on first launch
.\cheesewaf.exe setup

# Launch the WAF daemon
.\cheesewaf.exe serve --config .\configs\cheesewaf.yaml --data-dir .\data
```

## 3. NSIS Graphical Installer (Recommended) {#nsis}

Ideal for workstation or production servers requiring guided installation and automated service registration:

1. Run the `CheeseWAF-*-windows-*-setup.exe` installer.
2. Follow the wizard prompts. The installer can automatically register CheeseWAF as an autostarting Windows background service.
3. Upon uninstallation, the `data\` directory containing your databases and certificates is retained by default to prevent accidental data loss.

## Local Helper Controller (GUI) {#gui}

`cheesewaf-gui` is a desktop tray assistant for managing the lifecycle of the underlying service:

- **Network Security**: Strictly binds only to the local loopback address `127.0.0.1:17943`.
- **Key Features**: System tray status icon, one-click service start/stop, direct access to the Web Console, and quick shortcuts to configuration directories.
- **Autostart**: Supports registering an autostart entry under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.

```powershell
.\cheesewaf-gui.exe --config .\configs\cheesewaf.yaml --data-dir .\data
```

Once started, open `http://127.0.0.1:17943/` in your browser to view the local desktop controller dashboard.
