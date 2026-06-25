---
name: x-score-post
description: PachiTracker向けX投稿候補を100点満点で採点する。
---


# x-score-post

Read:

- prompts/scoring-rubric.md
- prompts/banned-patterns.md

Score the post out of 100.

Breakdown:

- first_line_hook: 20
- pain_specificity: 20
- pachitracker_connection: 15
- profile_visit_potential: 15
- low_sales_smell: 10
- risk_safety: 10
- readability: 10

Return:

```json
{
  "score_total": 0,
  "breakdown": {},
  "risk_flags": [],
  "decision": "post | revise | reject",
  "rewrite": ""
}
```
