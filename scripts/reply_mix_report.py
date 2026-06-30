#!/usr/bin/env python3
"""data/reply_outreach_log.csv の tier 実績を、Notionの対象比率(50/30/20)と比較表示する。

使い方:
  python3 scripts/reply_mix_report.py            # 累計
  python3 scripts/reply_mix_report.py --days 7   # 直近N日のみ
"""
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

LOG = Path("data/reply_outreach_log.csv")
TARGET = {"A": 50, "B": 30, "C": 20}
LABEL = {
    "A": "A 500〜5,000垢 ",
    "B": "B 5,000〜50,000垢",
    "C": "C 10万超アカウント",
}


def load_rows(days=None):
    if not LOG.exists():
        return []
    rows = list(csv.DictReader(LOG.open(encoding="utf-8")))
    if days is None:
        return rows
    cutoff = date.today() - timedelta(days=days)
    out = []
    for r in rows:
        try:
            d = date.fromisoformat((r.get("date") or "").strip())
        except ValueError:
            continue
        if d >= cutoff:
            out.append(r)
    return out


def bar(pct, width=20):
    filled = round(pct / 100 * width)
    return "▓" * filled + "░" * max(width - filled, 0)


def main():
    argv = sys.argv[1:]
    days = None
    if "--days" in argv:
        i = argv.index("--days")
        days = int(argv[i + 1])

    rows = load_rows(days)
    tiered = [r for r in rows if (r.get("tier") or "").strip() in TARGET]
    untiered = len(rows) - len(tiered)
    total = len(tiered)

    period = f"直近{days}日" if days else "累計"
    print(f"📊 リプ周り tier 構成（{period}、tier記録あり {total}件" + (f"、未設定 {untiered}件）\n" if untiered else "）\n"))

    if total == 0:
        print("tierが記録されたリプがまだありません。`npm run reply-log -- --add ...` で記録してください。")
        return

    for tier, target_pct in TARGET.items():
        count = sum(1 for r in tiered if r["tier"] == tier)
        actual_pct = count / total * 100
        diff = actual_pct - target_pct
        sign = "+" if diff >= 0 else ""
        print(f"{LABEL[tier]}  実績{actual_pct:4.0f}% (目標{target_pct}%, {sign}{diff:.0f}pt)  {bar(actual_pct)}  {count}件")

    if untiered:
        print(f"\n⚠️ tier未設定 {untiered}件あり。`npm run reply-log -- --update target_url=... tier=A/B/C` で埋めると精度が上がります。")


if __name__ == "__main__":
    main()
