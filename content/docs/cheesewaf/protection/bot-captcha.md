---
title: Bot challenge and CAPTCHA
linkTitle: Bot and CAPTCHA
weight: 40
description: JS clearance, PoW, slider, image CAPTCHA, login CAPTCHA, and the waiting room.
---

Console: **Bot challenge**, plus **CAPTCHA lab** for operators who design challenges.
Config: `protection.bot` and `console.login.captcha`.

The sample starts with `protection.bot.enabled: false`.
Turn it on only after you have a site that can complete a browser challenge.

## Traffic challenge {#traffic}

| Key | Role |
| --- | --- |
| `js_challenge` | Issue a JS clearance cookie |
| `captcha` | Extra CAPTCHA after JS |
| `captcha_type` | `pow`, `image`, or `slider` |
| `cookie_name` | Default `cheesewaf_js_clearance` |
| `path_prefixes` | Where the challenge applies |
| `exempt_path_prefixes` | Skip, sample includes `/health` |
| `suspicious_user_agents` | Extra scrutiny for curl, sqlmap, nuclei, and similar |

Keep `secret` out of git.
Let the process generate it into the data directory.

## Challenge kinds {#kinds}

- **PoW / Altcha.** Header `X-CheeseWAF-Altcha` by default.
- **Slider.** Geometry and min-drag live under `slider_captcha_*`.
- **Image.** Length, size, and audio-limit knobs.
- **Behavior pack.** Curve draw, scratch, icon click, and related lab types. Use the lab before you enable them on production traffic.

Upload custom assets under `/api/captcha/assets`.
Quota and remote source tests are on the same console page.

## Login CAPTCHA {#login}

`console.login.captcha` protects the **management** login, not the data plane.
The sample uses a slider with an optional PoW.

`console.login.security_entry` can hide the login behind a secret path and cookie.

## Waiting room {#waiting-room}

`waiting_room` plus `waiting_room_max_active` queues excess clients instead of dropping them immediately.
See also [Rate limit](../ratelimit/).
