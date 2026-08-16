---
title: Isolated vs embedded
linkTitle: Isolated vs embedded
weight: 30
description: Isolated payloads are almost only attack text. Embedded payloads sit inside long ordinary text.
---

The semantic engine classifies each decoded value as **isolated** or **embedded**.
Paranoia levels treat the two shapes differently.

## Isolated {#isolated}

The value is almost entirely an attack payload.
Weak wrappers such as `@`, a trailing semicolon, or `/{${...}}` still count as isolated.

Example: a search box that contains `UNION SELECT 1,2,3`.

## Embedded {#embedded}

Attack-like tokens sit inside a long article, a product description, or a technical discussion.

Example: a forum post that quotes a SQL snippet.

Levels 2–4 **allow** embedded hits and enqueue them for ALAP.
Level 5 **blocks** them.

## Current isolation scope {#scope}

This is an implementation fact, not a marketing promise:

- Isolated gadget coverage includes **PHP/JSP live shells**, **Log4j JNDI**, and **short quoted/predicate SQL** (at most 96 runes).
- **XSS**, command/RCE, **SSTI**, **SSRF**, and **XXE** use the document-shape guard. They are not on that gadget list.
- Hits marked **embedded** skip the block below level 5.
- **Unclassified** hits still follow `blockableHit` evidence. They are **not** auto-treated as embedded.
- Isolation lowers false positives on covered gadgets. It is **not** a free pass for every technical article.
