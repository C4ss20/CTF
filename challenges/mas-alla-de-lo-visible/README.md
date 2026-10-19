# Más allá de lo visible — TheM4rv3ls CTF

**70 points** · **OSINT / Geolocation / GitHub Discovery** · **Bonus: Encoding and Classical Cryptography**

> **Spoiler warning:** this document contains the flag and the decoded credentials for a *separate follow-up puzzle*.
>
> **Documentation note:** I solved this CTF challenge but did not retain a complete set of screenshots from my original session. This is a reconstructed write-up, with challenge facts and the flag checked against the [original public CTF repository](https://github.com/DarthAshmed/11-07-2023-Toronto). Those public materials validate the technical details, not my personal completion history.

## Objective

Track interdimensional anomalies across publicly accessible websites and social media, correlate their clues, and locate the hidden CTF flag.

## Investigation summary

| Source | Observation | How it contributes |
| --- | --- | --- |
| Instagram `@anomalies_tracker`, post 1 | `Photon` | Encryption key for an additional puzzle |
| Instagram, post 2 | `43°40′13″N 79°23′12″W` | Location resolves to Toronto, Canada |
| Instagram, post 3 | `11/07/2023` | Date used to construct a repository name |
| Instagram story highlight | `github.com/DarthAshmed/***-***-20***-T****o` | Identifies the account and gives a repository pattern |
| GitHub repository README | `MrMarvel{...}` | Flag for **this** challenge |
| GitHub `Pistas/README.md` | Encoded strings | Optional pivot into a later challenge, not required for this flag |

## 1. Open-source reconnaissance: Instagram

The challenge description directs the investigator to the public Instagram account [`anomalies_tracker`](https://www.instagram.com/anomalies_tracker/). The challenge's Instagram clues consist of three posts and a story highlight named *pista*.

### 1.1 Extract a keyword

The first post states that access to the archives requires the secret key **`Photon`**. Record its exact spelling and capitalization for potential decryption work.

### 1.2 Identify coordinates

The second post gives the last reported signal for Carol as:

```text
43°40'13"N 79°23'12"W
```

Plotting these coordinates using a public mapping service places the location in **Toronto, Canada**. This supplies the geographical component of the later repository name.

### 1.3 Identify the date

The third post mentions anomalies in Hala and displays **`11/07/2023`**. In combination with the masked GitHub pattern, the repository uses the date as **`11-07-2023`**. The month/day interpretation is not necessary; the critical detail is the literal date ordering reproduced in the repository name.

### 1.4 Investigate the story highlight

The highlight *pista* provides a partially masked GitHub URL tied to the username `DarthAshmed`:

```text
https://github.com/DarthAshmed/***-***-20***-T****o
```

The prompt also indicates that part of the address is missing and that the images can help reconstruct it.

**Working hypothesis:** the hidden repository name combines the observed date and location.

## 2. Correlate clues to discover the repository

Combine the independently obtained pieces:

```text
11/07/2023       → 11-07-2023
Toronto          → Toronto
GitHub account   → DarthAshmed

Repository       → 11-07-2023-Toronto
```

The resulting URL is:

**[github.com/DarthAshmed/11-07-2023-Toronto](https://github.com/DarthAshmed/11-07-2023-Toronto)**

This candidate is testable: visiting the repository reveals a README with the same challenge title, *Más allá de lo visible*. That title match confirms that the repository is not merely a coincidental naming match.

## 3. Retrieve and validate the flag

The [repository's root `README.md`](https://github.com/DarthAshmed/11-07-2023-Toronto/blob/main/README.md) contains a congratulatory message and the challenge flag.

```text
MrMarvel{aed5fe6c0a87d4e403b14c0c888ea199}
```

**Result:** the flag was verified directly in the original public repository README. No brute force, account login, or exploitation was needed to solve this OSINT challenge.

---

## Bonus: Intercepted transmission and the next challenge

**Important scope distinction:** the flag above completes *Más allá de lo visible*. The repository's [`Pistas/README.md`](https://github.com/DarthAshmed/11-07-2023-Toronto/blob/main/Pistas/README.md) contains an additional challenge that leads toward a later WordPress puzzle. The following decoding steps are useful cryptography practice, but are **not necessary** for the 70-point flag.

### 4.1 Reverse and repeatedly decode Base64

The intercepted string in the original `Pistas/README.md` is:

```text
=0zZzkFdax2V0oEVXZEbUJFbO5WUVRmVNNEasVVVo1WTahWRjdlRxQ1TaZlV
```

The initial `=` is suspicious: Base64 padding belongs at the **end**, not the beginning. Reverse the entire string, then apply standard Base64 decoding **four times**:

```text
reverse(text)
  ↓
Base64 decode × 4
  ↓
A#@dg!HJncIq87%aX5
```

The output is not the final password. The challenge's hint says to reuse the key found at the beginning of the investigation for a **Vigenère cipher**. Apply Vigenère decryption to alphabetic characters using `PHOTON`, leaving punctuation and digits unchanged.

The resulting **candidate password** is:

```text
L#@ws!OVanBc87%hJ5
```

*Terminology note:* Base64 is an **encoding**, not encryption. Vigenère is the encryption step. When reconstructing the CyberChef recipe, letter case and operation order matter.

### 4.2 Decode Morse code to obtain the username

The second intercepted message is:

```text
-.-. .- .-. --- .-.. -.. .- -. ...- . .-. ...
```

Morse decoding yields:

```text
CAROLDANVERS
```

The puzzle says the username has **two uppercase letters**, with the remainder lowercase. A plausible normalization is **`CarolDanvers`** (capital C and D). This is a **candidate username**; no subsequent WordPress login was independently verified in this write-up.

### 4.3 Reproduce the transformations in Python

A dependency-free script accompanies this write-up:

```bash
python3 challenges/mas-alla-de-lo-visible/scripts/decode_clues.py
```

It prints all four Base64 intermediate stages, the Vigenère result, the Morse decode, and the inferred capitalization. It also asserts the expected outputs for the puzzle strings.

## Tools and concepts

| Tool or technique | Purpose |
| --- | --- |
| Public Instagram posts and story highlights | Extract usernames, dates, coordinates, and hints |
| Geographic coordinates / mapping | Turn a coordinate pair into a location hypothesis |
| GitHub browsing | Validate a repository-name hypothesis and identify the flag |
| [CyberChef](https://gchq.github.io/CyberChef/) | Explore reversing, Base64, Vigenère, and Morse transforms |
| Python 3 standard library | Reproduce and check the decoding chain |

## Lessons learned

1. **Treat public content as evidence.** Several seemingly unrelated sources supplied pieces of one exact URL.
2. **Build testable hypotheses.** A masked repository path can be inferred from independent location and date clues, then validated against the page title.
3. **Separate the goal from adjacent findings.** Discovering the flag completed this challenge; the intercepted transmission belonged to the next stage.
4. **Decode in the right order.** A leading Base64 padding character was a useful sign that the string had been reversed, while repeated layers concealed the Vigenère ciphertext.
5. **Label confidence correctly.** The flag was directly confirmed. The inferred follow-up login credentials were decoded but not tested here.

## References and documentation limits

- [Original CTF repository](https://github.com/DarthAshmed/11-07-2023-Toronto) — repository name, challenge title, and flag.
- [Original bonus puzzle README](https://github.com/DarthAshmed/11-07-2023-Toronto/blob/main/Pistas/README.md) — encoded messages and cipher hint.

I completed this challenge, but my original screenshot evidence is incomplete. The steps above explain the solution and can be followed or checked against the public CTF resources. Public challenge pages are used as references, **not as proof of my personal solve**. No third-party screenshots or recordings are included.

*Educational use only. The documented activity concerns intentionally public CTF assets.*
