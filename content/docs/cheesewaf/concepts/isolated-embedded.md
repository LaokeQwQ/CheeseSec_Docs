---
title: Isolated vs. Embedded Payloads
linkTitle: Isolated vs. Embedded
weight: 30
description: In-depth analysis of semantic engine payload morphology evaluation, contextual boundary detection, and targeted gadget isolation coverage.
---

In modern web applications, user submissions vary widely in structure. In community forums, developer blogs, or technical support tickets, legitimate users frequently submit code snippets, SQL queries, or log entries. Applying strict signature matching to such content inevitably causes widespread false positives.

To resolve this challenge, CheeseWAF's AST semantic engine evaluates the contextual proportion and structural wrapping of decoded parameter values, categorizing detections into **Isolated Payloads** or **Embedded Payloads**.

## Payload Morphologies {#definitions}

### 1. Isolated Payloads {#isolated}

An isolated payload indicates that the parameter value consists almost entirely of an attack pattern without legitimate surrounding business text.

- **Typical Scenario**: Direct inputs into search boxes or login fields such as `UNION SELECT 1,2,3` or `' OR 1=1 --`.
- **Wrapping Evaluation**: Even when attackers prepend/append light obfuscation—such as `@`, trailing semicolons, or `${...}` wrappers—the engine still classifies the value as isolated if the payload dominates the syntax tree.
- **Enforcement**: Under Paranoia Levels 2 through 5, isolated payload detections trigger an **immediate block**.

### 2. Embedded Payloads {#embedded}

An embedded payload occurs when suspicious syntax constructs are enclosed within larger natural language text, documentation, or product descriptions.

- **Typical Scenario**: A user posting in a technical forum discussing database tuning by quoting an example SQL query, or an article referencing a Log4j JNDI string.
- **Enforcement**: Under standard paranoia levels (2–4), the engine **allows the request and asynchronously enqueues the sample to ALAP**, preserving user experience while maintaining vigilance. Under strict mode (Level 5), embedded hits are blocked immediately.

## Gadget Coverage & Engineering Scope {#scope}

To ensure complete operational clarity, the following outlines the exact engineering boundaries of the current feature isolation implementation:

- **Targeted Gadgets**: Dedicated gadget isolation analyzers currently cover **PHP/JSP dynamic webshells**, **Log4j JNDI injection**, and **short quoted/predicate SQL injection** (constrained to fragments under 96 runes/characters).
- **Document Shape Guards**: Attack vectors such as **XSS**, **Remote Code Execution (RCE)**, **Server-Side Template Injection (SSTI)**, **Server-Side Request Forgery (SSRF)**, and **XML External Entity (XXE)** are evaluated by specialized Document Shape Guards, operating independently of the short-gadget analyzer.
- **Evidence Fallback**: Detections classified as `embedded` bypass inline blocking below Level 5. Unclassified or ambiguous hits adhere strictly to deterministic `blockableHit` evidence rules and are never silently downgraded to embedded status.
- **Operational Guidance**: Isolation mitigates false positives on known gadgets in rich-text workflows. For strictly structured API endpoints, enabling higher paranoia levels or schema validation remains recommended.
