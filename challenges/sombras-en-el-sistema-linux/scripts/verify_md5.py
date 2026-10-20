#!/usr/bin/env python3
"""Verify the reconstructed MD5 answer for a historical CTF challenge.

Offline calculation only. No evidence archive, login, or executable is accessed.
"""
from __future__ import annotations

import hashlib

CLUE = "skrull_backdoor"
EXPECTED_DIGEST = "9de9a032343dbf5f749c93304e962f90"


def md5_hex(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def main() -> None:
    result = md5_hex(CLUE)
    assert result == EXPECTED_DIGEST, "Unexpected MD5 digest"
    print(f"Candidate key: {CLUE}")
    print(f"MD5: {result}")
    print("Offline verification passed.")


if __name__ == "__main__":
    main()
