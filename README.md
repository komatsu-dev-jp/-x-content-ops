# PachiTracker X Growth Org

PachiTrackerのX運用を、Claude Code / Codex のSkill・Subagentで「小さな会社組織」のように分担して回すためのリポジトリです。

> 🚀 **初めての方は [docs/QUICKSTART.md](docs/QUICKSTART.md) を先に読んでください**（この順でやればOK、という使い方の1枚）。

## 結論

このリポジトリは、Xを完全自動運用するためのものではありません。目的は、PachiTrackerの思想に合った投稿を安定して作り、投稿前に品質とリスクを判定し、投稿後にログから勝ち型を更新することです。

追加課金を避けるため、MVPでは以下を使いません。

- X API
- FireCrawl
- Arcade
- Supabase
- Postiz有料版
- SocialDog有料版
- 外部LLM APIキー
- ブラウザ自動操作による自動いいね/自動リプ/自動フォロー

MVPは以下だけで回します。

- Claude Code または Codex の月額プラン内利用
- ローカルMarkdown / CSV
- Xの手動投稿またはX Proの予約投稿
- GitHubリポジトリ管理

## Core Concept

PachiTrackerのX運用は、以下の順番で評価します。

1. プロフィール遷移率
2. フォロー率
3. 返信率・リポスト率
4. いいね率
5. インプレッション

「バズったがユーザー候補が増えない投稿」より、「インプレッションは中程度でもプロフィール遷移とフォローが起きる投稿」を上位評価します。

## Main Workflow

```text
Idea Harvest
  → Draft
  → Risk Check
  → Score
  → Human Review
  → Schedule / Post
  → Log
  → Weekly Review
  → Rule Update
```

## Quick Start

Claude Code:

```text
/x-growth-company 今週のPachiTracker用X投稿を5本作って。追加課金なし、X Pro予約投稿前提で。
```

Codex:

```text
$x-growth-company を使って、PachiTrackerのX運用を今週分作成してください。投稿候補、採点、リスクチェック、CSVログ用行まで出してください。
```

## Directory

```text
CLAUDE.md / AGENTS.md    実行憲法（Claude Code / Codex が常に従うルール。同一内容）
.claude/agents/          Claude Code用サブエージェント
.claude/skills/          Claude Code用Skill
.codex/agents/           Codex用サブエージェント定義
.codex/skills/           Codex用Skill
prompts/                 投稿型、採点、禁止表現、ポジショニング、/loopテンプレ
memory/                  学習ループ（同じ指摘を2回受けたら追記し二度と繰り返さない）
docs/                    運用設計、コスト方針、リスク方針、ゴール・検証シート
data/                    投稿ログ、ネタ帳、A/Bテスト計画
scripts/                 文字数チェック、採点、週次レビュー、ログ追記補助
content/approved/        承認済み投稿（週次）
content/drafts/          下書き
content/assets/          画像素材
output/posts/            過去に生成した投稿ドラフト（履歴）
```

`.claude/skills/write-article/` は記事執筆用の既存Skillで、本X運用フローとは独立して共存します。

## ループ運用（任意・上級）

`/loop` で生成・分析・下書きまでを自走させられます（公開・送信・プッシュは常に人間）。
テンプレは `prompts/loop-prompts.md`、各ワークフローのゴール・検証は `docs/goal-verification-sheet.md` を参照。
同じ修正を2回受けたら `memory/feedback_*.md` に追記して再発を防ぎます。

## Scripts

```text
npm run validate   # 標準入力の投稿の文字数・禁止語チェック（exit 1 で不可）
npm run score      # 投稿候補を100点で採点
npm run weekly     # post_log.csv から週次レビュー（セグメント別＋縮小率ランキング）
npm run log -- --set post_id=... status=posted impressions=... profile_visits=...  # ログ追記/更新
npm run schedule   # post_log.csv → X Pro予約投稿用スケジュール・ワークシートCSV
```

## 統計的な勝敗判定

少数インプレッションの偶然当たりを「勝ち」と誤認しないため、週次レビューは次を守ります。

- impressions < 500 の投稿は「保留（低n）」として勝ち仮説の根拠にしない
- ランキングは経験ベイズ縮小率 `(events + 500*prior)/(impressions + 500)` で行う

詳細は `prompts/scoring-rubric.md`。
