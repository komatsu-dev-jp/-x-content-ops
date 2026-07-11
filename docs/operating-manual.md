# 運用マニュアル

## 日次タスクの考え方（`data/daily_goals.json`）

Phase 0（フォロワー50人未満）は量より継続が効く。全項目を毎日満点で回そうとして
実行が止まるより、少ない項目を毎日続ける方が学習ループ（週次レビュー）が止まらない。

- **リプ周りだけ数値目標**（最低ライン3・満点ライン5）。`npm run today` で両方の達成状況が出る。
  最低ラインを守れない日が続くようなら、満点ラインではなく最低ラインの方を疑う。
- **記録は1日の終わりにまとめて行う。** リプを打つたびに記録すると摩擦で止まりやすい
  （実際に11日間記録が止まった原因）。日中はURLをメモに貼るだけにして、寝る前に
  `python3 scripts/daily_tracker.py --done reply --batch` でまとめて流し込む（詳細は`x-reply-outreach`）。
- **いいね・フォロー・投稿・β興味はノルマなし（記録のみ）。**
  - いいねは独立目標にしない。リプ対象を探す下調べのついでに行う。
  - フォローは、リプで会話が成立した相手（`got_reply=1` を記録した相手）だけに絞る。
    機械的な日次フォローはFF比を悪化させ、プロフィール遷移してきた人への信頼感を損なう。
  - 投稿は週次でまとめて予約する（`npm run schedule`）ため、日次ノルマにしない。

## Daily Workflow

1. `data/idea_backlog.csv` にネタを追加（`x-idea-harvest` Skillで生成可）
2. `x-growth-company` Skillで投稿候補を生成
3. `x-risk-check` Skillでリスク判定
4. `x-score-post` Skillで採点
5. 人間が最終判断
6. Xに手動投稿または予約投稿したら、**その場で** `status=posted` だけ反映する（数値は空でよい）:
   `python3 scripts/log_post.py --set post_id=... status=posted`
   - これをやらないと `npm run today` の「投稿」タスクが永久に未達成表示になる（scheduled のまま実績入力日まで残るため）。
7. 24〜48時間後、`data/post_log.csv` に実績（impressions等）を追記
   - `python3 scripts/log_post.py --set post_id=... impressions=... profile_visits=... follows_gained=...` で列ズレなく追記/更新でき、各rate列と quality_score を自動計算する（追加課金なしのローカル処理）
8. リプ周りを送った場合、翌日以降に反応が分かれば `python3 scripts/log_reply.py --update target_url=... got_reply=1 profile_visit=1 follow=0` で記録（`data/reply_outreach_log.csv`）
9. リプ・DM等で「β版に興味がある」反応があれば `npm run today -- --done beta_interest target_url=... note=...` で記録（ノルマなし・記録専用。AGENTS.mdのprimary KPI `beta_interest_count` の実データ）

## Weekly Workflow

1. `scripts/weekly_review.py` を実行
2. `scripts/reply_mix_report.py` でリプ周りのtier構成と反応率を確認
3. 勝ち投稿と負け投稿を比較
4. `prompts/post-patterns.md` を更新（勝ちフックの追加）
5. `prompts/banned-patterns.md` を更新
6. 次週のA/B変数を1つだけ決める

## Monthly Workflow

1. 固定ポストを見直す
2. プロフィール文を見直す
3. 投稿比率を見直す
4. β募集導線を見直す
5. リポジトリのSkillを更新する

## Approval Rules

投稿承認条件：

- 140字以内、または意図的なスレッド
- 1行目に明確な痛点がある
- 売り込み臭が弱い
- PachiTrackerの思想に接続している
- 禁止表現がない
- 未実装機能を断定していない
- 画像がある場合、権利・個人情報・店舗情報に問題がない

## Rejection Rules

投稿しない条件：

- 「勝てる」「稼げる」断定
- ハッシュタグ過多
- 同じ言い回しの繰り返し
- リンクだけを主役にする
- アプリの機能説明だけで読者の痛みがない
- 説教臭い
- パチンコユーザーを馬鹿にしている
