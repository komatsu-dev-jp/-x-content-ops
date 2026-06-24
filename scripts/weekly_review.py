#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


def pct(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def main():
    log = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/post_log.csv")
    if not log.exists():
        print("post_log.csv not found")
        sys.exit(1)
    rows = list(csv.DictReader(log.open(encoding="utf-8")))
    posted = [r for r in rows if r.get("status") == "posted"]
    if not posted:
        print("No posted rows yet.")
        return
    for r in posted:
        try:
            r["_score"] = float(r.get("quality_score") or 0)
        except ValueError:
            r["_score"] = 0
    top = sorted(posted, key=lambda r: r["_score"], reverse=True)[:5]
    bottom = sorted(posted, key=lambda r: r["_score"])[:5]

    print("# Weekly X Review")
    print("\n## Top Posts")
    for r in top:
        print(f"- {r.get('post_id')} | {r.get('theme')} | {r.get('post_type')} | score={r.get('quality_score')} | first_line={r.get('first_line')}")
    print("\n## Bottom Posts")
    for r in bottom:
        print(f"- {r.get('post_id')} | {r.get('theme')} | {r.get('post_type')} | score={r.get('quality_score')} | first_line={r.get('first_line')}")
    print("\n## Next Hypothesis")
    print("次週は、上位投稿の first_line と post_type を再利用し、時間帯か画像有無だけを1変数で検証する。")

if __name__ == "__main__":
    main()
