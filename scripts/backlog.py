#!/usr/bin/env python3
"""data/idea_backlog.csv の未消化ネタを管理する。

使い方:
  python3 scripts/backlog.py --status
      未使用/消化済みの件数と、未使用ネタの一覧を表示する。

  python3 scripts/backlog.py --consume "<ideaの前方一致文字列>" post_id=week03-p1
      前方一致（なければ部分一致）で1件だけ未使用ネタを特定し、consumed に変更する。
"""
import csv
import sys
from datetime import date
from pathlib import Path

BACKLOG = Path("data/idea_backlog.csv")
BASE_COLS = ["date", "idea", "source", "theme", "reader_pain", "post_type", "priority", "notes"]
STATUS_COLS = ["status", "consumed_by", "consumed_date"]
COLS = BASE_COLS + STATUS_COLS


def load():
    if not BACKLOG.exists():
        sys.exit(f"{BACKLOG} not found")
    rows = list(csv.DictReader(BACKLOG.open(encoding="utf-8")))
    for r in rows:
        for c in STATUS_COLS:
            r.setdefault(c, "")
        if not r.get("status"):
            r["status"] = "unused"
    return rows


def save(rows):
    with BACKLOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})


def cmd_status(rows):
    unused = [r for r in rows if r["status"] == "unused"]
    consumed = [r for r in rows if r["status"] == "consumed"]
    print(f"unused: {len(unused)} / consumed: {len(consumed)} / total: {len(rows)}")
    if len(unused) < 10:
        print("⚠️ unused<10: x-idea-harvest で15件まで補充する。")
    print()
    for r in unused:
        print(f"- [{r['priority']}] ({r['post_type']}) {r['idea']}")


def cmd_consume(rows, needle, post_id):
    matches = [r for r in rows if r["status"] == "unused" and r["idea"].startswith(needle)]
    if not matches:
        matches = [r for r in rows if r["status"] == "unused" and needle in r["idea"]]
    if not matches:
        sys.exit(f"no unused idea matches: {needle!r}")
    if len(matches) > 1:
        sys.exit(f"ambiguous match ({len(matches)} rows) for: {needle!r}")
    target = matches[0]
    target["status"] = "consumed"
    target["consumed_by"] = post_id
    target["consumed_date"] = date.today().isoformat()
    print(f"consumed: {target['idea']} -> {post_id}")


def main():
    argv = sys.argv[1:]
    rows = load()
    if "--status" in argv:
        cmd_status(rows)
        save(rows)
        return
    if "--consume" in argv:
        idx = argv.index("--consume")
        needle = argv[idx + 1]
        post_id = next(
            (a.split("=", 1)[1] for a in argv[idx + 2:] if a.startswith("post_id=")),
            None,
        )
        if not post_id:
            sys.exit("post_id=... is required")
        cmd_consume(rows, needle, post_id)
        save(rows)
        return
    sys.exit("usage: backlog.py --status | --consume <idea前方一致> post_id=<id>")


if __name__ == "__main__":
    main()
