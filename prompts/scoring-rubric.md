# Scoring Rubric

## Pre-post Score / 100

| 項目 | 点数 | 見ること |
|---|---:|---|
| 1行目フック | 20 | スクロールを止めるか。痛点・違和感・意外性があるか |
| 読者の痛み具体性 | 20 | 台選び・続行・撤退・記録面倒のどれかに刺さるか |
| PachiTracker接続 | 15 | 機能説明ではなく判断ログ思想に接続しているか |
| プロフィール遷移期待 | 15 | 何を作っている人か気になるか |
| 売り込み臭の低さ | 10 | 押し売り・PR臭が弱いか |
| リスクの低さ | 10 | 勝ち保証・誇大・規約リスクがないか |
| 読みやすさ | 10 | 140字以内、改行、短文、自然な日本語 |

## Decision

- 90-100: 投稿可。軽微な調整のみ。
- 80-89: 投稿可だが、1行目かCTAを改善。
- 70-79: 使えるが弱い。別案と比較。
- 60-69: 説明文・売り込み・抽象化の可能性。
- 0-59: 投稿しない。

## Post Performance Score

```text
quality_score =
  0.30 * profile_visit_rate +
  0.25 * follow_rate +
  0.20 * repost_rate +
  0.15 * reply_rate +
  0.10 * like_rate
```

## 最低母数とスムージング（重要）

少数インプレッションの偶然当たりを「勝ち」と誤認しないための統計ルール。

- **最低母数: impressions < 500 の投稿は「保留（低信頼）」**として扱い、勝ち仮説の根拠にしない。
- ランキングは生のrateではなく**経験ベイズ縮小率**で行う:

```text
shrunk_rate = (events + K * prior) / (impressions + K)
  prior = 母集団平均率（全posted行の events合計 / impressions合計）
  K = 500（疑似カウント。impが小さいほど prior へ引き戻す）
```

`scripts/weekly_review.py` がこの縮小率で profile_visit を順位付けし、`impressions<500` を `(低n)` と明示する。

## Caution

Raw impressions alone are not success.

A post with moderate impressions but high profile visits is more valuable than a viral post that does not convert into followers or beta interest.
