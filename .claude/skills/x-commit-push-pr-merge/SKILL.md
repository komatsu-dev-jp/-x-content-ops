---
name: x-commit-push-pr-merge
description: |
  git commit → push → PR作成 → マージ → 履歴記録 → /clear推奨 の完全ワークフロー。
  変更をコミットしてPRを作成し、GitHub上でマージした後、セッション内に履歴を残してトークン節約を促す。
  
  このスキルを使う場面：
  - ステージング済みの変更を commit してから PR を作成したい
  - PR マージ履歴（PR#、SHA、タイトル、日時）をセッション内に記録したい
  - マージ完了後に /clear を実行するよう促してほしい
  - 「#14 マージ済み」のような見える化が欲しい
  
  使い方：
  `/x-commit-push-pr-merge`（またはこのスキル名を呼び出し）後、
  1. commit message を提供
  2. GitHub で PR を開いて merge ボタンをクリック
  3. スキルに戻って「merged」と言う
  4. 履歴が記録され、/clear 推奨メッセージが表示される
---

# x-commit-push-pr-merge

## Purpose

git の commit 〜 push 〜 PR作成 〜 マージ 〜 ログ記録 〜 clear促進、という一連のワークフローを自動化し、
セッション内にマージ履歴を可視化（`✅ PR#14 マージ済み` 形式）して、トークン節約を促す。

## Workflow

### STEP 1: 前提確認と入力

```
必須入力：
  - commit message（1行以上。変更の説明）

オプション入力：
  - branch name（デフォルト: 現在のブランチ。指定時は切り替え）
```

始める前に以下を確認：
- [ ] `git status` で変更がある（stage済みまたはunstaged）
- [ ] 新しいコミットを作成するのが明確か
- [ ] ブランチ名は確認したか（デフォルトで現在のブランチ）

---

### STEP 2: git add + commit + push

1. **git status** で現状を表示
2. **git add** して変更をステージング（既に stage 済みなら skip）
3. **git commit** でコミット作成（メッセージはユーザー提供）
4. **git push -u origin <branch>** で push

---

### STEP 3: PR 作成

1. リポジトリの PR テンプレがあるか確認（`.github/pull_request_template.md` 等）
2. **mcp__github__create_pull_request** で PR 作成
   - title: commit message の 1 行目
   - body: テンプレあれば使用 / なければ commit message を本文に
   - base: `main`（デフォルト）
   - head: 現在のブランチ
3. PR URL と PR# を表示

---

### STEP 4: マージ待機と確認

表示：
```
┌──────────────────────────────────────────────────────┐
│ ✅ PR #<number> 作成完了
│
│ URL: https://github.com/.../pull/<number>
│
│ 📋 GitHub 上で以下を実行してください：
│ 1. PR を確認
│ 2. [Merge pull request] ボタンをクリック
│ 3. マージ方式は squash を選択
│ 4. マージ完了後、ここに戻ってきて「merged」と言ってください
└──────────────────────────────────────────────────────┘
```

ユーザーが「merged」と言ったら次へ。

---

### STEP 5: マージ確認と履歴記録

1. **git fetch origin <branch>** して最新情報を取得
2. **git log** で merge commit の SHA を確認
3. **output/prs/merge-log.md** に追記
   - ファイルがなければ作成
   - テーブル形式で記録：`| 日時 | PR# | タイトル | マージ方式 | SHA |`
   - 追記は append のみ

マージ履歴ファイルのヘッダー例：
```markdown
# PR Merge Log

| 日時 | PR# | タイトル | マージ方式 | SHA |
|------|-----|---------|---------|-----|
| 2026-08-06 14:30 | #14 | x-account-launch... | squash | 12ab493b... |
```

---

### STEP 6: マージ完了通知 + clear 推奨

表示（GitHub の差分画面のような見える化）：
```
┌──────────────────────────────────────────────────────┐
│                 ✅ PR #<number> マージ済み
│
│ 📊 詳細
│    PR#:         <number>
│    マージ方式:    squash
│    マージ SHA:   <short-sha>
│    タイムスタンプ: <datetime>
│
│ 💾 マージ履歴を記録しました：
│    output/prs/merge-log.md
│
│ 🚀 トークン節約のため、次を実行してください：
│    /clear
└──────────────────────────────────────────────────────┘
```

---

## Hard Constraints

- PR 作成までは自動化。**GitHub での merge はユーザーが手動実行**。
- ユーザーが「merged」と言うまで待機（API poll は使わない）。
- 履歴ファイルは上書きしない。必ず append のみ。
- PR テンプレがなければ、commit message をそのまま body に使用。
- マージ方式は squash で固定（オプション指定は skill 拡張時に）。
- `output/prs/` ディレクトリがなければ自動作成。

---

## Output Format

### 成功時：
マージ完了画面（上記の見える化フォーマット）+ merge-log.md への追記確認

### 失敗時：
- push 失敗：エラーメッセージ + retry 案
- PR 作成失敗：GitHub API エラー + manual PR 作成案
- merge 確認失敗：git fetch エラー + manual 確認案

---

## Notes

- **コンテキスト保持**：このスキルは対話形式（「merged」確認待機）なので、セッション継続が必須
- **ブランチ切り替え**：オプション入力で異なるブランチに push することも可能（デフォルトは現在のブランチ）
- **マージ履歴の意義**：GitHub 画面では見えない「このセッションでマージした」という記録をセッション内に残し、context 管理を明確にする

## Test Run Log

- 2026-08-06: Test Case 1 execution for warmup benchmark validation
- 2026-08-06: Test Case 3 multi-file changes validation (SKILL.md + references/example.md)
  - Scenario: Add example.md reference file alongside SKILL.md modification
  - Expected: Both files committed, pushed, and PR created with squash merge
