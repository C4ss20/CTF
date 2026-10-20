#!/usr/bin/env python3
"""Reconstruct the final flag derivation from the CTF's decompiled C# logic.

Safe offline analysis only: never loads, extracts, or executes the challenge EXE.
"""

from __future__ import annotations

import hashlib

SEED = "72b83d5b4716e40bece9c566a5f4fa6b"
START = 1500
EXPECTED = "Ms.Marvel{9bb8e66ac13f32b07488c3dddbe20b49}"


def recover_flag(seed: str = SEED, starting_number: int = START) -> tuple[str, int]:
    if starting_number < 1:
        raise ValueError("The start value must be positive")

    value = seed
    number = starting_number
    steps = 0
    while True:
        value = hashlib.md5(f"{value}{number}".encode("ascii")).hexdigest()
        steps += 1
        if number <= 1:
            break
        number = number // 2 if number % 2 == 0 else 3 * number + 1

    return f"Ms.Marvel{{{value}}}", steps


def main() -> None:
    flag, steps = recover_flag()
    print(f"Starting integer: {START}")
    print(f"MD5 updates: {steps}")
    print(f"Recovered flag: {flag}")
    assert flag == EXPECTED, "Reconstructed algorithm produced an unexpected value"
    assert steps == 48
    print("Verified: expected flag matches the offline reconstruction.")


if __name__ == "__main__":
    main()
