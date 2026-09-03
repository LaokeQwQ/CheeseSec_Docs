---
title: Command-Line Interface & Interactive TUI
linkTitle: CLI & TUI
weight: 150
description: Unified single-binary CLI distribution for cheesewaf and waf-cli, global flags, subcommand reference, and terminal UI operations.
---

CheeseWAF utilizes a unified single-binary (BusyBox pattern) architecture. The execution mode is determined automatically based on the invocation command name:

| Executable Name | Default Execution Behavior |
| --- | --- |
| `cheesewaf` | Executes the `serve` command by default, launching both Data Plane reverse proxy and Control Plane management services |
| `waf-cli` | Launches the interactive Terminal User Interface (TUI, equivalent to `panel`) |

## Global Command-Line Flags {#global-flags}

```text
-c, --config string     Path to configuration file (default ./data/config/cheesewaf.yaml)
    --data-dir string   Path to runtime data directory (default ./data)
    --lang string       UI language preference (en or zh-CN)
```

The language resolution hierarchy is: CLI `--lang` flag > Environment variable `CHEESEWAF_LANG` > Saved setting in data directory > Host operating system locale.

## Subcommand Reference Table {#commands}

| Subcommand | Functionality & Description |
| --- | --- |
| `serve` | Launches the full WAF daemon (Data Plane reverse proxy + Control Plane API and Web console) |
| `setup` | Interactive or headless terminal initialization wizard for hardware profiling and initial credentials |
| `rules` | Batch imports, exports, and template generation for site custom regex rules |
| `panel` | Launches the interactive TUI terminal management panel |
| `status` | Checks daemon health, process PID lease, and runtime status |
| `healthcheck` | Diagnostic probes for admin API and outbound TLS (used in Docker healthcheck probes) |
| `stop` | Gracefully terminates the running local daemon process |
| `restart` | Gracefully stops and restarts the local daemon |
| `user` | Resets local admin credentials, renames users, and manages 2FA credentials |
| `cluster` | Cluster controller init, worker node join, certificate rotation, token management, and runtime operations |
| `logs` | Packages service logs into a compressed ZIP support bundle (`logs pack`) |
| `lang` | Displays or persistently configures the default CLI interface language (`lang show` / `lang set`) |
| `version` | Displays software version, build Git commit, release channel, and build timestamp |

## Subcommand Details & Examples {#subcommands-detail}

### 1. System Setup Wizard (`setup`) {#cmd-setup}

Supports both interactive prompts and non-interactive scripted automation:

```bash
# Interactive setup wizard with hardware probing and password configuration
cheesewaf setup

# Headless unattended installation
cheesewaf setup --yes \
  --username admin \
  --password-stdin < /path/to/password.txt \
  --profile balanced \
  --admin-listen 127.0.0.1:9443 \
  --skip-probe
```

Key flags:
- `-y, --yes`: Skip all confirmation prompts and commit changes directly.
- `--username` / `--password-stdin`: Initial root administrator username and password from standard input.
- `--profile`: Hardware profile tuning (`minimal`, `balanced`, or `performance`).
- `--admin-listen`: Admin management API listen address (default `127.0.0.1:9443`).
- `--skip-probe` / `--skip-external`: Skip hardware autodetection or skip external telemetry (GeoIP/Prometheus/VictoriaLogs) setup.

### 2. Custom Rules Management (`rules`) {#cmd-rules}

Batch replaces or exports site `custom_rules` via YAML or JSON. On successful import, it automatically notifies the running daemon to perform a zero-downtime hot reload:

```bash
# Output official custom rules template
cheesewaf rules example --format yaml --file rules-template.yaml

# Validate and import custom rules for a target site
cheesewaf rules import --site site-demo --file my-rules.yaml

# Export custom rules of a site to JSON
cheesewaf rules export --site site-demo --format json --file exported-rules.json
```

### 3. Local User Administration (`user`) {#cmd-user}

```bash
# Reset password for a local user interactively
cheesewaf user password admin

# Generate a strong temporary password and disable TOTP 2FA (emergency recovery)
cheesewaf user password admin --generate --reset-2fa

# Ensure an administrator account exists (creates or updates credentials)
cheesewaf user ensure-admin admin --password-stdin < secret.txt

# Rename an existing user
cheesewaf user rename old_admin new_admin
```

### 4. Cluster Management (`cluster`) {#cmd-cluster}

```bash
# Initialize current node as cluster controller and mint cluster CA
cheesewaf cluster init

# Create a temporary worker join token (default TTL: 15 minutes)
cheesewaf cluster token create --ttl 15m

# List or revoke join tokens
cheesewaf cluster token list
cheesewaf cluster token revoke <token_id>

# Join a worker node into the cluster
cheesewaf cluster join \
  --controller https://10.0.0.1:9444 \
  --token <join_token> \
  --node-id node-worker-02 \
  --advertise-addr 10.0.0.2:9444 \
  --ca-cert /path/to/cluster-ca.crt

# Rotate cluster mTLS communication certificates online
cheesewaf cluster cert rotate

# Inspect cluster health and consensus status
cheesewaf cluster status
```

### 5. Support Bundle Packaging (`logs`) {#cmd-logs}

```bash
# Package all runtime logs into a timestamped support ZIP archive
cheesewaf logs pack

# Specify target archive output path
cheesewaf logs pack --dir /tmp --name support-bundle.zip
```

### 6. CLI Language Configuration (`lang`) {#cmd-lang}

```bash
# Show current locale and supported language list
cheesewaf lang show

# Persistently set default language
cheesewaf lang set en
cheesewaf lang set zh-CN
```

## Operational Examples {#examples}

```bash
# Launch with custom configuration and data paths
cheesewaf serve --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf

# Check process execution status and PID lease
cheesewaf status

# Launch the interactive terminal UI
waf-cli

# Run container diagnostics and readiness check
cheesewaf healthcheck
```

{{% pageinfo color="info" %}}
On Windows systems, if you wish to run `waf-cli` directly by name, copy or create an alias from `cheesewaf.exe` to `waf-cli.exe`.
{{% /pageinfo %}}
