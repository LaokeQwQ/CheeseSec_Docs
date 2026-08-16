---
title: CLI and TUI
linkTitle: CLI
weight: 150
description: cheesewaf and waf-cli share one binary. Default commands depend on the executable name.
---

The same binary answers to two names.

| Invoked as | Default command |
| --- | --- |
| `cheesewaf` | `serve` |
| `waf-cli` | interactive TUI (`panel`) |

Global flags:

```text
-c, --config     path to cheesewaf.yaml (default ./data/cheesewaf.yaml)
    --data-dir   runtime data directory (default ./data)
    --lang       en or zh-CN
```

Language order: flag, then environment, then data-dir, then the OS locale.

## Commands {#commands}

| Command | Purpose |
| --- | --- |
| `serve` | Start the WAF |
| `panel` | TUI |
| `status` | Is the process up |
| `healthcheck` | Exit non-zero when unhealthy (Compose uses this) |
| `stop` | Stop a running process |
| `restart` | Stop then serve |
| `user` | Manage local users |
| `cluster` | Join, certs, runtime |
| `version` | Version, channel, build time |
| `lang` | Persist CLI language |
| `logs` | Pack or inspect logs |

Examples:

```bash
cheesewaf serve --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf
cheesewaf status
waf-cli
cheesewaf user
cheesewaf cluster
```

On Windows, copy `cheesewaf.exe` to `waf-cli.exe` if you want the TUI name.
The desktop controller is a **separate** binary: [Windows install](../install/windows/#gui).
