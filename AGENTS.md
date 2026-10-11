# CheeseSec documentation constraints

## Product-source boundary

- CheeseWAF documentation must be verified against the current CheeseWAF source, UI, and acceptance flow before publication. Keep the English and Chinese pages aligned.
- Treat `configs/cheesewaf.yaml` as a source template. Runtime examples must copy it into the data directory before running setup, so documentation never instructs users to mutate a tracked template.
- First-install Token instructions must describe the complete Fragment URL and the manual `/setup` fallback. Tokens are sent only in `X-CheeseWAF-Setup-Token`; never document query parameters, cookies, localStorage, screenshots, or logs as Token transport.
- Config keys, ports, CAPTCHA defaults, onboarding behavior, and Docker commands are acceptance-tested facts. Do not preserve stale aliases such as `ai.base_url` or `ai.auto_agree` as if they were active.
- User identity documentation must match `internal/identity/username.go`: 3–32 characters, an ASCII letter first, an ASCII letter or digit last, only ASCII letters, digits, `.`, `_`, and `-`, with every whitespace, control, and invisible character rejected. Do not describe trimming or lowercasing as normalization.
- Document `cheesewaf user repair-username USER_ID NEW_USERNAME --reason '...'` as a repair path only for historical non-canonical usernames. Canonical users must use `user rename`; repair is ID-based, rejects missing or duplicate targets, preserves the account credentials, role, and TOTP state, revokes all unrevoked sessions, and writes an append-only audit record with the current OS user ID, reason, and time in one transaction.
- The SQLite management store currently uses the `temporary` profile. Schema 3 to 4 adds username-repair audit storage and does not rewrite old usernames. Back up before an upgrade; never copy an active WAL database directly. Prefer SQLite online backup, or stop the exact writer for a consistent maintenance copy. An older binary must reject a newer schema; do not recommend editing `PRAGMA user_version` by hand.
- User-ID lookup examples must select only `id` and `quote(username)` in SQLite read-only mode. Never query or print `password_hash` or `two_fa_secret` in documentation examples. The Web setup summary displays that a password is set; it does not display a system master key or administrator credential digest.

## Production dependency boundary

- `@agent-eyes/agent-eyes`, code-inspector, `codex-acp`, and similar editor/Agent tooling are development/test-only. Never add them to published site dependencies, generated assets, examples, or production images.
- Documentation build output is disposable. Do not commit generated Hugo destinations or local acceptance artifacts.

## User-facing agent reference

This file is also the operational source of truth for agents that prepare, install, or troubleshoot CheeseWAF for a user. Keep this section synchronized with the current CheeseWAF release, installer, UI, and acceptance tests. Do not replace a source-verified fact with a preferred future workflow.

### Product capability baseline

- **Data plane:** reverse proxying, request normalization, AST semantic inspection, ACLs, IP and client-fingerprint controls, rate limiting, and bot challenges. This is the synchronous enforcement path.
- **Management plane:** Web Console, REST API, CLI/TUI workflows, setup wizard, RBAC, audit records, and readiness/health endpoints. It is separate from business traffic.
- **ALAP review:** optional asynchronous review of ambiguous samples. It is out of band and must never be documented as a prerequisite for inline blocking or as a synchronous request dependency.
- **Storage:** the default `temporary` profile uses the local runtime store. Production storage must be explicitly configured; the service must fail closed rather than silently falling back to SQLite.
- **Adapters and plugins:** adapterd connects an existing NGINX or Envoy gateway through its authenticated contract. CRP packages are signed offline resources and must be verified before staging or activation.
- **Desktop support:** Windows and macOS may provide a local helper controller on `127.0.0.1:17943`; this is not the public management listener.

The code defaults are `127.0.0.1:8080` for the data plane, `127.0.0.1:9443` for the management plane, and `127.0.0.1:9444` for the optional cluster plane. The shipped `configs/cheesewaf.yaml` template, the setup wizard, and the official Linux installer default to a public HTTPS management listener on `0.0.0.0:9443` with `server.admin_public: true`, gated by a one-time setup token and a generated security entry. Only a configuration that omits the `server` keys falls back to the loader default `127.0.0.1:9443`. A public listener still requires management TLS, a valid certificate, and an explicit network access policy.

### Supported Linux installation flow

The one-line installer lives at the release `latest/download` URL: it reads release metadata, downloads the architecture-matched archive, verifies the single matching `SHA256SUMS` entry, extracts it, and runs the packaged installer. The bootstrap script itself is fetched over HTTPS; pin `CHEESEWAF_RELEASE` or use the offline archive when the script itself must be verified before execution. The packaged installer still expects `cheesewaf`, `web/dist`, `configs/`, `systemd/`, and `install-linux.sh` in its working directory and does not download a release by itself.

Documented install paths:

1. **One-line:** `curl -fsSL https://github.com/LaokeQwQ/CheeseWAF/releases/latest/download/install-linux.sh | sudo bash`. It asks for language, install root, and a security-entry value on `/dev/tty`, then installs and starts the service.
2. **Offline or verified archive:** download the archive and `SHA256SUMS` from the same release, run `sha256sum --check SHA256SUMS --ignore-missing`, extract the complete archive, and run `sudo ./install-linux.sh` from the package root.

The installer defaults to `/usr/local/bin/cheesewaf`, `/usr/share/cheesewaf/web`, `/etc/cheesewaf`, `/var/lib/cheesewaf`, `/var/log/cheesewaf`, and `/etc/systemd/system`. `CHEESEWAF_INSTALL_DIR` derives a shared application root (`bin`, `web`, `config`, `data`, `logs`); `CHEESEWAF_PREFIX`, `CHEESEWAF_WEB_DIR`, `CHEESEWAF_CONFIG_DIR`, `CHEESEWAF_DATA_DIR`, `CHEESEWAF_LOG_DIR`, and `CHEESEWAF_UNIT_DIR` override individual paths. Install roots must be absolute dedicated directories with only ASCII letters, digits, `.`, `_`, or `-` in each path segment.

For a fresh configuration the installer writes `server.admin_listen`, enables `server.admin_public` and management TLS, and generates the security-entry path. The service generates and persists the one-time setup token when it first starts. It creates the `cheesewaf` non-login system user, copies the Web assets, copies the configuration template only when the runtime file does not exist, and preserves an existing configuration on re-run (upgrade). Runtime state must remain outside the Git checkout.

Setup uses `https://PUBLIC_IP:9443/setup#setup_token=...`; the token travels only in `X-CheeseWAF-Setup-Token` and is revoked after the first successful setup. The root-only receipt is `<config-dir>/install-secrets.txt`; while setup is pending, the protected `setup.url` file also exists in the data directory. Use `sudo -u cheesewaf /usr/local/bin/cheesewaf --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf setup token reset --show` when the URL is lost before an administrator exists; adjust the paths for a custom install root. Without `--show`, the command writes the new URL to the protected `setup.url` file under the data directory.

### Quick-start acceptance path

Every quick-start or onboarding page should lead the user through this order:

1. **Install:** run the one-line installer, or verify the release archive and run the packaged installer.
2. **Setup:** initialize the management plane and create the first administrator.
3. **Verify:** check `systemctl is-active cheesewaf`, `ss -ltnp | grep ':9443'`, and `curl -kfsS https://127.0.0.1:9443/health/ready` (the installer enables a self-signed certificate by default).
4. **Onboard:** create one test site, verify the upstream from the WAF host, and send a test request through `127.0.0.1:8080`.
5. **Operate:** configure access boundaries, backups, logs, certificates, and rollback before production DNS.

Use short command-first sections named `Summary`, `Prepare`, `Install`, `Configure / Setup`, `Verify`, `Next steps`, and `Troubleshooting`. Keep the English and Chinese pages structurally parallel. Each command block should state the expected result and the next action.

### FAQ and troubleshooting baseline

- **The installer says `cheesewaf binary not found`:** the script is not running from the extracted package root. Re-extract the complete archive and run it there.
- **The installer says `web/dist/index.html missing`:** the download is incomplete or only the binary was extracted. Download the full release archive again.
- **Checksum verification fails:** delete the archive and obtain both the archive and `SHA256SUMS` from the same GitHub Release. Never continue with a mismatch.
- **The service exits on startup:** inspect `sudo journalctl -u cheesewaf -b --no-pager`; fix the first configuration validation error and confirm the service points to the runtime copy, not `configs/cheesewaf.yaml` in the source tree.
- **A remote browser cannot reach `9443`:** the one-line installer binds `0.0.0.0:9443` with TLS and public admin enabled, so check the firewall or security group, the listener, and `CHEESEWAF_ADMIN_PUBLIC_HOST`. The shipped template and setup wizard already enable a public HTTPS listener; a configuration that omits the `server` keys falls back to loopback. Use an SSH tunnel for a loopback listener, or document the complete TLS, `server.admin_public`, firewall, certificate, and access-control change before exposing the management plane publicly.
- **The setup page is missing or the setup URL has expired:** read the root-only `install-secrets.txt` receipt in the configuration directory, or the protected `setup.url` in the data directory while setup is pending, or reset with `sudo -u cheesewaf /usr/local/bin/cheesewaf --config /etc/cheesewaf/cheesewaf.yaml --data-dir /var/lib/cheesewaf setup token reset --show`. The setup token itself has no timer; it is revoked on setup completion or reset. Never put setup tokens in query parameters, logs, screenshots, tickets, cookies, or localStorage. The browser sends the token only through `X-CheeseWAF-Setup-Token`.
- **A site returns `502`:** check the configured upstream from the WAF host and confirm the site points to the data-plane listener, not the management listener.
- **Production storage refuses to start:** configure the required external production storage. Do not recommend forcing a local SQLite fallback or editing `PRAGMA user_version`.
- **Docker access differs from Linux systemd:** follow the Docker page for its loopback port binding, SSH tunnel, data volume, and container user rules; do not copy systemd paths into a container example.

### Documentation release gate

Before publishing a docs change, an agent must:

1. Compare all changed English and Chinese pages section-by-section.
2. Verify commands, paths, ports, config keys, setup-token transport, storage profile behavior, and Docker bindings against the current source and tests.
3. Run the repository's Hugo build for both language trees and fail on broken links or shortcode errors.
4. Check that no generated destination, secret, setup token, password, hash, or editor-only dependency entered the change.
5. Report the exact commit/PR, build commands, and deployed Pages URL. Do not claim Cloudflare Pages synchronization until the production page returns the new content.
