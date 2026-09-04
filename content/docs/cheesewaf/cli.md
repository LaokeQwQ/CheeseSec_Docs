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
| `waf-cli` | Launches the interactive Terminal User Interface (TUI, equivalent to `cli`; `panel` is a compatibility alias) |

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
| `cli` | Launches the interactive TUI terminal management panel (compatibility alias: `panel`) |
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
  --profile smart \
  --admin-listen 127.0.0.1:9443 \
  --skip-probe
```

Key flags:
- `-y, --yes`: Skip interactive confirmation prompts and commit directly (headless setup requires `--password-stdin` to ensure strong credential generation).
- `--username` / `--password-stdin`: Initial root administrator username and password read from standard input.
- `--profile`: Hardware profile tuning (`smart`, `low`, `medium`, `high`, or `custom`; official aliases `minimal`, `balanced`, and `performance` are fully supported).
- `--admin-listen`: Admin management API listen address (default `127.0.0.1:9443`; prints `http://` or `https://` based on `admin_tls`).
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
# Set a local user's password by reading it from stdin (recommended; avoids shell history/process leakage)
cheesewaf user password admin --password-stdin < secret.txt

# Direct --password is less safe because the value can appear in shell history, environment variables, or process arguments
cheesewaf user password admin --password 'replace-with-new-password'

# Generate a strong temporary password and disable TOTP 2FA (emergency recovery)
cheesewaf user password admin --generate --reset-2fa

# Ensure an administrator account exists (creates or updates credentials)
cheesewaf user ensure-admin admin --password-stdin < secret.txt

# Rename an existing user
cheesewaf user rename old_admin new_admin
```

### 4. Cluster Management (`cluster`) {#cmd-cluster}

```bash
# Initialize current node as a single-node cluster (does not mint a CA)
cheesewaf cluster init

# Create a temporary worker join token (default TTL: 15 minutes)
cheesewaf cluster token create --ttl 15m

# List or revoke join tokens
cheesewaf cluster token list
export CHEESEWAF_TOKEN_ID='token-id-to-revoke'
cheesewaf cluster token revoke "$CHEESEWAF_TOKEN_ID"

export CHEESEWAF_CONTROLLER='https://10.0.0.1:9443'
export CHEESEWAF_JOIN_TOKEN='one-time-join-token'
export CHEESEWAF_NODE_ID='node-worker-02'
export CHEESEWAF_ADVERTISE_ADDR='10.0.0.2:9444'
export CHEESEWAF_CONTROLLER_CA='/etc/cheesewaf/certs/admin-ca.crt'

# Join a worker node using a one-time token; the CLI creates the local key and CSR
cheesewaf cluster join \
  --controller "$CHEESEWAF_CONTROLLER" \
  --token "$CHEESEWAF_JOIN_TOKEN" \
  --node-id "$CHEESEWAF_NODE_ID" \
  --advertise-addr "$CHEESEWAF_ADVERTISE_ADDR" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA" # --ca-cert is also accepted

export CHEESEWAF_API_TOKEN='management-token-with-write-cluster'

# Request replacement cluster mTLS files (requires existing local certificate paths; reload/restart afterward)
cheesewaf cluster cert rotate \
  --controller "$CHEESEWAF_CONTROLLER" \
  --ca-file "$CHEESEWAF_CONTROLLER_CA" \
  --api-token-env CHEESEWAF_API_TOKEN

# Inspect cluster health and consensus status
cheesewaf cluster status

# Export declarative cluster objects (redirect the YAML output to a file)
cheesewaf cluster export > cluster-export.yaml

# Run the local node heartbeat loop toward the HTTPS interconnect (mTLS) controller
export CHEESEWAF_INTERCONNECT_CONTROLLER='https://10.0.0.1:9444'
cheesewaf cluster monitor-node --controller "$CHEESEWAF_INTERCONNECT_CONTROLLER" --interval 10s
```

`--ca-file` for `cluster join` and `cert rotate` verifies the controller's **9443 HTTPS management endpoint**; it is not the cluster CA returned during enrollment. Omit it only when the controller certificate chains to the system trust store; pre-provision a private admin CA when needed. Joining generates a local key/CSR and writes the returned cluster CA and certificate under the node data directory. Certificate rotation requires exactly one token source (`--api-token`, `--api-token-file`, or `--api-token-env`), writes files locally, and takes effect after the service reload/restart procedure.

`cluster monitor-node` posts heartbeats to the cluster **interconnect** (normally HTTPS `:9444`) using the local configured cluster CA/certificate/key. A custom `--controller` value must likewise be an HTTPS interconnect address; `--insecure-skip-verify` is for isolated laboratory testing only.

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

The TUI subcommand's canonical spelling is `cheesewaf cli`; `cheesewaf panel` remains available as a compatibility alias.

`cheesewaf user` also accepts the `users` alias. `cheesewaf healthcheck` is intentionally hidden from normal `--help` output and is used by service/container probes.
{{% /pageinfo %}}
