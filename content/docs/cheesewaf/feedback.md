---
title: Feedback & Security Reporting
linkTitle: Feedback
weight: 210
description: Communication channels and procedures for issue reporting, feature suggestions, and critical security disclosures.
---

CheeseSec welcomes community contributions and operational feedback. Please use the appropriate channel below depending on the nature of your report:

## General Feedback & Issue Tracking {#general-feedback}

### 1. GitHub Issues

For operational defects, bugs, runtime errors, documentation corrections, or feature proposals, open an issue in the corresponding GitHub repository:

| Project Scope | Repository & Issue Tracker | Intended Coverage |
| --- | --- | --- |
| **Core Engine & Server** | [LaokeQwQ/CheeseWAF Issues](https://github.com/LaokeQwQ/CheeseWAF/issues) | WAF daemon, data plane proxy, AST semantic engine, CLI utilities, and Web console |
| **Gateway Adapters** | [LaokeQwQ/CheeseWAF-Adapters Issues](https://github.com/LaokeQwQ/CheeseWAF-Adapters/issues) | NGINX `auth_request`, Envoy `ext_authz`, and the `adapterd` daemon |
| **Plugin Ecosystem** | [LaokeQwQ/CheeseSec_Plugin Issues](https://github.com/LaokeQwQ/CheeseSec_Plugin/issues) | CRP specification, package manifests, and registry admission policies |
| **Technical Documentation** | [LaokeQwQ/CheeseSec_Docs Issues](https://github.com/LaokeQwQ/CheeseSec_Docs/issues) | Documentation accuracy, clarity, and bilingual synchronization |

{{% pageinfo color="info" %}}
**Issue Submission Guidelines**: Include your operating system, architecture, CheeseWAF version (`cheesewaf version`), deployment mode (systemd service or Docker), and minimal reproduction steps. Sanitize logs to ensure database credentials, API tokens, and private keys are never exposed in public issues.
{{% /pageinfo %}}

### 2. Email Correspondence

For general questions, private deployment inquiries, or matters not suitable for a public tracker, contact the project team via email:

- **Contact Email**: `coqimax@gmail.com`

---

## Critical Vulnerabilities & Security Disclosures {#security-reporting}

CheeseSec treats security defects with the highest priority. If you identify a security vulnerability, detection bypass, or critical stability defect in CheeseWAF or its ecosystem components, please follow **Responsible Disclosure** practices and do not post exploit details in public channels (such as GitHub Issues or social media).

### Dedicated Security Contact {#security-contact}

- **Vulnerability Reporting Mailbox**: `sec@cheesesec.com`

### Scope of Security Reports

Reportable issues include, but are not limited to:
- Remote Code Execution (RCE) or arbitrary command injection
- Management plane authentication bypass, privilege escalation, or session forgery
- Universal detection bypasses against the AST semantic engine or baseline rulesets
- Uncontrolled resource consumption, memory leaks, or deadlocks causing high-severity Denial of Service (DoS)
- Exposure or insecure handling of sensitive configuration data, credentials, or keys

### Recommended Report Contents

To accelerate verification and resolution, please include:
1. **Description & Severity**: Vulnerability class, affected endpoints or components, and estimated impact.
2. **Affected Versions**: Specific release versions or Git commit hashes.
3. **Proof of Concept (PoC)**: Clear, reproducible steps, including sample HTTP payloads, curl commands, or scripts.
4. **Prerequisites**: Required user roles, configuration flags, or network topology necessary to trigger the defect.
5. **Remediation (Optional)**: Suggested patches or workarounds, if available.

### Response & Handling Workflow

1. **Acknowledgment**: The security team confirms receipt of reports sent to `sec@cheesesec.com` and opens an internal tracking case.
2. **Triage & Reproduction**: Engineers reproduce the PoC in an isolated environment, evaluate severity, and prioritize a patch.
3. **Patch & Advisory**: Once a fix is implemented and verified, a security patch release and corresponding Security Advisory are published. We request that reporters maintain confidentiality until the patch is publicly available.
