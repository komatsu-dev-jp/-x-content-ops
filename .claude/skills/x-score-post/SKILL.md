---
name: x-score-post
description: PachiTracker向けX投稿候補を100点満点で採点する。
---


# x-score-post

Read:

- prompts/scoring-rubric.md
- prompts/banned-patterns.md

Score the post out of 100. 配点・判定閾値は `prompts/scoring-rubric.md`（Pre-post Score / Decision）に従う。
rubric を変更した場合はここではなく scoring-rubric.md を直す。

Breakdown keys（rubric の項目に対応）:

- first_line_hook
- pain_specificity
- pachitracker_connection
- profile_visit_potential
- low_sales_smell
- risk_safety
- readability

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
