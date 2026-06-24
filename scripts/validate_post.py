#!/usr/bin/env python3
import sys

BANNED = [
    "絶対勝てる", "勝率爆上げ", "誰でも稼げる", "必勝", "攻略法", "爆益", "最強", "革命",
    "人生変わる", "勝ち組", "稼げる", "確実に勝てる"
]

def main():
    text = sys.stdin.read().strip()
    compact = text.replace("\n", "")
    flags = [w for w in BANNED if w in text]
    print(f"chars_no_newline: {len(compact)}")
    print(f"within_140: {len(compact) <= 140}")
    print(f"banned_flags: {flags}")
    if flags or len(compact) > 140:
        sys.exit(1)

if __name__ == "__main__":
    main()
