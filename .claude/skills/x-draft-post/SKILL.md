---
name: x-draft-post
description: PachiTracker向けX投稿案を投稿型に沿って3〜5案作る。
---


# x-draft-post

Read:

- prompts/pachitracker-positioning.md
- prompts/post-patterns.md
- prompts/banned-patterns.md
- prompts/angle-rotation.md

Generate 3-5 Japanese X post candidates.

Rules:

- Prefer 60-140 Japanese characters
- Strong first line
- Low sales smell
- Connect to judgment log
- Mention PachiTracker lightly
- 0-2 hashtags
- Include image suggestion if useful

## 切り口の分散（必須）

角度の定義は `prompts/angle-rotation.md` を正典とする。3〜5案は**別々の角度**から作り、同じ角度に偏らせない。
直近投稿（`data/post_log.csv` の theme / hook_type）が特定角度に偏っていれば、別角度を優先する。

## 表現の安全（必ず守る）

`prompts/banned-patterns.md` の「表現の安全（生成時に必ず守る）」セクションに従う
（未実装断定・オカルト表現・専門語・UI誇張・リンク主役の5項目）。

Output each draft with:

- post_type
- text
- first_line
- expected_kpi
- suggested_image
- CTA
