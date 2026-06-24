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
9. Output final recommendation

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
