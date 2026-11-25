#!/usr/bin/env python3
"""Museum of the Year 3000 — museum label entry.

Writes one line (1-200 chars, UTF-8, no trailing newline) to entry.txt
in MAKEFUN_OUTPUT_DIR or /output, with a local output/ fallback.
Pure Python standard library only.
"""

import os
import sys

LINE = (
    "Parking Meter, c. 2025: citizens fed this iron box coins to rent "
    "the patch of ground beneath their car, then hurried back before "
    "its patience ran out."
)


def main():
    line = LINE
    if not line or not line.strip():
        print("error: line is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if len(line) > 200:
        print(f"error: line is {len(line)} chars, over the 200-char limit",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "output")
        os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "entry.txt")
    old_umask = os.umask(0o022)
    try:
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        os.chmod(out_path, 0o644)
    finally:
        os.umask(old_umask)

    print(f"wrote {out_path} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
