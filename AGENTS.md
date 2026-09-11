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
