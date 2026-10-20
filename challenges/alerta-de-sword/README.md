# Alerta de S.W.O.R.D. — TheM4rv3ls CTF

**Category:** Traffic Analysis / Network Forensics · **Points:** 60 · **Techniques:** PCAP examination, Wireshark HTTP object extraction, archive analysis, password recovery

> **Documentation note:** I completed this CTF challenge, but I did not retain a complete set of original session evidence. This is a retrospective account of the investigation. The original `KreeTransmition.zip`, packet capture, and recovered `SwordDefense.zip` have **not** been provided for independent re-analysis. The flag is transcribed from the available end-result record; extraction, password recovery, and challenge submission were **not rerun** for this write-up. No third-party recordings or screenshots are included or linked.

## Challenge objective

S.W.O.R.D. intercepted traffic following an apparent leak of confidential research. The challenge provides an archive containing a packet capture and indicates that **one transferred file contains an important clue**, while other traffic is meant to distract analysts.

The goal is to inspect the network traffic, locate the relevant artifact, recover its contents, and submit the flag.

## Investigation summary

| Stage | Observation | Why it matters |
| --- | --- | --- |
| Archive triage | `KreeTransmition.zip` contains `KreeTransmition.pcapng` | Establishes a network-capture investigation |
| Packet inspection | Large capture with TCP, TLS, DNS, and HTTP traffic | Motivates narrowing the analysis instead of reviewing all packets individually |
| HTTP object export | Transferred object named `SwordDefense.zip` (289 bytes in the recorded object list) | Produces a candidate file from the capture |
| Archive inspection | `SwordDefense.zip` is password protected using AES ZIP encryption | The content cannot simply be read without the password |
| Password recovery | ZIP hash extracted with `zip2john`, then checked using John the Ripper and a wordlist | Recovers the challenge archive password |
| Artifact extraction | Encrypted archive contains `flag.txt` | Recovers the flag text |

## 1. Identify and extract the PCAP

First, inspect the downloaded artifact without assuming its type:

```bash
file KreeTransmition.zip
unzip -l KreeTransmition.zip
unzip KreeTransmition.zip
```

The recorded extraction yields:

```text
KreeTransmition.pcapng
```

Open the capture in Wireshark:

```bash
wireshark KreeTransmition.pcapng
```

The large capture contains several protocols, including TCP, TLS, DNS, and HTTP. Many TLS packets carry encrypted application data. Their presence alone does **not** permit reconstructing protected HTTPS content or prove data exfiltration.

## 2. Search transferred HTTP objects in Wireshark

Instead of examining every individual packet, inspect the transfer artifacts:

```text
Wireshark → File → Export Objects → HTTP
```

The recorded HTTP object list included spreadsheets and other transferred resources. One particularly relevant entry was:

```text
Filename: SwordDefense.zip
Content type: application/zip
Size: 289 bytes
```

Export `SwordDefense.zip` to the analysis working directory. The point of this step is to reconstruct an **HTTP-transferred file from the capture**, not to download or alter a current external service.

**Forensic reasoning:** A small archive whose name matches the S.W.O.R.D. theme deserves inspection, but the filename alone is only a hypothesis. Its encrypted contents must still be examined.

## 3. Determine whether the ZIP is encrypted

Inspect the recovered archive before extraction:

```bash
file SwordDefense.zip
7z l SwordDefense.zip
```

The recorded `file` output identifies a ZIP archive using **AES encryption**. Attempting extraction with `7z x SwordDefense.zip` prompts for a password.

The repository includes a read-only helper to inspect standard ZIP central-directory metadata (member names, sizes, encryption flags, and compression method):

```bash
python3 challenges/alerta-de-sword/scripts/inspect_zip.py SwordDefense.zip
```

The helper intentionally does **not** attempt to decrypt, crack, or extract any member. It was developed for documentation and tested on synthetic ZIP data, not on the unavailable original CTF artifact.

## 4. Recover the challenge ZIP password

To prepare a ZIP password hash representation in the isolated CTF environment, use **`zip2john`**:

```bash
zip2john SwordDefense.zip > zip_hashes.txt
```

Then test candidates using **John the Ripper** and the local wordlist:

```bash
john --format=zip --wordlist=/usr/share/wordlists/rockyou.txt zip_hashes.txt
john --format=zip --show zip_hashes.txt
```

John versions vary in available ZIP formats and auto-detection behavior. The historical session used the ZIP format and reported:

```text
jupiter
```

**Recovered archive password:** `jupiter` (lowercase).

The `zip2john` output is an attackable representation of ZIP encryption verification data; it is **not the plaintext password** and does not mean the archive used unsalted MD5 or another simple password hash.

**Scope:** This password-recovery method was applied to a CTF-provided, intentionally encrypted archive. It is not a claim about any third-party account, password, or live network service.

## 5. Extract the flag

Once the password is known, extract the archive in a local analysis directory:

```bash
7z x SwordDefense.zip
```

Enter the recovered password when prompted. The recorded archive contained `flag.txt`. Read the file:

```bash
cat flag.txt
```

**Recorded flag:**

```text
MrMarvel{5dd0777bd0a0111d1132749d0ef8409b}
```

This flag was transcribed from the documented final terminal output. It has a correctly structured 32-character hexadecimal body, but the missing original archive means the extraction cannot be independently reproduced here.

## Tools used

| Tool | Role |
| --- | --- |
| `file`, `unzip` | Recognize and inventory the supplied archive |
| Wireshark | Analyze the capture and export HTTP-transferred objects |
| `7z` | Inspect and extract encrypted ZIP members |
| `zip2john` | Convert the encrypted ZIP into a format suitable for password testing |
| John the Ripper / `rockyou.txt` | Recover the challenge archive's password from candidate guesses |
| Python `zipfile` | Optional, read-only local metadata triage |

## Security lessons and limitations

1. **Reassemble transferred artifacts.** Wireshark's HTTP object export can reveal files more efficiently than manually inspecting thousands of packets.
2. **Keep protocol claims precise.** TLS traffic is encrypted; the presence of TLS packets does not establish the contents of a transfer.
3. **Treat encrypted artifacts as leads, not conclusions.** Identifying an AES-encrypted ZIP is separate from recovering its password and validating its contents.
4. **Distinguish ZIP password recovery from server compromise.** The work targeted an offline file deliberately supplied for the CTF, not live authentication.
5. **Maintain evidence boundaries.** The commands describe the reconstructed workflow; the original capture and archive were not available for independent verification during publication.

## Artifacts and reproducibility

- **Original challenge archive:** `KreeTransmition.zip` — not retained in this repository.
- **Captured network file:** `KreeTransmition.pcapng` — not retained.
- **Exported HTTP object:** `SwordDefense.zip` — not retained.
- **Recovered member:** `flag.txt` — result transcribed above.
- **Independently verifiable:** Python metadata helper can be tested against a user-supplied ZIP; it does not validate this historical extraction.

*Educational documentation of an authorized, historical capture-the-flag exercise only.*
