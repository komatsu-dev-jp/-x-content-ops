#!/usr/bin/env python3
"""本日のX運用タスクの進捗を「2/5 あと3件」形式で表示するローカル追跡スクリプト。

自動投稿はしない。人間が手で投稿/返信したあとに 1 カウントするだけの後追いツール。
追加課金なし（ローカルCSV/JSONのみ）。

データソース:
- リプ周り: data/reply_outreach_log.csv（--done-reply で本日分を1行追加）
- 投稿:     data/post_log.csv（status=posted かつ date=今日 の行を自動カウント）

日次目標: data/daily_goals.json（無ければ reply_outreach=5 / post=1）

使い方:
  python3 scripts/daily_tracker.py                       # 本日の進捗を表示
  python3 scripts/daily_tracker.py --status              # 同上
  python3 scripts/daily_tracker.py --done-reply \\
      target_url=https://x.com/.../status/123 archetype=同意+質問 \\
      [got_reply=0 profile_visit=0 follow=0 note=...]    # リプ完了を1件記録→進捗表示
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

REPLY_LOG = Path("data/reply_outreach_log.csv")
POST_LOG = Path("data/post_log.csv")
GOALS = Path("data/daily_goals.json")
REPLY_COLS = ["date", "target_url", "archetype", "got_reply", "profile_visit", "follow", "note"]
DEFAULT_GOALS = {"reply_outreach": 5, "post": 1}


def today():
    return date.today().isoformat()


def load_goals():
    if GOALS.exists():
        try:
            g = json.loads(GOALS.read_text(encoding="utf-8"))
            return {**DEFAULT_GOALS, **g}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULT_GOALS)


def count_replies_today():
    if not REPLY_LOG.exists():
        return 0
    with REPLY_LOG.open(encoding="utf-8") as f:
        return sum(1 for r in csv.DictReader(f) if (r.get("date") or "").strip() == today())


def count_posts_today():
    if not POST_LOG.exists():
        return 0
    with POST_LOG.open(encoding="utf-8") as f:
        return sum(
            1 for r in csv.DictReader(f)
            if (r.get("date") or "").strip() == today()
            and (r.get("status") or "").strip() == "posted"
        )


def bar(done, goal, width=None):
    width = width or max(goal, 1)
    filled = min(done, goal)
    return "▓" * filled + "░" * max(width - filled, 0)


def line(label, done, goal):
    if goal <= 0:
        return f"{label}  {done}/{goal}"
    if done >= goal:
        extra = f"（+{done - goal}）" if done > goal else ""
        return f"{label}  {done}/{goal}  {bar(done, goal)}  ✅ 達成{extra}"
    return f"{label}  {done}/{goal}  {bar(done, goal)}  あと{goal - done}件"


def show_status():
    goals = load_goals()
    r_done, r_goal = count_replies_today(), goals["reply_outreach"]
    p_done, p_goal = count_posts_today(), goals["post"]
    total_done = min(r_done, r_goal) + min(p_done, p_goal)
    total_goal = r_goal + p_goal
    print(f"📅 本日のタスク ({today()})\n")
    print(line("リプ周り", r_done, r_goal))
    print(line("投稿　　", p_done, p_goal))
    print(f"\n合計 {total_done}/{total_goal} 完了", end="")
    if total_done >= total_goal:
        print(" 🎉 本日のノルマ達成！")
    else:
        print(f"（残り {total_goal - total_done} 件）")


def done_reply(argv):
    pairs = argv[argv.index("--done-reply") + 1:]
    data = {}
    for p in pairs:
        if "=" not in p:
            sys.exit(f"bad pair (need key=value): {p}")
        k, v = p.split("=", 1)
        data[k.strip()] = v.strip()
    if not data.get("target_url"):
        sys.exit("target_url is required (例: target_url=https://x.com/.../status/123)")
    unknown = [k for k in data if k not in REPLY_COLS]
    if unknown:
        sys.exit(f"unknown columns (not in {REPLY_COLS}): {unknown}")

    new = {c: "" for c in REPLY_COLS}
    new.update(data)
    new["date"] = today()
    write_header = not REPLY_LOG.exists()
    with REPLY_LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REPLY_COLS)
        if write_header:
            w.writeheader()
        w.writerow(new)
    print(f"✅ リプ完了を記録: {new['target_url']}\n")
    show_status()


def main():
    argv = sys.argv[1:]
    if "--done-reply" in argv:
        done_reply(argv)
    else:  # default / --status
        show_status()


if __name__ == "__main__":
    main()
