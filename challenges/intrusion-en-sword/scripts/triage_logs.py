#!/usr/bin/env python3
"""Offline triage helper for text logs in a CTF archive.

Lists non-ASCII and Braille-bearing lines without modifying input files.
This is a reconstruction helper, not the original solve artifact.
"""

import argparse
import re
from pathlib import Path

BRAILLE = re.compile(r"[\u2800-\u28ff]{2,}")


def inspect(path: Path) -> tuple[int, int]:
    content = path.read_text(encoding="utf-8", errors="replace")
    unusual = 0
    braille_lines = 0
    for lineno, line in enumerate(content.splitlines(), start=1):
        unusual += any(ord(char) > 127 for char in line)
        sequences = BRAILLE.findall(line)
        if sequences:
            braille_lines += 1
            for sequence in sequences:
                print(f"{path.name}:{lineno}: {sequence}")
    if unusual:
        print(f"{path.name}: {unusual} lines contain non-ASCII characters")
    return unusual, braille_lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Directory with extracted *.txt challenge logs")
    args = parser.parse_args()
    if not args.folder.is_dir():
        parser.error(f"Not a directory: {args.folder}")
    paths = sorted(args.folder.glob("*.txt"))
    if not paths:
        parser.error("No .txt log files found")
    print(f"Inspecting {len(paths)} files (read-only)")
    results = [inspect(path) for path in paths]
    print(f"Files with non-ASCII content: {sum(bool(n) for n, _ in results)}")
    print(f"Files with Braille sequences: {sum(bool(b) for _, b in results)}")
    print("Use CyberChef's 'From Braille' operation on any candidate sequence.")


if __name__ == "__main__":
    main()
