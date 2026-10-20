# Sombras en el Sistema — TheM4rv3ls CTF (Windows)

**Category:** Windows Forensics · **Points:** 100 · **Techniques:** offline Registry analysis, Windows Security Event ID 4625, Base64, MD5

> **Documentation note:** I completed this CTF challenge, but my original evidence archive and full first-hand screenshots were not retained. This is a retrospective reconstruction, not a new examination of the original Windows host. The encoded clue and final MD5 calculation **have been verified offline**. No third-party videos, video screenshots, or YouTube links are used as evidence.

## Objective
The fictional CTF scenario describes suspicious Windows system activity. The goal is to inspect an offline Windows evidence bundle, find a hidden identifier in the records, and submit its **MD5 hex digest**. This is a distinct challenge from [Sombras en el Sistema — Linux](../sombras-en-el-sistema-linux/README.md), although both use the same title.

## Findings at a glance
| Phase | Finding | Meaning |
| --- | --- | --- |
| Evidence inventory | Windows artifacts including `registry`, `winevt`, `Prefetch` and user directories | Offline forensic collection |
| Registry triage | `SAM` and per-user `NTUSER.DAT` | Account context; not the final clue |
| Security log triage | **Event ID 4625**, failed logon | Authentication anomaly search |
| Suspicious event | Base64-like value in the **Account Name** field | Hidden CTF payload |
| Decoding | Reverse string, then **four Base64 decodes** | `MrMarvels{Windows_failed}` |
| Final verification | MD5 of exact `Windows_failed` | `b209b6f2713d454c1273f2b5b702708a` |

## 1. Inventory the artifacts
The extracted evidence collection included directories for `registry`, `winevt`, `Prefetch`, `Appdata`, `Profile`, and filesystem information. Start by identifying the saved EVTX files and Registry hives instead of assuming that any single artifact contains the answer.

```bash
find ./evidence -iname '*.evtx'
find ./evidence -type f \( -iname 'sam' -o -iname 'ntuser.dat' \)
```

Paths above are illustrative: the original evidence bundle is not distributed here and is not required for offline flag verification.

## 2. Review the offline Windows Registry
The historical investigation used **RegRipper** on the collected local `SAM` hive and a Marvel-themed user's `NTUSER.DAT`. This helped identify accounts and review user settings. Representative RegRipper syntax (depending on the installed package) is:

```bash
rip.pl -r ./evidence/registry/sam -a > sam-parsed.txt
rip.pl -r ./evidence/registry/users/nick_fury/ntuser.dat -a > user-parsed.txt
```

The registry review did not yield the final answer. Note that Windows Registry hives are **binary** artifacts: `dos2unix` is for text line endings and is not a Registry parser.

## 3. Investigate failed logons in Event Viewer
The saved Windows Security logs were opened via **Event Viewer → Action → Open Saved Log…**. Filter the Security log using **Event ID `4625`**. A 4625 event records a *failed logon attempt*; it does not automatically prove malicious activity.

The recorded suspicious event included a **type 3 network logon**, failure information, and an unusual value in **Account Name** where an ordinary username would normally appear. Review the time, failure code, Account Name, source address (when available), and whether related success Event ID 4624 records exist. Such event fields should be treated as untrusted data.

## 4. Reverse and decode the abnormal Account Name
The string appeared with `==` at its beginning, an unusual position for Base64 padding. Reversing characters puts the padding at the end.

```text
==QNBRkVWFzRkRnWGN1SkBTWIZEVihVMX50dwATYhVzVWBDcwIla01mUVBHbO9mTqZFawtWYUxmRiNnUxM1batmV
```

The reconstructed decoding chain is:

```text
Reverse characters
  → From Base64 (1)
  → From Base64 (2)
  → From Base64 (3)
  → From Base64 (4)
  → MrMarvels{Windows_failed}
```

This is reversible **obfuscation**, not encryption. The correct identifier extracted from the wrapper is **`Windows_failed`** — uppercase `W`, lowercase `failed`.

## 5. Produce the requested MD5 digest
The task asks for the **MD5 of the identifier inside the braces**, not the entire `MrMarvels{…}` string. The exact spelling, capitalization, and absence of a newline matter.

```bash
printf %s 'Windows_failed' | md5sum
```

**Verified answer:**

```text
b209b6f2713d454c1273f2b5b702708a
```

To reproduce the complete chain without the evidence archive, run the included read-only Python helper:

```bash
python3 challenges/sombras-en-el-sistema-windows/scripts/recover_clue.py
```

The script reverses the stored string, strictly validates and decodes **four Base64 layers**, extracts the wrapped clue, and verifies its MD5. It performs no network access or modification of forensic files.

## Why the findings matter
| Indicator | Forensic significance | Suggested validation |
| --- | --- | --- |
| Security Event 4625 | Failed account logon, potentially benign or suspicious | Correlate source host, frequency, timestamps, and 4624 successes |
| Unexpected Account Name | Untrusted event-field content, possibly deliberately encoded | Preserve full raw event and analyze offline |
| SAM / NTUSER.DAT | Account and user context | Correlate with Event Logs and timeline artifacts |
| Reversal and repeated Base64 | Conceals a readable string without cryptographic secrecy | Follow each reversible layer and record intermediate findings |
| MD5 result | Puzzle submission digest | Do not equate puzzle use of MD5 with secure password storage |

## Lessons learned
1. **Use the correct Windows event ID:** 4625 narrows investigation to failed logons.
2. **Inspect fields, not just messages:** the clue sat in the unusual Account Name value.
3. **Do not misinterpret Registry hives:** parse binary structures with proper offline forensic tools.
4. **Count encoding layers:** this reconstruction requires a reversal followed by four Base64 decodes.
5. **Hash the exact intended identifier:** `Windows_failed` produces a different MD5 from `windows_failed` or a newline-terminated string.
6. **Distinguish result verification from source authentication:** the transformation is independently reproducible; the original EVTX file was not reacquired for this publication.

## Tools and evidence limits
**Windows Event Viewer · RegRipper · Linux shell · CyberChef · Python 3 (`base64`, `hashlib`)**

- Original forensic bundle: not retained in this repository.
- Reconstructed encoded string: documented above and verified through all decoding stages.
- Raw original Security.evtx evidence and a current chain of custody: unavailable.
- No third-party screenshots or recordings are submitted as evidence.

*Educational, intentionally scoped CTF analysis only.*
