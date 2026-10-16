# CTF Practice & Security Writeups

**An evidence-based cybersecurity portfolio by [C4ss20](https://github.com/C4ss20).**

> **Status: Documentation in progress.** I completed a CTF and am reconstructing my personal walkthroughs from the original exercise. No individual challenge solution has been independently verified or published here yet.

## Purpose

This repository will document the reasoning behind each challenge: **observations → hypotheses → tests → validation → security takeaways**. It is intended to demonstrate technical investigation and communication, not simply list tools or flags.

My security interests include cloud security, vulnerability management, and application security. Where applicable, each writeup will explain how to detect or remediate the underlying weakness.

## Challenge index

| Challenge | Category | Status | Writeup |
|---|---|---|---|
| First challenge (title to confirm) | To verify | Draft; not a published solution | [Working notes](challenges/first-challenge/README.md) |

I will only mark a challenge *Verified* once I have checked its solution against my notes or authorized lab output. Unverified content is explicitly labeled.

## Project structure

```text
challenges/        Individual solutions and sanitized evidence
docs/              Methodology and evidence standards
references/        Original learning resources and attribution
templates/         Reusable writeup template
tomar_decision.zip Existing file, left untouched
```

## Writeup process

1. Define the authorized challenge and objective.
2. Separate initial observations from possible explanations.
3. Explain the tests, commands, scripts, and why I chose them.
4. Provide sanitized evidence linking the steps to the result.
5. Explain the root cause (if applicable), defensive implications, and lessons learned.

See [methodology](docs/METHODOLOGY.md), [evidence handling](docs/EVIDENCE.md), and the [writeup template](templates/challenge-writeup.md).

## Learning source & credit

The CTF reference was shared as a [YouTube playlist](https://www.youtube.com/playlist?list=PLDo9DMLZyP6ki_F4Jv4NTOjFOnYHGon0y). Playlist creator, videos, and individual challenge titles still need confirmation; see [source record](references/playlist.md). Material learned from educational walkthroughs will be properly credited, and my own observations will be distinguished from those sources.

## Responsible security practice

Everything here concerns authorized CTFs and intentionally vulnerable labs. Never test third-party infrastructure without permission, or publish passwords, tokens, sensitive customer information, active competition flags, or third-party challenge assets without permission.

## About the existing ZIP

`tomar_decision.zip` predates this documentation project. Its content has not been analyzed here, so this README makes no claims about what is inside.
