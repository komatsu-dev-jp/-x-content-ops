---
name: x-growth-company
description: |
  PachiTrackerのX運用を小さなAI編集部として実行する統合Skill。ネタ収集、投稿生成、リスクチェック、採点、返信案、週次改善までを統合する。

  以下の場面で使うこと:
  - 「今週のX投稿を作って」「PachiTrackerの投稿候補を出して」などの投稿生成依頼
  - X運用、SNS戦略、β募集、UIスクショのキャプション作成
  - 投稿の採点・リスクチェック・週次レビュー
---

# x-growth-company

## Purpose

Operate PachiTracker's X growth workflow as an AI organization.

## Required Inputs

If missing, infer conservatively:

- objective: profile visits / follows / beta testers / UI feedback
- theme
- target reader
- post lane
- media availability

## Workflow

1. CEO: decide objective and KPI
2. Editor-in-Chief: choose post lane
3. Audience Researcher: extract reader pain
4. Product Translator: convert feature into pain/benefit
5. Draft Writer: generate 3-5 candidates
6. Risk Guard: remove risky claims and spam-like patterns
7. Growth Analyst: score each candidate /100
8. Reply Concierge: prepare 2-3 reply templates
9. A/B Planner: assign time slots per `data/ab_test_plan.csv` rotation (see below)
10. Output final recommendation

## A/B & 検証設計（必須ルール）

「投稿計画」ではなく「検証計画」を作る。何が勝因かを後から切り分けられる形にする。

- **1度に変える変数は1つ**。型・時間帯・画像有無・曜日を同時に動かさない。
- **1週内で朝/昼/夜を直接比較しない**（型と時間帯が交絡するため）。
- 各型を週ごとに別スロットへローテーションし、**同じ型の時間帯差を週またぎで比較**する。
  ローテーション表は `data/ab_test_plan.csv`（post_type ごとの w1/w2/w3 スロット）。
- UIスクショ型は画像を常に付け、画像有無を変数化しない（時間帯のみ動かす）。
- 各投稿に必ず `post_type` / `time_slot` / `weekday` / `image_type` を記録（`data/post_log.csv`）。
- 週次は「勝ち投稿」ではなく「勝ち仮説」を1つだけ決める（`x-weekly-review`）。

## 切り口の分散（既視感の回避）

同じ思想（判断ログ）でも切り口を毎回ずらす。Phase 0 は同一読者に何度も見られるため、
「また同じこと言ってる人」化を避ける。最低でも以下5角度をローテーション:

| 角度 | 例 |
|---|---|
| 記憶のズレ | 勝った日の記憶だけ残る |
| 入力の面倒さ | 入力が重いと記録しない／楽な判断を選ぶ |
| 続行理由の変化 | 打ってる最中と後で理由が変わる |
| 店・台選び | 店の印象と実績がズレる |
| UI思想 | 実戦中は考えず押せる方がいい |

直近の投稿が「記憶のズレ」「判断ログ」に偏っていないか毎回チェックする。

## Output Format

```markdown
# X投稿候補

## 目的

## 推奨投稿
本文

- score:
- reason:
- risk:
- image suggestion:
- recommended time slot:

## 代替案

### 案2
...

## 返信テンプレ

## CSVログ用メモ
```

## Hard Constraints

- No guaranteed profit claims
- No automated X actions
- No external paid APIs
- No link-first posts by default
- No exposing proprietary algorithms
- No unreleased feature overstatement
