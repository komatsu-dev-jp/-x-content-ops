---
name: x-weekly-review
description: post_log.csvから週次レビューを作り、勝ち型と次週仮説を出す。
---


# x-weekly-review

Read:

- data/post_log.csv
- data/ab_test_plan.csv
- data/weekly_review_template.md
- data/reply_outreach_log.csv（リプ周りの反応実績。投稿と並ぶ主要チャネル）
- prompts/scoring-rubric.md

実行: `python3 scripts/weekly_review.py`（または `npm run weekly`）でセグメント集計の素を出す。
補助: `python3 scripts/reply_mix_report.py`（または `npm run reply-mix`）でリプ周りのtier構成を確認。

Analyze:

- top posts by quality_score / profile_visit_rate / follow_conv_rate
- weak posts
- セグメント別平均（post_type / time_slot / image_type / weekday）
- 型×時間帯（同型の週またぎ比較）で「勝ちスロット」を判定
- winning hook patterns / losing patterns
- **リプ周り（archetype別）の got_reply率 / profile_visit率 / follow率**（`weekly_review.py` が自動集計）

## 検証前提（厳守）

- 1週内では時間帯と型が交絡するため、**同じ週の朝/昼/夜を直接比較しない**。
- 判断は「型×時間帯」表（週またぎ）で行う。各セルに n を併記し、n<2 のスロットは「要追加データ」とする。
- profile_visit_rate と follow_conv_rate（= follows_gained / profile_visits）を主軸にする。
  raw impressions だけで勝敗を決めない。
- **最低母数**: impressions<500 の投稿は「保留（低n）」とし勝ち仮説の根拠にしない。
  ランキングは経験ベイズ縮小率 `(events + 500*prior)/(impressions + 500)` で行う（`weekly_review.py` が自動）。
- **Phase 0（posted平均impressions<500）の間は縮小率ランキングを参考値扱いとし、
  絶対数（profile_visits・replies・follows_gained）と定性シグナルで仮説を立てる**
  （`weekly_review.py` が平均impressionsで自動判定し、該当時は `⚠️ Phase 0 モード` を表示する）。
- **投稿とリプ周りは分けて評価する。** インプレッションの主源泉がどちらかは
  `daily_activity_log.csv`（送信件数）と `reply_outreach_log.csv`（反応）を見て判断する。
  reply_outreach_log に未更新行（got_reply列が空）が多い場合は、まず記録を埋めるよう促す。

## 出力

- weekly review Markdown
- **次週の仮説を1つだけ**（勝ち投稿ではなく勝ち仮説）。投稿・リプ周りのどちらから出してもよい。
  例:「失敗告白型は朝より昼の方がpv_rateが高い」「archetype『同意+一歩+狭い質問』はgot_reply率が高い」
- 反映先: `data/ab_test_plan.csv`（winning_slot / decision）, `prompts/post-patterns.md`（勝ちフック）,
  `prompts/reply-outreach-playbook.md`（リプ周りの勝ち型）
