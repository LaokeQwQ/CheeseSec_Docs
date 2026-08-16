---
title: Initialize
linkTitle: Initialize
weight: 10
description: Create the first administrator at /setup and lock down the management listener.
---

{{% steps %}}

### Open the wizard {#open-wizard}

On a local install open `http://127.0.0.1:9443/setup`.
On Docker open `https://<host>:9443/setup` and accept the self-signed certificate.

If the process prints a setup token, paste it when the wizard asks.

### Create the admin {#create-admin}

Set a username and a password that meets the console password policy.
Save every generated secret the wizard shows.
CheeseWAF will not print them again in clear text.

### Confirm the listener {#confirm-listener}

Leave `server.admin_listen` on loopback for a single-host install.
Set `server.admin_public` to `true` only with TLS and a network policy in front.

{{% /steps %}}

After setup, the same URL becomes the login page.
CLI users can also run `waf-cli` (TUI) or `cheesewaf user`.
