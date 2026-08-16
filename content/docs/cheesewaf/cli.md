---
title: Command-Line Interface & Interactive TUI
linkTitle: CLI & TUI
weight: 150
description: Unified single-binary CLI distribution for cheesewaf and waf-cli, global flags, subcommand reference, and terminal UI operations.
---

CheeseWAF utilizes a unified single-binary architecture. The execution mode is determined automatically based on the invocation command name:

| Executable Name | Default Execution Behavior |
| --- | --- |
| `cheesewaf` | Executes the `serve` command by default, launching both Data Plane and Control Plane listeners |
| `waf-cli` | Launches the interactive Terminal User Interface (TUI, equivalent to `panel`) |

## Global Command-Line Flags {#global-flags}

```text
-c, --config string     Path to configuration file (default ./data/cheesewaf.yaml)
    --data-dir string   Path to runtime data directory (default ./data)
    --lang string       UI language preference (en or zh-CN)
```

The language resolution hierarchy is: CLI `--lang` flag > Environment variable `CHEESEWAF_LANG` > Saved setting in data directory > Host operating system locale.

## Subcommand Reference Table {#commands}

| Subcommand | Functionality & Description |
| --- | --- |
| `serve` | Launches the full WAF daemon (Data Plane reverse proxy + Control Plane API and Web console) |
| `panel` | Launches the interactive TUI terminal management panel |
| `status` | Checks daemon health and outputs process PID and memory usage |
| `healthcheck` | Executes local diagnostic probes (exits non-zero on failure; used in container healthchecks) |
| `stop` | Gracefully terminates the running local daemon process |
| `restart` | Gracefully stops and restarts the local daemon |
| `user` | Manages local administrator user accounts, passwords, and 2FA credentials |
| `cluster` | Manages cluster node joining, mTLS certificates, and runtime node operations |
| `version` | Displays software version, build Git commit, release channel, and build timestamp |
| `lang` | Configures and persists the default CLI interface language |
| `logs` | Streams live logs or archives logs into a compressed bundle |

## Operational Examples {#examples}

```bash
# Launch with custom configuration and data paths
cheesewaf serve --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf

# Check process execution status
cheesewaf status

# Launch the interactive terminal UI
waf-cli

# Manage users and cluster nodes
cheesewaf user list
cheesewaf cluster status
```

{{% pageinfo color="info" %}}
On Windows systems, if you wish to run `waf-cli` directly by name, copy or create an alias from `cheesewaf.exe` to `waf-cli.exe`.
{{% /pageinfo %}}
