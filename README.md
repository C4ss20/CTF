# CTF Writeups | Casandra Paulín

A collection of CTF challenges I have solved, documenting the **investigation process**, **technical reasoning**, and **reproducible analysis** behind each flag.

> **Documentation standard:** challenge → observations → hypothesis → validation → outcome → lessons learned. These are controlled CTF exercises, not assessments of production environments.

## Challenges

| Challenge | Event | Topics | Outcome | Write-up |
| --- | --- | --- | --- | --- |
| **Más allá de lo visible** | TheM4rv3ls CTF | OSINT, geolocation, GitHub discovery, encoding and cryptography | Flag verified | [Read walkthrough](challenges/mas-alla-de-lo-visible/README.md) |
| **Intrusión en S.W.O.R.D.** | TheM4rv3ls CTF | Web log forensics, encoding detection, Braille decoding | Flag recovered; original archive not retained | [Read walkthrough](challenges/intrusion-en-sword/README.md) |
| **Protectoras del Multi-Verso** | TheM4rv3ls CTF | WordPress authentication analysis, privilege abuse, server-side execution, Base64 | Flag recovered; historical lab | [Read walkthrough](challenges/protectoras-del-multi-verso/README.md) |
| **Energía Cifrada** | TheM4rv3ls CTF | .NET reverse engineering, PowerShell obfuscation, Base64/Gzip, MD5 and Collatz | Flag independently reproduced offline | [Read walkthrough](challenges/energia-cifrada/README.md) |

## What these write-ups demonstrate

- Correlating clues from public sources and challenge-provided artifacts into testable hypotheses.
- Explaining how each clue supports or rejects a testable hypothesis.
- Distinguishing **encoding**, **encryption**, and plain-text identifiers.
- Providing small, dependency-free Python helpers for repeatable analysis.
- Documenting verification methods and any gaps in retained proof transparently.

## Documentation and verification

I solved the challenges documented in this repository. Some original session screenshots or terminal captures were not retained, so these write-ups reconstruct the investigation steps instead of presenting a complete contemporaneous evidence log.

Where possible, challenge details, flags, and decoding steps are rechecked against public CTF materials or with reproducible local scripts. These references **validate the explanation**, but do not serve as independent proof of my original solve. I do not present anyone else's screenshots or recordings as my own.

The original challenge materials belong to their creators. The challenge archives and source screenshots are not redistributed here.

## Future challenges

More write-ups from the same CTF will be added as their details are documented and verified.

## Repository layout

```text
CTF/
├── README.md
└── challenges/
    ├── mas-alla-de-lo-visible/
    │   ├── README.md
    │   └── scripts/
    │       └── decode_clues.py
    ├── intrusion-en-sword/
    │   ├── README.md
    │   └── scripts/
    │       └── triage_logs.py
    ├── protectoras-del-multi-verso/
    │   ├── README.md
    │   └── scripts/
    │       └── decode_flag.py
    └── energia-cifrada/
        ├── README.md
        └── scripts/
            └── recover_flag.py
```

The destination repository may contain unrelated files outside this documentation tree; these write-ups do not modify or remove them.