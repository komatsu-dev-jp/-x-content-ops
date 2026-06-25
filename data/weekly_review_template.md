# Weekly X Review

> 重点KPI: profile_visit_rate → follow_conv_rate（= follows_gained / profile_visits）
> ⚠️ 1週内の朝/昼/夜は型と交絡するので直接比較しない。型×時間帯（週またぎ）で判断する。
> 素データは `python3 scripts/weekly_review.py`（`npm run weekly`）で出力。

## 期間

YYYY-MM-DD 〜 YYYY-MM-DD

## 今週の投稿数

- 投稿数:
- 画像あり / なし:
- β導線あり:

## 上位投稿（profile_visit_rate順）

| rank | post_id | post_type | time_slot | pv_rate | follow_conv | why_won |
|---|---|---|---|---:|---:|---|

## 下位投稿

| rank | post_id | post_type | time_slot | quality_score | why_lost |
|---|---|---|---|---:|---|

## セグメント別平均（pv_rate / follow_conv_rate）

- 型別:
- 時間帯別（※型と交絡。参考）:
- 画像タイプ別:
- 曜日別:

## 型×時間帯（同型の週またぎ比較）

| post_type | morning | noon | night | 暫定の勝ちスロット |
|---|---|---|---|---|

## 勝ちフック / 負けパターン

- 勝ち:
- 負け:

## 次週の仮説（1つだけ）

勝ち投稿ではなく「勝ち仮説」を1つ決める。

```text
次週は ______ を検証する（例: 失敗告白型は朝より昼の方がpv_rateが高い）。
```

## 更新するファイル

- data/ab_test_plan.csv（winning_slot / decision）
- prompts/post-patterns.md（勝ちフック / Hook Bank）
- prompts/banned-patterns.md（負けパターン）
- docs/integrated-strategy.md
