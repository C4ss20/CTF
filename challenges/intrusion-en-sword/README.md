# Intrusión en S.W.O.R.D. — TheM4rv3ls CTF

**Category:** Web Hacking · **Points:** 100 · **Techniques:** HTTP log analysis, file-type identification, Unicode/Braille decoding

> **Write-up status:** Completed challenge, documented retrospectively. The original `themarvels_logs.zip` and a complete set of my original terminal captures are not available in this repository. The steps below reflect the observed investigation and recorded result; they have not been independently rerun against the original archive for this publication. No third-party screenshots or recordings are presented as my evidence.

## Objective

S.W.O.R.D.'s systems have reportedly been compromised. The challenge asks the analyst to investigate suspicious HTTP requests, including potential SQL injection, cross-site scripting (XSS), and encoded payloads, and **submit one of seven payloads**.

A downloadable archive, `themarvels_logs.zip`, contains 40 numbered text logs. The solution documented here focuses on the suspicious data in file 7. It does **not** establish that any attack in the surrounding log traffic successfully exploited a real application.

## Summary of findings

| Step | Observation | Interpretation |
| --- | --- | --- |
| Unpack the challenge archive | 40 `themarvels_logs_*.txt` files | Multiple candidate requests to review |
| Check file types | Most files are ASCII; `themarvels_logs_7.txt` is UTF-8 Unicode text | An unusual character set merits closer inspection |
| Inspect file 7 | A suspicious `POST /files/reports` request contains encoded-looking characters | Candidate for further decoding |
| Isolate the non-ASCII sequence | Symbols resemble Braille | Try an explicit Braille decoding operation |
| Decode | The **From Braille** operation outputs a flag-format string | Recover the challenge submission |

## 1. Unpack and inventory the log archive

After downloading the archive from the CTF platform, extract it to an isolated working directory:

```bash
mkdir -p intrusion-sword
cd intrusion-sword
unzip ../themarvels_logs.zip
ls -1 themarvels_logs_*.txt
```

The archive expands into 40 numbered text files. A quick inventory establishes the scope and file naming pattern before focusing on individual requests.

## 2. Use file-type analysis to narrow the search

Instead of immediately reading all 40 files, first inspect their detected data types:

```bash
file themarvels_logs_*.txt
```

The key anomaly is:

```text
themarvels_logs_7.txt: Unicode text, UTF-8 text
```

The remaining numbered logs were identified as ASCII text in the recorded investigation. Because UTF-8 can represent characters that are not ASCII, this difference made file 7 an efficient triage candidate. **UTF-8 by itself does not imply a malicious payload**; the difference simply prioritizes a closer look.

## 3. Inspect the suspicious HTTP request

Read the unusual file and search for opening braces, a useful clue when looking for a flag-like token or embedded payload:

```bash
cat themarvels_logs_7.txt
grep -n '{' themarvels_logs_7.txt
```

The relevant request is a `POST` to `/files/reports`. The captured line also includes unusual non-ASCII characters. Some surrounding text resembles an injection test, but without server responses and application context, it would be incorrect to claim a confirmed SQL injection or XSS vulnerability.

The interesting discovery was **an encoded-looking sequence within the log line**, rather than a proven exploit.

## 4. Identify and decode the encoded text

The characters resemble Unicode Braille symbols. To inspect the sequence:

1. Copy the suspected Braille portion of the request, rather than the entire unrelated HTTP log line.
2. Open [CyberChef](https://gchq.github.io/CyberChef/).
3. Choose the **From Braille** operation.
4. Paste the candidate symbols into the input pane and inspect the output.

The documented decode produced:

```text
MRMARVEL{738CCA09B5ACC1B034CB91C06DFE44A2}
```

**Result:** the recorded flag was recovered by recognizing and decoding Braille-encoded content in the anomalous log file.

The original Unicode payload is not reproduced here because the source log archive was not supplied for this write-up. Accordingly, the flag above is transcribed from the available solution record; this documentation does not claim that a fresh decode of the archive was performed.

## 5. Optional offline triage helper

For future challenges involving a large set of text logs, a small Python helper accompanies this write-up:

```bash
python3 challenges/intrusion-en-sword/scripts/triage_logs.py ./intrusion-sword
```

It performs **read-only** inspection of `*.txt` files, reports non-ASCII content, and prints sequences containing consecutive Unicode Braille characters (`U+2800`–`U+28FF`).

This helper was written to make the methodology reproducible; it is **not** presented as a script used during the original solve. It does not replace the decoding step in CyberChef and has been tested with synthetic inputs, **not with the missing original log archive**.

## Techniques demonstrated

| Skill | Value |
| --- | --- |
| Archive inspection | Establishing a clear set of artifacts before investigating |
| `file` command | Quickly identifying unusual encodings and file types |
| Log analysis and targeted `grep` | Reducing irrelevant output and selecting an anomalous request |
| Encoding recognition | Recognizing that Unicode symbols can represent another text format |
| CyberChef: From Braille | Converting the symbol payload into a readable CTF flag |
| Evidence boundaries | Separating observed suspicious requests from proven application vulnerabilities |

## Lessons learned

- **Prioritize anomalous artifacts.** A single UTF-8 file among primarily ASCII logs was worth investigating first.
- **Do not confuse encoded data with an exploit.** A suspicious HTTP request may contain both attack-looking syntax and a deliberately encoded CTF clue.
- **Confirm assumptions with a reversible transformation.** Recognizing Braille only became useful after a matching decoder returned a coherent flag.
- **Document limitations.** When the original archive is unavailable, clearly distinguish the recorded result from a fresh technical reproduction.

## Artifact and verification notes

- **Challenge:** *Intrusión en S.W.O.R.D.*, TheM4rv3ls CTF (100 points, Web Hacking).
- **Expected original input:** `themarvels_logs.zip`, containing numbered `themarvels_logs_*.txt` files.
- **Recorded result:** the flag above.
- **Independent re-execution against the archive:** not performed for this write-up.
- **Source footage or third-party screenshots:** not included or linked.

*For educational, intentionally scoped CTF use only.*
