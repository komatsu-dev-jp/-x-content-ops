#!/usr/bin/env python3
"""data/idea_backlog.csv の在庫確認・消化印つけ（追加課金なし・ローカルCSVのみ）。

backlog は「溜める→使う→補充」を回して初めて機能する。
このスクリプトは status（未使用/投稿済）の棚卸しと消化印つけを担う。
補充（新ネタ生成）は x-idea-harvest Skill が行う。

使い方:
  # 在庫確認（未使用が10件を切っていたら補充サインを出す）
  python3 scripts/idea_backlog.py --status

  # 使ったネタに投稿済の印をつける（idea前方一致 or 完全一致）
  python3 scripts/idea_backlog.py --consume "勝った日の記憶" post_id=week02-p1
"""
import csv
import sys
from pathlib import Path

LOG = Path("data/idea_backlog.csv")
FIELDS = ["date", "idea", "source", "theme", "reader_pain",
          "post_type", "priority", "status", "notes"]
LOW_WATER = 10  # 未使用がこれを下回ったら補充


def load():
    if not LOG.exists():
        sys.exit(f"{LOG} not found")
    return list(csv.DictReader(LOG.open(encoding="utf-8")))


def save(rows):
    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def show_status(rows):
    free = [r for r in rows if (r.get("status") or "未使用") == "未使用"]
    used = [r for r in rows if r.get("status") == "投稿済"]
    print(f"📥 backlog在庫: 未使用 {len(free)}件 / 投稿済 {len(used)}件 / 計 {len(rows)}件")
    if len(free) < LOW_WATER:
        print(f"⚠️ 未使用が{LOW_WATER}件未満。x-idea-harvest で15件まで補充してください。")
    else:
        print(f"✅ 在庫は十分（{LOW_WATER}件以上）。補充不要。")
    print("\n--- 未使用（次に使える新鮮なネタ）---")
    for r in free:
        print(f"  [{r.get('post_type','')}/{r.get('theme','')}] {r['idea']}")


def consume(rows, needle, post_id):
    hit = None
    for r in rows:
        if r["idea"] == needle or r["idea"].startswith(needle):
            hit = r
            break
    if hit is None:
        sys.exit(f"該当ネタなし: {needle}")
    hit["status"] = "投稿済"
    note = (hit.get("notes") or "").strip()
    tag = f"{post_id}に反映" if post_id else "投稿済"
    hit["notes"] = f"{note} / {tag}".strip(" /")
    save(rows)
    print(f"✅ 投稿済に更新: {hit['idea']}（{post_id or '-'}）")
    show_status(rows)


def main():
    argv = sys.argv[1:]
    rows = load()
    if "--status" in argv or not argv:
        show_status(rows)
        return
    if "--consume" in argv:
        i = argv.index("--consume")
        needle = argv[i + 1] if i + 1 < len(argv) else None
        if not needle:
            sys.exit("usage: --consume \"idea前方一致\" post_id=week03-p1")
        post_id = ""
        for a in argv[i + 2:]:
            if a.startswith("post_id="):
                post_id = a.split("=", 1)[1]
        consume(rows, needle, post_id)
        return
    sys.exit("usage: --status | --consume \"idea\" post_id=...")


if __name__ == "__main__":
    main()
