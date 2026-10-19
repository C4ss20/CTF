# CTF Writeups | Casandra Paulín

A collection of structured capture-the-flag walkthroughs, focused on the **evidence**, **reasoning**, and **reproducibility** behind each finding.

> **Documentation standard:** challenge → observations → hypothesis → validation → outcome → lessons learned. These are controlled CTF exercises, not assessments of production environments.

## Challenges

| Challenge | Event | Topics | Outcome | Write-up |
| --- | --- | --- | --- | --- |
| **Más allá de lo visible** | TheM4rv3ls CTF | OSINT, geolocation, GitHub discovery, encoding and cryptography | Flag verified | [Read walkthrough](challenges/mas-alla-de-lo-visible/README.md) |

## What these write-ups demonstrate

- Correlating publicly available clues into testable hypotheses.
- Maintaining an evidence trail instead of treating guesses as findings.
- Distinguishing **encoding**, **encryption**, and plain-text identifiers.
- Reproducing transformations with short, dependency-free Python scripts.
- Documenting source material and limitations transparently.

## Evidence & attribution

The first challenge was **reconstructed from user-provided screenshots and a public video tutorial**, then cross-checked against the challenge's original public GitHub resources. The referenced tutorial footage shows the walkthrough rather than a newly executed lab session. Visual evidence links point to the relevant moments in that recording. This distinction is intentional; it avoids attributing another person's actions to the repository owner.

- [Tutorial video](https://www.youtube.com/watch?v=zk36oU2tL-Q&list=PLDo9DMLZyP6ki_F4Jv4NTOjFOnYHGon0y&index=2)
- [Original challenge repository](https://github.com/DarthAshmed/11-07-2023-Toronto)

Only intentionally public CTF assets were used for this documentation. The source challenge and footage remain the property of their respective creators; reproduction of stills here is for analysis and commentary with attribution.

## Repository layout

```text
CTF/
├── README.md
└── challenges/
    └── mas-alla-de-lo-visible/
        ├── README.md
        ├── evidence/
        │   └── README.md
        └── scripts/
            └── decode_clues.py
```

The destination repository may contain unrelated files outside this documentation tree; these write-ups do not modify or remove them.