#!/usr/bin/env python3
"""本日のX運用タスクの進捗を「いいね 4/10 あと6件」形式で表示するローカル追跡。

自動操作はしない。人間が手で投稿/リプ/いいね/フォローしたあとに 1 カウントするだけの
後追いツール。追加課金なし（ローカルCSV/JSONのみ）。

タスク定義: data/daily_goals.json（task ごとに goal / label / source）
  - source=post_log : data/post_log.csv の status=posted & 本日分を自動カウント
  - source=manual   : data/daily_activity_log.csv に --done で記録した本日分をカウント

使い方:
  python3 scripts/daily_tracker.py                          # 本日の全タスク進捗を表示
  python3 scripts/daily_tracker.py --done like              # いいねを1件カウント
  python3 scripts/daily_tracker.py --done like count=5      # まとめて5件
  python3 scripts/daily_tracker.py --done reply target_url=https://x.com/.../status/123 note=...
  python3 scripts/daily_tracker.py --done reply target_url=... tier=A archetype=狭い質問  # tier比率も同時記録
  python3 scripts/daily_tracker.py --done follow target_url=https://x.com/someone
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

POST_LOG = Path("data/post_log.csv")
ACTIVITY_LOG = Path("data/daily_activity_log.csv")
REPLY_LOG = Path("data/reply_outreach_log.csv")
GOALS = Path("data/daily_goals.json")
ACT_COLS = ["date", "task", "count", "target_url", "note"]
TIER_TARGET = {"A": 50, "B": 30, "C": 20}
TIER_LABEL = {"A": "A 500〜5k", "B": "B 5k〜50k", "C": "C 10万+"}
DEFAULT_GOALS = {
    "post":   {"goal": 1,  "label": "投稿",     "source": "post_log"},
    "reply":  {"goal": 5,  "label": "リプ周り", "source": "manual"},
    "like":   {"goal": 10, "label": "いいね",   "source": "manual"},
    "follow": {"goal": 3,  "label": "フォロー", "source": "manual"},
}


def today():
    return date.today().isoformat()


def load_goals():
    if GOALS.exists():
        try:
            return json.loads(GOALS.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_GOALS


def count_posts_today():
    if not POST_LOG.exists():
        return 0
    with POST_LOG.open(encoding="utf-8") as f:
        return sum(
            1 for r in csv.DictReader(f)
            if (r.get("date") or "").strip() == today()
            and (r.get("status") or "").strip() == "posted"
        )


def count_manual_today(task):
    if not ACTIVITY_LOG.exists():
        return 0
    total = 0
    with ACTIVITY_LOG.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("date") or "").strip() == today() and (r.get("task") or "").strip() == task:
                try:
                    total += int(r.get("count") or 1)
                except ValueError:
                    total += 1
    return total


def count_today(task, spec):
    return count_posts_today() if spec.get("source") == "post_log" else count_manual_today(task)


def split_goal_by_tier(goal):
    """目標件数を50/30/20で按分（最大剰余法で合計が goal に一致するよう整数化）。"""
    exact = {t: goal * pct / 100 for t, pct in TIER_TARGET.items()}
    base = {t: int(v) for t, v in exact.items()}
    remainder = goal - sum(base.values())
    for t in sorted(exact, key=lambda t: exact[t] - base[t], reverse=True)[:remainder]:
        base[t] += 1
    return base


def count_tier_today():
    """本日 reply_outreach_log.csv に記録された tier 別件数（A/B/C）。"""
    counts = {t: 0 for t in TIER_TARGET}
    if not REPLY_LOG.exists():
        return counts
    with REPLY_LOG.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("date") or "").strip() != today():
                continue
            t = (r.get("tier") or "").strip()
            if t in counts:
                counts[t] += 1
    return counts


def tier_breakdown_line(reply_goal):
    """リプ周りタスクの下に出す tier 内訳行。tier記録が1件もなければ何も返さない。"""
    counts = count_tier_today()
    if sum(counts.values()) == 0:
        return None
    target = split_goal_by_tier(reply_goal)
    parts = []
    for t in TIER_TARGET:
        done, goal = counts[t], target[t]
        mark = "済" if done >= goal else f"あと{goal - done}"
        parts.append(f"{TIER_LABEL[t]} {done}/{goal}({mark})")
    return "  └ tier目安(50/30/20): " + " ・ ".join(parts)


def disp_width(s):
    # 全角(CJK)は2、半角は1で概算してラベル幅を揃える
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


def pad(s, width):
    return s + " " * max(width - disp_width(s), 0)


def bar(done, goal):
    filled = min(done, goal)
    return "▓" * filled + "░" * max(goal - filled, 0)


def line(label, done, goal, label_w):
    lbl = pad(label, label_w)
    if goal <= 0:
        return f"{lbl}  {done}/{goal}"
    if done >= goal:
        extra = f"（+{done - goal}）" if done > goal else ""
        return f"{lbl}  {done}/{goal}  {bar(done, goal)}  ✅ 達成{extra}"
    return f"{lbl}  {done}/{goal}  {bar(done, goal)}  あと{goal - done}件"


def compute_status():
    """進捗を構造化して返す（表示・Slack通知の共通ソース）。"""
    goals = load_goals()
    tasks, done_total, goal_total = [], 0, 0
    for task, spec in goals.items():
        goal = int(spec.get("goal") or 0)
        done = count_today(task, spec)
        tasks.append({"label": spec.get("label", task), "done": done, "goal": goal})
        done_total += min(done, goal)
        goal_total += goal
    return {"date": today(), "tasks": tasks, "done_total": done_total, "goal_total": goal_total}


def show_status():
    st = compute_status()
    goals = load_goals()
    label_w = max((disp_width(t["label"]) for t in st["tasks"]), default=4)
    print(f"📅 本日のタスク ({st['date']})\n")
    for task, t in zip(goals, st["tasks"]):
        print(line(t["label"], t["done"], t["goal"], label_w))
        if task == "reply":
            tb = tier_breakdown_line(t["goal"])
            if tb:
                print(tb)
    done_total, goal_total = st["done_total"], st["goal_total"]
    print(f"\n合計 {done_total}/{goal_total} 完了", end="")
    print(" 🎉 本日のノルマ達成！" if done_total >= goal_total and goal_total > 0
          else f"（残り {goal_total - done_total} 件）")


def maybe_notify(argv):
    """--notify が付いていれば Slack へ実数つき進捗を送る（任意）。"""
    if "--notify" not in argv:
        return
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import notify_slack
        notify_slack.run()
    except Exception as e:  # 通知失敗で本処理を止めない
        print(f"(Slack通知スキップ: {e})")


def done_task(argv):
    i = argv.index("--done")
    rest = argv[i + 1:]
    if not rest:
        sys.exit("usage: --done <task> [count=N target_url=... note=...] [--date YYYY-MM-DD]")
    task = rest[0]
    goals = load_goals()
    manual = [t for t, s in goals.items() if s.get("source") != "post_log"]
    if task not in goals:
        sys.exit(f"unknown task '{task}'. 使えるのは: {manual}")
    if goals[task].get("source") == "post_log":
        sys.exit(f"'{task}' は post_log から自動集計します。投稿は `npm run log` で記録してください。")

    # --date YYYY-MM-DD で過去日付への後追い記録が可能
    record_date = today()
    filtered = []
    j = 1
    while j < len(rest):
        if rest[j] == "--date" and j + 1 < len(rest):
            record_date = rest[j + 1]
            j += 2
        else:
            filtered.append(rest[j])
            j += 1

    data = {}
    for p in filtered:
        if p.startswith("--"):  # 他のフラグ（--notify など）は無視
            continue
        if "=" not in p:
            sys.exit(f"bad pair (need key=value): {p}")
        k, v = p.split("=", 1)
        data[k.strip()] = v.strip()
    allowed = ("count", "target_url", "note") + (("tier", "archetype") if task == "reply" else ())
    unknown = [k for k in data if k not in allowed]
    if unknown:
        sys.exit(f"unknown keys: {unknown} (使えるのは {', '.join(allowed)})")

    row = {c: "" for c in ACT_COLS}
    row.update({"date": record_date, "task": task, "count": data.get("count", "1"),
                "target_url": data.get("target_url", ""), "note": data.get("note", "")})
    write_header = not ACTIVITY_LOG.exists()
    with ACTIVITY_LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ACT_COLS)
        if write_header:
            w.writeheader()
        w.writerow(row)

    if task == "reply" and data.get("target_url"):
        sys.path.insert(0, str(Path(__file__).parent))
        import log_reply
        log_reply.append_row(record_date, data["target_url"], data.get("tier", ""),
                              data.get("archetype", ""), data.get("note", ""))

    past = f"（{record_date} 付け）" if record_date != today() else ""
    print(f"✅ {goals[task].get('label', task)} +{row['count']} を記録{past}\n")
    show_status()


def main():
    argv = sys.argv[1:]
    if "--done" in argv:
        done_task(argv)
    else:  # default / --status
        show_status()
    maybe_notify(argv)


if __name__ == "__main__":
    main()
