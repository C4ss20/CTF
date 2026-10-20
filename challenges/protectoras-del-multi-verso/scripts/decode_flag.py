#!/usr/bin/env python3
"""Verify the recorded Base64 payload for TheM4rv3ls CTF.

This standalone script decodes a historical challenge string. It performs
no network requests, authentication, filesystem reads, or exploitation.
"""
from __future__ import annotations

import base64
import binascii

ENCODED = "bXJtYXJ2ZWx7M2JlZTE5MTc5NDg4Mzk3NzBmZDEzNDZmODcyZmUwZjJ9"
EXPECTED = "mrmarvel{3bee1917948839770fd1346f872fe0f2}"


def decode_base64(payload: str) -> str:
    """Decode and validate the input as strict UTF-8 Base64."""
    try:
        return base64.b64decode(payload, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValueError("Invalid Base64 challenge text") from exc


def main() -> None:
    decoded = decode_base64(ENCODED)
    assert decoded == EXPECTED, "Decoded text differs from recorded CTF flag"
    print("Decoded CTF text:", decoded)
    print("Offline Base64 verification passed.")
    print("This does not verify live challenge access.")


if __name__ == "__main__":
    main()
