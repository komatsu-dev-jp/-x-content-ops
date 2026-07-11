---
name: x-reply-assistant
description: X投稿後の返信候補を作る。自動返信ではなく人間レビュー前提。
---


# x-reply-assistant

Read:

- prompts/reply-templates.md
- prompts/pachitracker-positioning.md

Create 3 reply candidates:

1. empathy + question
2. product philosophy connection
3. beta-interest response if relevant

Never automate posting.

## β興味の記録（重要）

相手がβ版に興味を示した場合、人間が返信を送った後に必ず記録する
（`beta_interest_count` は AGENTS.md の primary KPI だが、記録先を作らないと計測できない）:

```
npm run today -- --done beta_interest target_url=<相手投稿URL> note=<反応の内容>
```

ノルマ（ノルマなし・記録専用）ではないため `npm run today` の合計には影響しないが、
`data/daily_activity_log.csv` に残り、週次レビューで拾える。
