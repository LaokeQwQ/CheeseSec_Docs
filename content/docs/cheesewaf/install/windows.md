---
title: Windows Deployment
linkTitle: Windows
weight: 30
description: "Three deployment options on Windows: Single-file CLI, Portable Zip archive, and NSIS graphical installer with local helper controller."
---

CheeseWAF offers three distribution formats on Windows, all sharing the identical core engine, security capabilities, and feature set:

## 1. Single-File CLI Mode {#cli}

Ideal for automated scripts, CI runners, or lightweight environments:

1. Download the standalone executable matching your architecture (e.g., `cheesewaf-*-windows-amd64.exe`).
2. Execute the following commands in PowerShell or Command Prompt:

```powershell
# Start WAF data and management planes
.\cheesewaf-*-windows-amd64.exe serve --config .\cheesewaf.yaml --data-dir .\data

# Query daemon execution status
.\cheesewaf-*-windows-amd64.exe status

# Terminate the running instance
.\cheesewaf-*-windows-amd64.exe stop
```

## 2. Portable Zip Archive {#zip}

Contains pre-bundled configuration templates and static assets:

1. Extract `cheesewaf-*-windows-amd64.zip` to your target directory (e.g., `D:\CheeseWAF`).
2. Run the executable from within that directory:

```powershell
.\cheesewaf.exe serve --config .\configs\cheesewaf.yaml --data-dir .\data
```

## 3. NSIS Graphical Installer (Recommended) {#nsis}

Provides an intuitive installation wizard, desktop shortcuts, and Windows Service registration:

1. Launch the `CheeseWAF-*-windows-*-setup.exe` installer.
2. Follow the setup wizard to select the target installation directory. The installer can automatically register CheeseWAF as a Windows background service (`CheeseWAF`).
3. During uninstallation, user data and databases in `data\` are preserved by default.

## Local Helper Controller (GUI) {#gui}

`cheesewaf-gui` is a lightweight desktop utility designed to manage the daemon lifecycle on workstation environments:

- **Strict Network Boundary**: Binds strictly to the local loopback address `127.0.0.1:17943`.
- **Core Functionality**: Displays current process PID and health status, toggles service start/stop, opens the Web management console, and provides direct access to configuration directories.
- **Autostart**: Supports registering an autostart entry for the current user (`HKCU\Run`).

```powershell
.\cheesewaf-gui.exe --config .\configs\cheesewaf.yaml --data-dir .\data
```

Once running, navigate to `http://127.0.0.1:17943/` in your browser to access the controller interface.
