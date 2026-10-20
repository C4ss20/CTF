#!/usr/bin/env python3
"""Read-only ZIP metadata inspection helper for a network-forensics CTF.

Does not extract, decrypt, execute, or modify archive contents.
Original SwordDefense.zip was not available when this script was created.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


def inspect(path: Path) -> int:
    if not path.is_file():
        print(f"File does not exist: {path}", file=sys.stderr)
        return 2

    try:
        with zipfile.ZipFile(path, "r") as archive:
            members = archive.infolist()
            print(f"Archive: {path.name}")
            print(f"Members: {len(members)}")
            for info in members:
                encrypted = bool(info.flag_bits & 0x1)
                compression = info.compress_type
                print(f"\nName: {info.filename}")
                print(f"  Uncompressed bytes: {info.file_size}")
                print(f"  Compressed bytes: {info.compress_size}")
                print(f"  Encrypted flag: {encrypted}")
                print(f"  ZIP compression method: {compression}")
                if compression == 99:
                    print("  Method 99 can indicate WinZip AES encryption.")
            return 0
    except (zipfile.BadZipFile, OSError, ValueError) as exc:
        print(f"Cannot inspect ZIP archive: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Path to a ZIP file to inspect")
    return inspect(parser.parse_args().archive)


if __name__ == "__main__":
    raise SystemExit(main())
