---
name: x-idea-harvest
description: PachiTracker向けX投稿のネタを収集し、重複と角度の偏りを避けて idea_backlog.csv へ追加する。
---


# x-idea-harvest

X運用パイプラインの最初の工程（ネタ収集）。下書き生成の前段。

Read:

- prompts/pachitracker-positioning.md（読者の痛みリスト）
- prompts/post-patterns.md（投稿型 / Hook Bank）
- data/idea_backlog.csv（既存ネタ。重複チェック用）
- data/post_log.csv（直近の theme / hook_type。角度の偏りチェック用）

## やること

1. 読者の痛み × 投稿型から新しいネタを 5〜10 個出す。
2. **重複排除**: idea_backlog.csv の既存 idea と意味が近いものは出さない（言い換え重複もNG）。
3. **角度の分散**: 直近の投稿/ネタが特定角度（記憶のズレ・判断ログ等）に偏っていれば、
   別角度（入力の面倒さ / 続行理由の変化 / 店・台選び / UI思想）を優先する。
4. 各ネタに reader_pain と post_type を紐づける。

## 出力

`data/idea_backlog.csv` のスキーマで追記行を出す:

```text
date,idea,source,theme,reader_pain,post_type,priority,notes
```

- source: observation / confession / product のいずれか
- priority: high / mid / low（会話化・遷移期待が高いものを high）
- notes: 角度や狙い（例: Lane A 共感 / 別角度=入力の面倒さ）

## Hard Constraints

- 勝ち保証・煽り・内部ロジック・未実装断定を含むネタは出さない。
- 同じ角度・同じ言い回しに偏らせない（Phase 0 は既視感が致命的）。
