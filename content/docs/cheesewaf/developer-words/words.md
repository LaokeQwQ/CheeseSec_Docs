---
title: Words from the Developer
linkTitle: Developer's Words
weight: 10
description: Personal reflections, architectural convictions, and perspectives from the author of CheeseWAF.
---

> *"Security should not be an expensive, closed black box that exhausts operations teams. It should be transparent, elegant, and dependable engineering infrastructure."*

---

## Preface {#preface}

If you are reading this document, perhaps you are preparing to deploy CheeseWAF on your servers, troubleshooting an elusive security incident, or simply exploring web security and application architecture as a fellow practitioner or enthusiast.

Whichever brings you here, I welcome you with all my heart.

Here, without cold CLI parameters or cryptic regular expression syntax, I want to use my own straightforward words to share why CheeseWAF came to life, and everything I have stood by and reflected upon throughout this journey.

---

## Why CheeseWAF Was Created {#why-cheesewaf}

Before committing to the project and writing the very first line of code for CheeseWAF, like many website operations and security engineers facing increasingly intricate web requests, I found myself caught in a difficult dilemma between exorbitant commercial WAF licensing quotes and the grueling rule maintenance, high false-positive, and false-negative rates of traditional open-source tools.

We often found ourselves trapped between two extremes:
- **Over-reliance on traditional regex signatures**: As signatures accumulate, maintenance overhead multiplies exponentially, yet a slight variation in multi-layer encoding or character nesting can bypass them;
- **Blindly forcing LLMs into the synchronous request path**: In the name of "intelligence," forcing synchronous waits for remote LLM inferences within the reverse proxy pipeline turns a simple HTTP exchange into hundreds of milliseconds or even seconds of latency, ultimately crippling the entire business service.

We firmly believe that **accuracy, low latency, and maintainability are the lifeline of the Data Plane, while deep semantic understanding should be entrusted to an asynchronous sidecar capable of decoupled execution and continuous self-learning.** This is where CheeseWAF began: we aspire to build a truly commercial-grade, self-contained, out-of-the-box self-hosted WAF, empowering every developer and operations team to take full ownership of their application security, unconstrained by cloud vendors and expensive commercial licenses.

---

## Architectural Convictions {#philosophy}

Throughout the evolution of CheeseWAF, several engineering principles have been held as non-negotiable baselines:

1. **Self-Contained Single Binary**: Consolidating complex components, the Web management console, and security engines into a single executable without wrestling with databases, middleware, or external dependencies beforehand. Written 100% in Go, CheeseWAF inherently possesses outstanding robustness and excellent portability, running directly across mainstream Linux, Windows, and macOS platforms. Furthermore, we natively support the LoongArch architecture, enabling seamless execution on hardware powered by domestic Loongson processors.
2. **Zero Compromise on the Request Path**: An inspection pipeline capable of sub-millisecond to microsecond processing, rooted in clear Abstract Syntax Tree (AST) semantic parsing. Dynamically tuned to hardware performance profiles and refined through extensive GC tuning and hardware acceleration, it relentlessly pursues ultimate performance and concurrency.
3. **Defensive Authority Stays with the Operator**: From gradual paranoia level progression to automated adoption of threat reviews, you can freely choose between autonomous AI remediation and manual alert approval. The ultimate control and final voice over your defense line always rest in your hands.

---

## A Note to the Community {#letter-to-community}

Building a serious Web application security product is by no means easy. It demands continuous adaptation to rapidly shifting attack vectors, modern Web protocols, and diverse production constraints.

As a newly launched, independently maintained open-source project in its formative stages, CheeseWAF continues to mature. If it helps you ward off an unexpected attack late at night, relieves your startup or small business from the heavy burden of commercial WAF licensing or cloud security costs, or simply makes your daily operations a bit easier and more dependable, that is already my greatest honor.

Anyone with ideas, feedback, or constructive critiques is warmly invited to connect via [GitHub Issues](https://github.com/LaokeQwQ/CheeseWAF/issues) or [email (coqimax@gmail.com)](mailto:coqimax@gmail.com).

Finally, my sincere gratitude for your trust and confidence in CheeseWAF, and my deepest respect to everyone who loves open source and security craftsmanship.

<div style="text-align: right; margin-top: 2rem; font-style: italic;">
— Laoke (老可), Creator &amp; Core Developer of CheeseWAF<br>
September 2026
</div>
