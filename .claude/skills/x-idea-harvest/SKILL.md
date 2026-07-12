---
name: x-idea-harvest
description: PachiTracker向けX投稿のネタを収集し、重複と角度の偏りを避けて idea_backlog.csv へ追加する。
---


# x-idea-harvest

X運用パイプラインの最初の工程（ネタ収集）。下書き生成の前段。

Read:

- prompts/pachitracker-positioning.md（読者の痛みリスト）
- prompts/post-patterns.md（投稿型 / Hook Bank）
- prompts/angle-rotation.md（角度の定義とローテーションルール）
- data/idea_backlog.csv（既存ネタ。重複チェック用）
- data/post_log.csv（直近の theme / hook_type。角度の偏りチェック用）

## backlogの循環（重要・これが無いとbacklogは死ぬ）

idea_backlog.csv は「溜める→使う→補充」を回して初めて機能する。各行に `status` 列があり、
`未使用 / 投稿済` で管理する。

- **投稿の下書きを作るとき（x-draft-post / x-growth-company）**: まず backlog の `未使用` から引く。
  ゼロから考えるより速く、角度の偏りも防げる。
- **使ったら印を付ける**: 引いたネタは、対応する post_id を notes に足して `status=投稿済` に更新する。
- **在庫が減ったら補充**: `未使用` が **10件を下回ったら** この skill で 15件まで補充する。
- 補充・棚卸しは `python3 scripts/idea_backlog.py`（`--status` で在庫確認、`--consume "idea前方一致" post_id=...` で消化印）でも操作できる。

## やること（補充モード）

1. `未使用` の在庫を確認（10件未満なら補充する）。
2. 読者の痛み × 投稿型から新しいネタを 5〜10 個出す。
3. **重複排除**: idea_backlog.csv の既存 idea（投稿済も含む）と意味が近いものは出さない（言い換え重複もNG）。
4. **角度の分散**: `prompts/angle-rotation.md` の角度を基準に、直近の投稿/ネタ（post_log.csv の theme / 未使用backlog）が
   特定角度（記憶のズレ・判断ログ等）に偏っていれば、別角度（入力の面倒さ / 続行理由の変化 / 店・台選び / UI思想）を優先する。
5. 各ネタに reader_pain と post_type を紐づけ、`status=未使用` で追記する。

## 出力

`data/idea_backlog.csv` のスキーマで追記行を出す:

```text
date,idea,source,theme,reader_pain,post_type,priority,status,notes
```

- source: observation / confession / product のいずれか
- priority: high / mid / low（会話化・遷移期待が高いものを high）
- status: 新規追加は必ず `未使用`
- notes: 角度や狙い（例: Lane A 共感 / 別角度=入力の面倒さ）。投稿になったら `week03-p1に反映` 等を足す

## Hard Constraints

- 勝ち保証・煽り・内部ロジック・未実装断定を含むネタは出さない。
- 同じ角度・同じ言い回しに偏らせない（Phase 0 は既視感が致命的）。
