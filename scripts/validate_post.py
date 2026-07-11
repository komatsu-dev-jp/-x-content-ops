#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from banned_words import find_flags  # noqa: E402


def main():
    text = sys.stdin.read().strip()
    # Xは改行も1文字としてカウントするため、改行を除去せずに数える。
    flags = find_flags(text)
    print(f"chars: {len(text)}")
    print(f"within_140: {len(text) <= 140}")
    print(f"banned_flags: {flags}")
    if flags or len(text) > 140:
        sys.exit(1)


if __name__ == "__main__":
    main()
