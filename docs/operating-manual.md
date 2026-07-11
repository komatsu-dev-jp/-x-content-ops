# 運用マニュアル

## Daily Workflow

1. `data/idea_backlog.csv` にネタを追加（`x-idea-harvest` Skillで生成可）
2. `x-growth-company` Skillで投稿候補を生成
3. `x-risk-check` Skillでリスク判定
4. `x-score-post` Skillで採点
5. 人間が最終判断
6. Xに手動投稿または予約投稿
7. 24〜48時間後に `data/post_log.csv` へ実績入力
   - 手動編集でも可。`python3 scripts/log_post.py --set post_id=... status=posted impressions=... profile_visits=... follows_gained=...` で列ズレなく追記/更新でき、各rate列と quality_score を自動計算する（追加課金なしのローカル処理）
8. リプ周りを送った場合、翌日以降に反応が分かれば `python3 scripts/log_reply.py --update target_url=... got_reply=1 profile_visit=1 follow=0` で記録（`data/reply_outreach_log.csv`）

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
