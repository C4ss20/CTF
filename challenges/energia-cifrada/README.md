# Energía Cifrada — TheM4rv3ls CTF

**Category:** Reversing · **Points:** 250 · **Target:** Windows/.NET executable · **Methods:** static inspection, layered-encoding analysis, C# logic reconstruction, Python verification

> **Documentation scope:** This is a retrospective write-up of a completed CTF challenge. The included Python script is a clean-room reconstruction of the flag-generation logic shown in decompiled code, not a copy of the executable. The existing CTF archive was checked for its ZIP structure, but the executable was **not executed** and the complete binary was **not independently decompiled** again for this write-up. Original screenshots and terminal recordings from my solve are incomplete; no third-party video links or screenshots are used as proof.

## Objective

An anomaly in the electromagnetic spectrum conceals a critical message. The challenge provides an archive named `tomar_decision.zip`; the goal is to analyze its layers and recover a hidden flag.

The archive is retained as an **untrusted challenge artifact** at [`../../tomar_decision.zip`](../../tomar_decision.zip). It can trigger malware detection because its content contains PowerShell-execution and embedded executable-loading behavior. Do **not** run the sample on a personal or production computer. Use an isolated analysis VM if binary inspection is necessary.

## 1. Triage the artifact without executing it

Begin with a file inventory:

```bash
unzip -l tomar_decision.zip
file tomar_decision.zip
```

The archive contents were checked against the repository's copy:

| File | Original size | Comment |
| --- | ---: | --- |
| `tomar_decision.exe` | 14,848 bytes | One executable stored inside the ZIP |

The executable was identified as a managed .NET/Mono program in the challenge analysis. This is useful because managed C# assemblies often retain high-level metadata and can be inspected through a tool such as **ILSpy**, without launching the executable.

## 2. Inspect the initial managed assembly

In the decompiled `Program.Main` method, a long Base64 string is decoded to UTF-8 text. The code then uses the .NET PowerShell automation APIs, including a `Runspace` and `PowerShell.Create()`, to pass that decoded text to `AddScript()` and `Invoke()`.

This pattern suggests a script launcher:

```text
.NET executable
    └─ Base64 string
        └─ decoded PowerShell source
            └─ dynamically invoked through a PowerShell runspace
```

**Analyst interpretation:** This is a suspicious loader pattern, not a reason to execute the sample. Base64 is an encoding mechanism; it is not encryption.

The Base64 string can be decoded as data using a separate offline utility or CyberChef's `From Base64` operation. The decoded text was a PowerShell script.

## 3. Identify the second encoded layer

Analysis of the PowerShell text showed a second variable named `$gzipB64`. It contained another encoded payload. The relevant data-processing chain was:

```text
$gzipB64 string
    └─ Base64 decode
        └─ Gzip decompress
            └─ Windows PE executable (starts with MZ)
```

The decoded output showed the `MZ` signature associated with a Windows Portable Executable file. In the historical investigation, this stage was saved under the analyst-chosen name `virus.exe` for further static inspection. The name itself is not a malware-family identification.

**Safety boundary:** Inspecting the extracted bytes or decompiling the nested assembly is different from executing them. This repository does not include a runnable loader or decrypted second-stage binary.

## 4. Reconstruct the flag-building routine

In the second .NET assembly, the decompiled `MrMarvel.Program` class contained the relevant flag logic. The flag builder used:

- A fixed initial hex string: `72b83d5b4716e40bece9c566a5f4fa6b`
- A starting integer of **1500**
- An MD5 hash applied at **every iteration** to the concatenation of the current hex string and the current integer
- A Collatz-style integer update: **even → n / 2**, **odd → 3n + 1**
- A stopping rule after hashing the integer **1**
- The CTF flag wrapper `Ms.Marvel{...}`

The decompiled method's meaning can be expressed as pseudocode:

```text
digest = "72b83d5b4716e40bece9c566a5f4fa6b"
n = 1500

repeat:
    digest = md5_hex_ascii(digest + decimal_string(n))
    if n <= 1:
        break
    if n is even:
        n = n / 2
    else:
        n = 3 * n + 1

flag = "Ms.Marvel{" + digest + "}"
```

**Important implementation detail:** The digest is updated **before** the stopping condition. Omitting the final MD5 update when `n == 1` produces the wrong flag. Hash text is lower-case hex, and the source algorithm uses ASCII bytes for the input string.

The obfuscated C# identifiers do not carry meaningful semantics. The core is a deterministic hash state machine using a Collatz sequence.

## 5. Recover and verify the flag safely in Python

A standalone Python 3 implementation is provided at [`scripts/recover_flag.py`](scripts/recover_flag.py).

Run it without extracting or executing the Windows executable:

```bash
python3 challenges/energia-cifrada/scripts/recover_flag.py
```

**Verified offline output:**

```text
Starting integer: 1500
MD5 updates: 48
Recovered flag: Ms.Marvel{9bb8e66ac13f32b07488c3dddbe20b49}
Verified: expected flag matches the offline reconstruction.
```

The result is reproducible from the decompiled constants and algorithm. The script uses only the standard-library `hashlib` module and makes **no network connections** or calls to the executable.

## Findings and interpretation

| Finding | What it demonstrates |
| --- | --- |
| Managed .NET/Mono executable | Opportunity for static review with ILSpy |
| Embedded Base64 script | Encoded content can conceal PowerShell actions |
| PowerShell runspace invocation | Decoded script is intended for dynamic execution |
| Second Base64 + Gzip layer | A nested binary concealed by compression and encoding |
| `MZ` header after decompression | Evidence of embedded Portable Executable content |
| Decompiled MD5/Collatz routine | Algorithm reconstruction can recover a flag without running unknown code |

## Lessons learned

1. **Avoid executing unknown challenge binaries.** Start with an archive listing, file identification, and static decompilation.
2. **Treat encodings as layers, not encryption.** Base64 and Gzip can obscure payload structure without protecting its content cryptographically.
3. **Follow data flow across stages.** The first assembly serves as a loader; the nested assembly contains the flag-generating logic.
4. **Pay attention to operation ordering.** Hashing before the stopping condition changes the final MD5 digest.
5. **Reimplement only the algorithm you need.** Reconstructing the C# logic in safe Python avoided executing the suspected loader.
6. **Separate confirmation levels.** The archive listing and reconstructed flag computation were checked offline; the full original executable was not independently reanalyzed in this publication.

## Tools and techniques

`unzip` · `file` · ILSpy · CyberChef · .NET/C# static analysis · PowerShell code inspection · Python 3 · `hashlib.md5`

*For controlled CTF and educational reverse-engineering analysis only. Do not deploy or execute unknown PE files from the archive.*
