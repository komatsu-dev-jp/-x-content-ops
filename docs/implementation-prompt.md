# Claude Code / Codex 初回実装プロンプト

```text
このリポジトリを PachiTracker のX運用編集部として整備してください。

目的:
Claude Code / Codex のSkill・Subagentを使って、PachiTracker用X投稿を追加課金なしで生成・採点・改善できるようにする。

前提:
- X APIは使わない
- 外部有料SaaSは使わない
- 自動いいね、自動リプ、自動フォローはしない
- 投稿は手動またはX Pro予約投稿
- ログはCSV
- 評価はプロフィール遷移率とフォロー率を最優先

やること:
1. AGENTS.mdを読んで運用方針を理解
2. docs/integrated-strategy.mdを中心設計として扱う
3. .claude/skills と .claude/agents をClaude Code用に調整
4. .codex/skills と .codex/agents をCodex用に調整
5. scripts/validate_post.py と scripts/score_posts.py を動作確認
6. data/idea_backlog.csv に初期ネタを20件作成
7. 今週分の投稿候補を5本作成
8. 各投稿に score、risk_flags、recommended_time_slot、reply_templates を付ける
9. 承認済み投稿を content/approved/week-01.md に保存
10. 投稿後に data/post_log.csv に追記できる形にする

PachiTrackerの思想:
- 感覚ではなく、判断ログで打つ
- 台選び・続行・撤退を記録して後から見直す
- 勝ち保証ではなく、判断の振り返り
- パチンコユーザーの感情的な判断ミスを可視化する

禁止:
- 絶対勝てる
- 稼げる
- 必勝
- 最強
- 勝率爆上げ
- 内部ロジックの詳細公開
- 未実装機能の断定
- ギャンブルを煽る表現
```
