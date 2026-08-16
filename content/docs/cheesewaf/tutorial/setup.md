---
title: System Initialization Wizard
linkTitle: Initialization
weight: 10
description: Access the /setup wizard to provision your initial administrator account, archive security credentials, and configure management network boundaries.
---

Upon launching CheeseWAF for the first time, complete the setup wizard to establish security baselines and administrative credentials:

{{% steps %}}

### 1. Access the Initialization Wizard {#open-wizard}

- **Local / Bare-Metal Deployment**: Open `http://127.0.0.1:9443/setup` in your browser.
- **Docker Container Deployment**: Open `https://<SERVER_IP>:9443/setup` (accept the self-signed certificate in your browser during initial access).

If a setup token was emitted in your service logs or stdout, paste it into the prompt to verify administrative ownership.

### 2. Provision Admin Account & Archive Master Secrets {#create-admin}

Enter the initial administrator username and configure a strong password compliant with the password complexity policy. The wizard will display generated system master keys and recovery credentials; securely record and archive these secrets, as CheeseWAF will not display them in clear text again.

### 3. Verify Management Plane Boundaries {#confirm-listener}

- For standalone or single-host deployments, maintain `server.admin_listen` on the local loopback address (`127.0.0.1:9443`).
- Set `server.admin_public: true` only if a trusted TLS certificate is installed and strict network-level Access Control Lists (ACLs) are enforced.

{{% /steps %}}

After completing the wizard, navigating to the management address will automatically redirect to the Web console login screen. Alternatively, administrative users can be managed via the `waf-cli` TUI panel or the `cheesewaf user` command.
