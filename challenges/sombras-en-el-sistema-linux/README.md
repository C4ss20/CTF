# Sombras en el Sistema — TheM4rv3ls CTF (Linux)

**Category:** Linux Forensics · **Points:** 100 · **Focus:** account activity, shell-history artifacts, persistence indicators, forensic correlation, MD5

> **Documentation scope:** This is a retrospective reconstruction of a challenge I completed. My original evidence archive and a complete set of session screenshots were not retained. The extracted artifacts described here come from the available challenge notes, but I did **not** independently repeat the original acquisition or all filesystem searches while preparing this document. The final MD5 calculation was reproduced offline. No video links or third-party screenshots are presented as proof of completion.

## Objective

In the fictional TheM4rv3ls setting, system records show signs of unauthorized access and suspicious persistence. The task is to investigate a Linux evidence bundle, extract a hidden key, convert that key to an **MD5 hex digest**, and submit the digest to the challenge platform.

The prompt refers to **Protocol PHOTON**. In this challenge, the required transformation is an MD5 calculation—not decryption and not password cracking.

## Investigation summary

| Evidence artifact | Relevant observation | Analyst interpretation |
| --- | --- | --- |
| Evidence bundle | Multiple directories including `users`, `persistence`, `processes`, `network`, and `audit.txt` | Offline forensic collection rather than a live target |
| `users/lastlog.txt` | An interactive last-login entry for `carol_danvers`; most service accounts display no login | Useful starting point for reviewing user activity, not proof of compromise by itself |
| `users/usuarios/carol_danvers/bash/history_file.txt` | Account-management commands referring to `skrull` and `skrull_login` | Possible creation/manipulation of an unusual local account |
| `users/usuarios/skrull_boss/bash/history_file.txt` | Repeated cron-related commands and candidate strings `skrull_persistence` and `skrull_backdoor` | Stronger indicators of a persistence attempt and likely embedded puzzle clue |
| Reconstructed key | `skrull_backdoor` | Candidate selected from the suspicious command history |
| MD5 verification | `9de9a032343dbf5f749c93304e962f90` | Final challenge submission value |

## 1. Inventory the Linux evidence

After safely extracting the CTF-provided evidence archive into a local working directory, examine its layout **without modifying the artifacts**:

```bash
find Evidence_CaptainMarvel_feb-24-02.33.31 -maxdepth 2 -type f | sort
```

The evidence tree in the documented investigation contains sections for user accounts, filesystem information, network data, persistence, security, processes, and services.

**Why start with users?** The question involves unauthorized activity, and user login metadata and shell histories can help connect identities to system changes.

## 2. Examine login activity

Within the extracted `users` directory, read:

```bash
cat users/lastlog.txt
```

The recorded `lastlog.txt` has a populated entry for `carol_danvers`, including an interactive terminal session and an originating private IP address. Many other account rows show that no login was recorded.

**Interpretation:** This prioritizes `carol_danvers` for further review. It does not mean that other accounts were never used, nor does a successful login alone prove an intrusion. Log coverage and possible tampering must be considered.

## 3. Review the relevant user's shell history

The evidence includes per-user directories under `users/usuarios/`. Review the available history files:

```bash
cat users/usuarios/carol_danvers/bash/history_file.txt
```

The history shows system-administration activity, including installation of an SSH service and multiple account-management operations involving an unusual user named `skrull`.

The notable clues are **account creation or removal**, **SSH-related changes**, and **embedded strings with a flag-like wrapper**. The latter are puzzle-specific markers, not proof that the strings were real production credentials.

A second account, `skrull_boss`, provides a stronger lead.

## 4. Investigate the suspected persistence trail

Review the `skrull_boss` history:

```bash
cat users/usuarios/skrull_boss/bash/history_file.txt
```

The captured command history contains attempts involving `crontab` and files under `/etc/cron.d/`. These commands reference two distinct marker names:

```text
skrull_persistence
skrull_backdoor
```

Cron is a legitimate Linux scheduler, but unexpected jobs executing scripts or commands on a recurring basis can be a **persistence mechanism**. Here, those history entries warrant closer examination because of the suspicious account context and repeated cron-related changes.

The histories include references resembling:

```text
... /tmp/cron_flag
... /etc/cron.d/persistence_flag
... crontab -u skrull_boss
```

These are **indicators to investigate**, not instructions to create cron jobs. A command recorded in shell history does not prove its successful execution. To validate persistence in a real forensic case, corroborate it with actual crontab contents, file metadata, process records, and timestamps.

## 5. Choose the clue and compute the MD5 answer

The evidence has multiple flag-like strings. The candidate that yielded the recorded solution was:

```text
skrull_backdoor
```

The challenge asks for its MD5 representation. Calculate the digest over the **exact lowercase UTF-8 string**, without a trailing newline:

```bash
printf %s 'skrull_backdoor' | md5sum
```

Result:

```text
9de9a032343dbf5f749c93304e962f90
```

**Recovered answer:** `9de9a032343dbf5f749c93304e962f90`

The MD5 calculation was also independently reproduced using Python's standard library. Note that the answer is **the raw hexadecimal digest**, rather than a `MrMarvel{...}` wrapper. The prompt explicitly requests the MD5 hash as the final submission.

The standalone verification script can be run from the repository root:

```bash
python3 challenges/sombras-en-el-sistema-linux/scripts/verify_md5.py
```

Expected output:

```text
Candidate key: skrull_backdoor
MD5: 9de9a032343dbf5f749c93304e962f90
Offline verification passed.
```

## Forensic techniques and defensive relevance

| Technique | Purpose in this challenge | Application to real investigations |
| --- | --- | --- |
| Directory inventory | Identify available acquisition artifacts | Preserve structure and establish scope |
| `lastlog` review | Prioritize accounts with recent logins | Correlate with SSH, PAM, audit, and network logs |
| Shell-history review | Find user-management and scheduling commands | Build a timeline; seek independent corroboration |
| Cron-related indicators | Investigate possible scheduled persistence | Examine user crontabs, `/etc/cron*`, permissions and change history |
| Exact-string MD5 calculation | Produce the CTF's requested answer | A deterministic checksum is **not** a secure modern password-storage method |

## Lessons learned

1. **Correlate artifacts rather than relying on a single line.** Login records point toward a user whose command history provides a connection to another suspicious account.
2. **Shell history is evidence of recorded commands, not proof of successful execution.** Additional artifacts would be needed to establish actual persistence and chronology.
3. **Consider decoys.** The record contains both `skrull_persistence` and `skrull_backdoor`; the correct answer requires identifying the intended challenge key.
4. **Handle exact input bytes carefully.** `echo` adds a newline by default and can produce the wrong digest. `printf %s` avoids it.
5. **Maintain the distinction between a hash and encryption.** MD5 transforms an input into a one-way digest; no decryption is performed.
6. **State verification limits.** The hash is reproducible; the original evidence bundle has not been independently reprocessed for this publication.

## Reproducibility and evidence limits

- **Original artifact:** Linux forensic evidence ZIP with a directory such as `Evidence_CaptainMarvel_feb-24-02.33.31` — not uploaded to this repository.
- **Historical findings:** Account histories contain suspicious `skrull`-related activity and possible cron persistence.
- **Verified offline:** `MD5("skrull_backdoor")` equals the final hex digest above.
- **Not claimed:** A fresh forensic acquisition, a verified timestamped chain of custody, or a confirmed real-world intrusion.

*Educational documentation of an intentionally scoped CTF environment.*
