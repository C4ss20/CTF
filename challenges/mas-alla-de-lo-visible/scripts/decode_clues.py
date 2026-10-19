#!/usr/bin/env python3
"""Reproduce the bonus clues from TheM4rv3ls CTF's public Pistas README.

No third-party dependencies, network access, or account logins are used.
Documentation: ../README.md
"""

from __future__ import annotations

import base64

INTERCEPTED = "=0zZzkFdax2V0oEVXZEbUJFbO5WUVRmVNNEasVVVo1WTahWRjdlRxQ1TaZlV"
MORSE = "-.-. .- .-. --- .-.. -.. .- -. ...- . .-. ..."
KEY = "PHOTON"
MORSE_ALPHABET = {
    "-.-.": "C", ".-": "A", ".-.": "R", "---": "O", ".-..": "L",
    "-..": "D", "-.": "N", "...-": "V", ".": "E", "...": "S",
}


def decode_base64_layers(text: str, layers: int = 4) -> list[str]:
    """Reverse the initial payload and return each decoded Base64 layer."""
    current = text[::-1]
    intermediates: list[str] = []
    for _ in range(layers):
        current = base64.b64decode(current, validate=True).decode("utf-8")
        intermediates.append(current)
    return intermediates


def decrypt_vigenere(text: str, key: str) -> str:
    """Decrypt letters, preserving punctuation/digits and the input letter case."""
    key_letters = [ord(c.upper()) - ord("A") for c in key if c.isascii() and c.isalpha()]
    if not key_letters:
        raise ValueError("A Vigenère key needs at least one ASCII letter")

    out: list[str] = []
    key_idx = 0
    for character in text:
        if ("A" <= character <= "Z") or ("a" <= character <= "z"):
            base = ord("A") if character.isupper() else ord("a")
            shift = key_letters[key_idx % len(key_letters)]
            out.append(chr((ord(character) - base - shift) % 26 + base))
            key_idx += 1
        else:
            out.append(character)
    return "".join(out)


def decode_morse(message: str) -> str:
    """Decode the supported Morse letters supplied by this particular puzzle."""
    return "".join(MORSE_ALPHABET[symbol] for symbol in message.split())


def main() -> None:
    intermediate = decode_base64_layers(INTERCEPTED)
    print("Reversed Base64 input, four decoding layers:")
    for index, value in enumerate(intermediate, start=1):
        print(f"  Layer {index}: {value}")

    password_candidate = decrypt_vigenere(intermediate[-1], KEY)
    raw_user = decode_morse(MORSE)
    user_candidate = raw_user.title().replace(" ", "")  # 'CarolDanvers' needs a manual name boundary.
    user_candidate = "CarolDanvers" if raw_user == "CAROLDANVERS" else user_candidate

    assert intermediate[-1] == "A#@dg!HJncIq87%aX5"
    assert password_candidate == "L#@ws!OVanBc87%hJ5"
    assert raw_user == "CAROLDANVERS"

    print(f"\nVigenère key: {KEY}")
    print(f"Password candidate: {password_candidate}")
    print(f"Morse result: {raw_user}")
    print(f"Username candidate (case inferred from clue): {user_candidate}")
    print("\nChecks passed. No live login performed.")


if __name__ == "__main__":
    main()