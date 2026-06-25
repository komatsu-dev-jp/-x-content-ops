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
- 未実装断定（未提供の機能を「試せます／できます」と断定 → 「試してもらう予定です」）
- オカルト・迷信（「据え置き」「○時から出る」など店側挙動を事実化 → 記憶/印象として表現）
- 専門語の壁（「ボーダー」等を初心者に伝わる日常語へ言い換え）
- UI動作の誇張（タップ数など実装と一致しない断定）

Return:

- safe / caution / reject
- risk_flags（該当なしは `none`）
- safer rewrite
