---
title: Bot Challenges & CAPTCHA Mitigation
linkTitle: Bot & CAPTCHA
weight: 40
description: Configure silent JavaScript challenges, Proof of Work (Altcha), slider and image CAPTCHAs, management console defense, and waiting room scheduling.
---

Modern web applications constantly face malicious automated traffic, including AI web scrapers, credential stuffing attacks, and automated vulnerability scanners. CheeseWAF provides multi-layered bot mitigation and challenge capabilities. Configure policies in the Web console under **Bot Challenge** and **CAPTCHA Lab**, or declare them in `protection.bot` and `console.login.captcha`.

## Traffic Challenge Configuration {#traffic}

```yaml
protection:
  bot:
    enabled: false
    js_challenge: true
    captcha: true
    captcha_type: "slider"
    cookie_name: "cheesewaf_js_clearance"
    path_prefixes: ["/login", "/register", "/api/order"]
    exempt_path_prefixes: ["/health", "/static"]
    suspicious_user_agents: ["curl", "sqlmap", "nuclei"]
```

| Configuration Parameter | Description |
| --- | --- |
| `js_challenge` | Issues silent JavaScript challenge and sets clearance cookie upon validation |
| `captcha` | Overlays interactive CAPTCHA validation on top of JS challenge |
| `captcha_type` | Challenge mechanism: `pow` (Proof of Work), `slider` (sliding puzzle), or `image` (character glyphs) |
| `cookie_name` | Name of the authorization clearance cookie; defaults to `cheesewaf_js_clearance` |
| `path_prefixes` | List of URI path prefixes where challenges are strictly enforced |
| `exempt_path_prefixes` | Whitelist of URI prefixes exempt from challenges (e.g., `/health`) |
| `suspicious_user_agents` | User-Agent substring matches that immediately escalate to full human verification |

{{% pageinfo color="warning" %}}
Do not check challenge signing `secret` values into version control. When the value is empty or a known placeholder, setup/startup generates a strong runtime secret and persists it in the protected runtime configuration or runtime secret file according to the selected deployment; it is not an in-memory-only guarantee. Keep the runtime path and permissions private.
{{% /pageinfo %}}

## Challenge Types & Interaction Mechanisms {#kinds}

- **Proof of Work (PoW / Altcha)**: Clients compute a cryptographic hash challenge in the browser background and submit the nonce via the `X-CheeseWAF-Altcha` request header. This is fully frictionless for real users while making automated concurrent scraping computationally prohibitive.
- **Sliding Puzzle (Slider)**: Analyzes mouse drag trajectories and validates minimum drag timing thresholds (configured via `slider_captcha_*`).
- **Character Image (Image)**: Supports configurable string lengths, image dimensions, and audio assistance limits.
- **Experimental Behavioral Tests**: Includes gesture curves, scratch-off, and icon point-and-click puzzles. Verify user experience in the console **CAPTCHA Lab** before rolling out to production traffic.

Custom background images and iconography can be uploaded via `/api/captcha/assets`.

## Management Console Login Defense {#login}

`console.login.captcha` protects the **Web Management Console login endpoint** (completely isolated from business data plane traffic), supporting slider puzzles with optional PoW verification.

The source template enables the management-login slider CAPTCHA by default (`console.login.captcha.enabled: true`). After initialization, the first browser login therefore requires completing the human-verification challenge in addition to the username and password. For local test fixtures only, set `console.login.captcha.enabled: false` in a runtime configuration copy and restart; do not disable this control in production merely to bypass acceptance checks.

Additionally, enable `console.login.security_entry` to obscure the management portal behind an obfuscated path and pre-shared authorization cookie.

## Waiting Room Queue Scheduling {#waiting-room}

Enable `waiting_room: true` and specify `waiting_room_max_active` to gracefully hold excess concurrent clients in an organized queue during flash sales or traffic surges, preventing origin resource exhaustion. The waiting room is effective only when the global `protection.policy.bot_cc` policy is not `off` and its action is `challenge`; enabling the site waiting-room flag alone is not sufficient. See [Rate Limiting](../ratelimit/).
