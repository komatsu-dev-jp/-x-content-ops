#!/usr/bin/env python3
"""Append or update a row in data/post_log.csv safely.

追加課金なし運用のためのローカル軽量スクリプト。X APIは使わず、Xアナリティクスの
数値を手動で渡して追記/更新する。ヘッダのカラム順に自動整列するので、列ズレを防ぐ。

使い方:
  # 予約投稿を仮登録
  python3 scripts/log_post.py --set post_id=week01-p1 date=2026-06-25 status=scheduled \
      theme=判断ミス post_type=問題提起型 time_slot=morning char_count=102

  # 投稿後にアナリティクス実績を追記（同じ post_id があれば上書き更新）
  python3 scripts/log_post.py --set post_id=week01-p1 status=posted \
      impressions=1200 profile_visits=48 follows_gained=3

derived rate列（like_rate / profile_visit_rate など）と quality_score は、
インプレッションと各数値が揃っていれば自動計算する。
"""
import csv
import sys
from pathlib import Path

LOG = Path("data/post_log.csv")


def parse_args(argv):
    if "--set" not in argv:
        sys.exit("usage: log_post.py --set key=value [key=value ...]")
    pairs = argv[argv.index("--set") + 1:]
    data = {}
    for p in pairs:
        if "=" not in p:
            sys.exit(f"bad pair (need key=value): {p}")
        k, v = p.split("=", 1)
        data[k.strip()] = v.strip()
    if "post_id" not in data:
        sys.exit("post_id is required")
    return data


def derive_rates(row):
    def f(k):
        try:
            return float(row.get(k) or 0)
        except ValueError:
            return 0.0

    imp = f("impressions")
    if imp <= 0:
        return
    pairs = {
        "like_rate": "likes",
        "repost_rate": "reposts",
        "reply_rate": "replies",
        "profile_visit_rate": "profile_visits",
        "follow_rate": "follows_gained",
    }
    for rate_col, count_col in pairs.items():
        if row.get(count_col):
            row[rate_col] = f"{f(count_col) / imp:.4f}"
    # follow_conv_rate: フォロー転換率 = follows_gained / profile_visits
    # （プロフィールに来た人のうち何%がフォローしたか。分母はインプレッションではない）
    pv = f("profile_visits")
    if pv > 0 and row.get("follows_gained"):
        row["follow_conv_rate"] = f"{f('follows_gained') / pv:.4f}"
    # quality_score: profile/follow を最優先する重み付け
    quality = (
        0.30 * f("profile_visit_rate")
        + 0.25 * f("follow_rate")
        + 0.20 * f("repost_rate")
        + 0.15 * f("reply_rate")
        + 0.10 * f("like_rate")
    ) * 100
    row["quality_score"] = f"{quality:.2f}"


def main():
    data = parse_args(sys.argv[1:])
    if not LOG.exists():
        sys.exit(f"{LOG} not found")
    rows = list(csv.DictReader(LOG.open(encoding="utf-8")))
    header = list(csv.reader(LOG.open(encoding="utf-8")))[0]

    unknown = [k for k in data if k not in header]
    if unknown:
        sys.exit(f"unknown columns (not in header): {unknown}")

    target = next((r for r in rows if r.get("post_id") == data["post_id"]), None)
    if target is None:
        target = {c: "" for c in header}
        rows.append(target)
        action = "appended"
    else:
        action = "updated"
    target.update(data)
    derive_rates(target)

    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in header})
    print(f"{action}: {data['post_id']} (quality_score={target.get('quality_score') or 'n/a'})")


if __name__ == "__main__":
    main()
