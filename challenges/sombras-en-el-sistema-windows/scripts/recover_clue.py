#!/usr/bin/env python3
"""Offline CTF decode: reverse, four Base64 layers, then hash the clue.

No network requests, subprocesses, archive extraction, or evidence mutation.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import re

ENCODED_FIELD = (
    "==QNBRkVWFzRkRnWGN1SkBTWIZEVihVMX50dwATYhVzVWBDcwIla01mUVBHbO9m"
    "TqZFawtWYUxmRiNnUxM1batmV"
)
EXPECTED_MESSAGE = "MrMarvels{Windows_failed}"
EXPECTED_CLUE = "Windows_failed"
EXPECTED_MD5 = "b209b6f2713d454c1273f2b5b702708a"


def decode_field(value: str) -> str:
    data = value[::-1].encode("ascii")
    for layer in range(1, 5):
        try:
            data = base64.b64decode(data, validate=True)
        except binascii.Error as exc:
            raise ValueError(f"Invalid Base64 at layer {layer}") from exc
    return data.decode("utf-8")


def main() -> None:
    message = decode_field(ENCODED_FIELD)
    match = re.fullmatch(r"MrMarvels\{([^{}]+)\}", message)
    if not match:
        raise ValueError("Unexpected decoded wrapper")
    clue = match.group(1)
    digest = hashlib.md5(clue.encode("utf-8")).hexdigest()
    assert message == EXPECTED_MESSAGE
    assert clue == EXPECTED_CLUE
    assert digest == EXPECTED_MD5
    print(f"Decoded message: {message}")
    print(f"Identifier: {clue}")
    print(f"MD5: {digest}")
    print("Verified: reverse + 4 Base64 layers + MD5.")


if __name__ == "__main__":
    main()
