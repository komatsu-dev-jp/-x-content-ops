---
name: x-draft-post
description: PachiTracker向けX投稿案を投稿型に沿って3〜5案作る。
---


# x-draft-post

Read:

- prompts/pachitracker-positioning.md
- prompts/post-patterns.md
- prompts/banned-patterns.md

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

同じ思想でも切り口を毎回ずらす。3〜5案は**別々の角度**から作り、同じ角度に偏らせない。

| 角度 | 狙い |
|---|---|
| 記憶のズレ | 共感・拡散 |
| 入力の面倒さ | 継続設計・信頼 |
| 続行理由の変化 | 振り返り・保存 |
| 店・台選び | あるある・自分事化 |
| UI思想 | プロフィール遷移 |

直近投稿（`data/post_log.csv` の theme / hook_type）が特定角度に偏っていれば、別角度を優先する。

## 表現の安全（必ず守る）

- 未実装機能を「試せます／できます」と断定しない（「試してもらう予定です」）。
- 「据え置き」「○時から出る」など店側の挙動を事実のように書かない（記憶・印象として書く）。
- 「ボーダー」など専門語は初心者に伝わる日常語へ言い換える。
- UIの操作（タップ数など）は実装と一致しない断定をしない。

Output each draft with:

- post_type
- text
- first_line
- expected_kpi
- suggested_image
- CTA
