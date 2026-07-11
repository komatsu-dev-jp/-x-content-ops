---
name: x-risk-check
description: X投稿の規約・景表法・ギャンブル煽り・内部情報漏洩リスクを確認する。
---


# x-risk-check

Read:

- docs/legal-risk-policy.md
- prompts/banned-patterns.md

Check for:

- guaranteed profit claims
- misleading claims
- gambling encouragement
- overhype
- excessive hashtags
- duplicate-like wording
- internal algorithm leakage
- unreleased feature overstatement
- screenshot rights issue
- `prompts/banned-patterns.md` の「注意表現 A〜E」（未実装断定 / オカルト・迷信 / 専門語の壁 / UI動作の誇張 / リンク主役）

Return:

- safe / caution / reject
- risk_flags（該当なしは `none`）
- safer rewrite
