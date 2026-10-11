---
title: CheeseWAF
linkTitle: CheeseWAF
weight: 10
description: Self-hosted Web Application Firewall with a single-binary data plane, management console, and asynchronous threat review.
---

CheeseWAF is a self-hosted reverse-proxy WAF. It keeps deterministic request inspection on the data plane and runs optional model-assisted review out of band, so an external model is never required to serve normal traffic.

{{% pageinfo color="info" %}}
The shortest supported path is: run the one-line Linux installer, open the HTTPS setup URL it prints, complete `/setup`, and onboard one test site. Download releases from [GitHub Releases](https://github.com/LaokeQwQ/CheeseWAF/releases). The Apache License 2.0 is available in the [source repository](https://github.com/LaokeQwQ/CheeseWAF/blob/master/LICENSE).
{{% /pageinfo %}}

## Choose a path {#start-here}

Start with the task you need to complete:

{{< nav-cards cols="2" >}}
{{< nav-card title="Quick Start" link="/docs/cheesewaf/tutorial/" icon="fa-solid fa-rocket" desc="Install, initialize the console, verify the service, and protect one test site." />}}
{{< nav-card title="Linux (recommended)" link="/docs/cheesewaf/install/linux/" icon="fa-brands fa-linux" desc="Install with the one-line installer or a verified archive, then run as a systemd service." />}}
{{< nav-card title="Docker" link="/docs/cheesewaf/install/docker/" icon="fa-brands fa-docker" desc="Run an isolated evaluation or compose-based deployment with explicit port and data mounts." />}}
{{< nav-card title="Production operations" link="/docs/cheesewaf/operations/" icon="fa-solid fa-shield-halved" desc="Review network boundaries, storage, backups, upgrades, and air-gapped operation." />}}
{{< /nav-cards >}}

## Five-minute path {#five-minute-path}

1. Prepare a supported Linux host with `sudo`, enough disk for the release and runtime data, and an administration path to port `9443`.
2. Run the one-line installer. It downloads and verifies the latest stable release, installs the systemd service when available, and prints the HTTPS setup URL. Follow the verified archive path in the [Linux guide](install/linux/) when the host cannot reach GitHub.
3. Open the printed HTTPS URL, create the first administrator, and keep the one-time token out of tickets, screenshots, shell history, and logs.
4. Follow [Quick Start](tutorial/) to add a test site before changing production DNS.

The installer creates a dedicated `cheesewaf` system user, copies the Web Console assets, installs the runtime configuration only when it does not already exist, enables HTTPS on the management listener, and places the systemd unit under `/etc/systemd/system` by default. It does not replace an existing configuration.

## What CheeseWAF provides {#capabilities}

- **Data plane:** reverse proxying, request normalization, AST-based semantic inspection, ACLs, IP and fingerprint controls, rate limiting, and bot challenges.
- **Management plane:** Web Console, REST API, CLI/TUI workflows, setup wizard, RBAC, audit records, and operational health endpoints.
- **Asynchronous review:** optional ALAP review for ambiguous samples. The review queue is out of band; it must not be treated as the inline enforcement path.
- **Storage choices:** the default `temporary` profile uses the local runtime store. Production deployments must explicitly provide the required external storage and must fail closed instead of silently falling back.
- **Adapters and plugins:** adapterd integrates existing gateways; CRP packages provide signed offline resources. Review [Plugins & CRP](plugins/) before enabling third-party packages.
- **Air-gapped operation:** release archives, checksums, signed resources, and local runtime data can be managed without making the data plane depend on an external model.

## Default network boundaries {#default-listeners}

| Plane / service | Default address | Purpose |
| --- | --- | --- |
| Data plane | `http://127.0.0.1:8080` | Business traffic inspection and reverse proxying |
| Management plane | `https://PUBLIC_IP:9443/setup` → `https://PUBLIC_IP:9443/SECURITY_ENTRY` | First setup uses a fixed `/setup` path with a one-time token; after setup, the generated security entry signs an access Cookie and redirects to login |
| Cluster plane | `https://127.0.0.1:9444` | Optional mTLS node interconnect when clustering is enabled |
| Local controller | `http://127.0.0.1:17943` | Desktop helper controller for Windows and macOS |

The one-line installer binds the management listener on all interfaces, enables HTTPS, and gates first setup with a one-time token and a generated security entry. Restrict port `9443` to trusted administration networks before exposing it. The shipped configuration template and the setup wizard default to `0.0.0.0:9443` with `server.admin_public: true`. A configuration that omits the `server` keys falls back to the loader default `127.0.0.1:9443`. A public listener still requires management TLS, a valid certificate, and an external access policy. Do not expose `/setup` or the management port to the Internet as a substitute for those controls.

## Continue

{{< nav-cards cols="2" >}}
{{< nav-card title="Core concepts" link="/docs/cheesewaf/concepts/" icon="fa-solid fa-diagram-project" desc="Understand the request lifecycle, management boundaries, storage profiles, and enforcement order." />}}
{{< nav-card title="Security policies" link="/docs/cheesewaf/protection/" icon="fa-solid fa-lock" desc="Configure semantic inspection, ACLs, IP controls, challenges, and rate limits." />}}
{{< nav-card title="Gateway adapters" link="/docs/cheesewaf/adapters/" icon="fa-solid fa-network-wired" desc="Connect NGINX or Envoy through the authenticated adapter contract." />}}
{{< nav-card title="Configuration reference" link="/docs/cheesewaf/config/" icon="fa-solid fa-sliders" desc="Look up supported keys, defaults, validation rules, and runtime boundaries." />}}
{{< /nav-cards >}}
