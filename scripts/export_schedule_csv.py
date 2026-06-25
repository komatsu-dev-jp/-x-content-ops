#!/usr/bin/env python3
"""post_log.csv から X Pro 予約投稿用のスケジュール・ワークシートを書き出す。

X Pro（予約投稿）はCSVの自動取り込みには非対応のため、これは「いつ・どれを・画像付きで
出すか」を一覧化した手作業用チェックリスト。time_slot を具体時刻の目安に変換する。

使い方:
  python3 scripts/export_schedule_csv.py                 # stdout に出力
  python3 scripts/export_schedule_csv.py --out out.csv   # ファイルに出力
  python3 scripts/export_schedule_csv.py --all           # posted も含める（既定は未投稿のみ）
"""
import csv
import sys
from pathlib import Path

LOG = Path("data/post_log.csv")

# time_slot → 予約の目安時刻（A/Bは weekly_review の結果で後から調整）
SLOT_TIME = {"morning": "08:30", "noon": "12:30", "night": "21:30"}

OUT_COLS = [
    "date", "suggested_time", "post_id", "post_type", "time_slot",
    "has_image", "image_type", "status", "first_line",
]


def main():
    argv = sys.argv[1:]
    include_all = "--all" in argv
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    if not LOG.exists():
        sys.exit(f"{LOG} not found")

    rows = list(csv.DictReader(LOG.open(encoding="utf-8")))
    selected = []
    for r in rows:
        if not include_all and r.get("status") == "posted":
            continue
        selected.append({
            "date": r.get("date", ""),
            "suggested_time": SLOT_TIME.get(r.get("time_slot", ""), ""),
            "post_id": r.get("post_id", ""),
            "post_type": r.get("post_type", ""),
            "time_slot": r.get("time_slot", ""),
            "has_image": r.get("has_image", ""),
            "image_type": r.get("image_type", ""),
            "status": r.get("status", ""),
            "first_line": r.get("first_line", ""),
        })
    selected.sort(key=lambda x: (x["date"], x["suggested_time"]))

    fh = open(out, "w", encoding="utf-8", newline="") if out else sys.stdout
    w = csv.DictWriter(fh, fieldnames=OUT_COLS)
    w.writeheader()
    for r in selected:
        w.writerow(r)
    if out:
        fh.close()
        print(f"wrote {len(selected)} rows -> {out}")


if __name__ == "__main__":
    main()
