# CTF writeup methodology

This is a **documentation standard**, not a claim that every technique below was used on the original CTF.

## 1. Define authorized scope

Document the original event/platform, lab environment, challenge objective, and any relevant usage or disclosure rules. Do not repurpose the instructions against real systems.

## 2. Separate observation from hypothesis

Write down exactly what was observed, then what it might imply. Do not treat an inference as a confirmed finding.

| Field | Meaning |
|---|---|
| Observation | Verifiable fact, response, output, or artifact |
| Hypothesis | Explanation that could account for the observation |
| Test | Reproducible action that can confirm or challenge the hypothesis |
| Result | What actually happened, including unexpected outcomes |
| Conclusion | Claim supported by the test and its evidence |

## 3. Document tests

For every important command or code fragment, provide purpose, sanitized syntax, expected behavior, observed behavior, and interpretation. Use small relevant output excerpts rather than uploading huge logs.

## 4. Validate

Link each conclusion to a reproducible result, screenshot, or log excerpt. Describe uncertainty and note failed tests when they changed your approach.

## 5. Explain defensive significance

When meaningful, cover affected component, weakness, prerequisites, impact, mitigation, monitoring, and retesting. If the CTF is a puzzle rather than an actual vulnerability, describe the skill learned; do not invent a CVE or severity score.

## 6. Publish carefully

Use the challenge template, redact secrets, credit all external walkthroughs, and mark the writeup Verified only after reviewing your original notes or repeating the authorized test.
