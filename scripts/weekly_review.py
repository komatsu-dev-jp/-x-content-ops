#!/usr/bin/env python3
"""週次レビュー生成。

post_log.csv の posted 行を、プロフィール遷移率（profile_visit_rate）とフォロー転換率
（follow_conv_rate = follows_gained / profile_visits）を主軸にセグメント集計する。

重要な検証前提:
- 1週内では「時間帯」と「型」が交絡するため、同じ週の朝/昼/夜を直接比較しない。
- 各型を週ごとに別スロットへローテーション（data/ab_test_plan.csv）し、
  同じ型の時間帯差を週またぎで比較する。本スクリプトの「型×時間帯」表がその比較。
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path


def f(row, key):
    try:
        return float(row.get(key) or 0)
    except (ValueError, TypeError):
        return 0.0


def avg(rows, key):
    vals = [f(r, key) for r in rows if r.get(key) not in (None, "")]
    return sum(vals) / len(vals) if vals else 0.0


def seg_table(title, rows, group_key, metrics):
    print(f"\n## {title}")
    groups = defaultdict(list)
    for r in rows:
        groups[r.get(group_key) or "(未設定)"].append(r)
    print("| " + group_key + " | n | " + " | ".join(metrics) + " |")
    print("|" + "---|" * (len(metrics) + 2))
    for g in sorted(groups):
        gr = groups[g]
        cells = " | ".join(f"{avg(gr, m):.4f}" for m in metrics)
        print(f"| {g} | {len(gr)} | {cells} |")


def type_x_slot(rows, metric):
    """同型クロス週A/B: 型ごとに時間帯別の metric 平均を出す。"""
    print(f"\n## 型×時間帯（同型の週またぎ比較 / {metric}）")
    print("> 同じ型の行を時間帯で比較する。1行に複数スロットの数字が並んで初めてA/Bが成立する。")
    by_type = defaultdict(lambda: defaultdict(list))
    slots = ["morning", "noon", "night"]
    for r in rows:
        by_type[r.get("post_type") or "(未設定)"][r.get("time_slot") or "(未設定)"].append(r)
    print("| post_type | morning | noon | night | 暫定の勝ちスロット |")
    print("|---|---|---|---|---|")
    for t in sorted(by_type):
        cells, scores = [], {}
        for s in slots:
            gr = by_type[t].get(s, [])
            if gr:
                v = avg(gr, metric)
                scores[s] = v
                cells.append(f"{v:.4f}(n={len(gr)})")
            else:
                cells.append("-")
        winner = max(scores, key=scores.get) if len(scores) >= 2 else "（要追加データ）"
        print(f"| {t} | {cells[0]} | {cells[1]} | {cells[2]} | {winner} |")


def main():
    log = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/post_log.csv")
    if not log.exists():
        print("post_log.csv not found")
        sys.exit(1)
    rows = list(csv.DictReader(log.open(encoding="utf-8")))
    posted = [r for r in rows if r.get("status") == "posted"]

    print("# Weekly X Review")
    print("\n重点KPI: profile_visit_rate（プロフィール遷移率）→ follow_conv_rate（フォロー転換率）")
    print("\n> ⚠️ 1週内の朝/昼/夜は型と交絡するので直接比較しない。型×時間帯表（週またぎ）で判断する。")

    if not posted:
        print("\nまだ posted 行がありません。`npm run log` で実績を入れてから再実行してください。")
        print("（最低でも impressions / profile_visits / follows_gained / weekday / image_type を記録）")
        return

    for r in posted:
        r["_q"] = f(r, "quality_score")

    print("\n## Top Posts（quality_score順）")
    for r in sorted(posted, key=lambda r: r["_q"], reverse=True)[:5]:
        print(f"- {r.get('post_id')} | {r.get('post_type')} | {r.get('time_slot')} | "
              f"q={r.get('quality_score')} | pv_rate={r.get('profile_visit_rate')} | "
              f"first_line={r.get('first_line')}")

    print("\n## Top Posts（profile_visit_rate順）")
    for r in sorted(posted, key=lambda r: f(r, "profile_visit_rate"), reverse=True)[:5]:
        print(f"- {r.get('post_id')} | {r.get('post_type')} | {r.get('time_slot')} | "
              f"pv_rate={r.get('profile_visit_rate')} | follow_conv={r.get('follow_conv_rate')}")

    print("\n## Bottom Posts（quality_score順）")
    for r in sorted(posted, key=lambda r: r["_q"])[:5]:
        print(f"- {r.get('post_id')} | {r.get('post_type')} | {r.get('time_slot')} | "
              f"q={r.get('quality_score')} | first_line={r.get('first_line')}")

    metrics = ["profile_visit_rate", "follow_conv_rate", "reply_rate", "repost_rate"]
    seg_table("セグメント: 型別", posted, "post_type", metrics)
    seg_table("セグメント: 時間帯別（※型と交絡。参考値）", posted, "time_slot", metrics)
    seg_table("セグメント: 画像タイプ別", posted, "image_type", metrics)
    seg_table("セグメント: 曜日別", posted, "weekday", metrics)

    type_x_slot(posted, "profile_visit_rate")

    print("\n## 次週の仮説（1つだけ決める）")
    print("```text")
    print("勝ち投稿ではなく『勝ち仮説』を1つ。例: 失敗告白型は朝より昼の方がprofile_visit_rateが高い。")
    print("検証法: 該当型を次週その時間帯へローテーション（data/ab_test_plan.csv を更新）。")
    print("```")
    print("\n更新ファイル: data/ab_test_plan.csv（winning_slot/decision）, prompts/post-patterns.md（勝ちフック）")


if __name__ == "__main__":
    main()
