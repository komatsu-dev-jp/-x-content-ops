---
name: x-weekly-review
description: post_log.csvから週次レビューを作り、勝ち型と次週仮説を出す。
---


# x-weekly-review

Read:

- data/post_log.csv
- data/ab_test_plan.csv
- data/weekly_review_template.md
- prompts/scoring-rubric.md

実行: `python3 scripts/weekly_review.py`（または `npm run weekly`）でセグメント集計の素を出す。

Analyze:

- top posts by quality_score / profile_visit_rate / follow_conv_rate
- weak posts
- セグメント別平均（post_type / time_slot / image_type / weekday）
- 型×時間帯（同型の週またぎ比較）で「勝ちスロット」を判定
- winning hook patterns / losing patterns

## 検証前提（厳守）

- 1週内では時間帯と型が交絡するため、**同じ週の朝/昼/夜を直接比較しない**。
- 判断は「型×時間帯」表（週またぎ）で行う。各セルに n を併記し、n<2 のスロットは「要追加データ」とする。
- profile_visit_rate と follow_conv_rate（= follows_gained / profile_visits）を主軸にする。
  raw impressions だけで勝敗を決めない。

## 出力

- weekly review Markdown
- **次週の仮説を1つだけ**（勝ち投稿ではなく勝ち仮説）。例:「失敗告白型は朝より昼の方がpv_rateが高い」
- 反映先: `data/ab_test_plan.csv`（winning_slot / decision）, `prompts/post-patterns.md`（勝ちフック）
