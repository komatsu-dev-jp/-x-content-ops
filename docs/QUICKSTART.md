# はじめての使い方（この順でやればOK）

このリポジトリは「自動投稿bot」ではありません。
**Claude Code / Codex に開かせて指示すると、中のルールに従って投稿案・採点・週次分析をしてくれる「X運用の道具箱＋AI編集部」** です。
投稿そのものは、あなたが手でXに貼る（またはX Proで予約）します。

```text
リポジトリ = 頭脳（ルール・AI編集部・記録/分析）
Notion     = 人が見る画面（予定・チェック）
X / X Pro  = 実際に投稿する場所（手動）
```

---

## 0. 準備（最初の1回だけ）

1. Claude Code か Codex で、このリポジトリ（`-x-content-ops`）を開く。
2. （任意）`data/idea_backlog.csv` に投稿ネタを10〜20個入れておく。
   - Skill `x-idea-harvest` に出させてもよい。

> 追加課金なしで動きます。X API・外部SaaS・自動いいね/リプ/フォローは使いません。

---

## 1. 投稿を作る（毎回 5〜10分）

Claude Code:

```text
/x-growth-company 今週のPachiTracker用X投稿を5本作って。X Pro予約前提で。
```

これ1つで「ネタ→下書き→リスクチェック→採点→返信テンプレ」まで出ます。
（個別にやりたいときは下の「Skill早見表」を参照）

出てきたら **1本選ぶ**。迷ったら採点（score）が高く、risk_flags が `none` のものを選ぶ。

---

## 2. 投稿する（手動）

- Xに手で貼る、またはX Proで予約（例: 夜21:30）。
- 画像付きの型（UIスクショ）は、店舗名・個人情報・他社UI・未実装画面が**写り込んでいないか確認**。

予約をまとめて準備したいときは、予定一覧CSVを書き出せます:

```bash
npm run schedule        # data/post_log.csv → 予約用ワークシートCSV
```

---

## 3. 実績を記録する（投稿の24〜48時間後）

Xアナリティクスの数字を1行入れるだけ。列ズレや率計算は自動です。

```bash
npm run log -- --set post_id=week03-p1 status=posted \
  impressions=1200 profile_visits=40 follows_gained=3 \
  weekday=mon image_type=none
```

- `profile_visit_rate` / `follow_conv_rate` / `quality_score` は自動計算。
- impressions が500未満だと「保留（低n）」警告が出ます（偶然のブレが大きいため）。

---

## 4. 週末に振り返る（週1回 15分）

```bash
npm run weekly          # セグメント別＋型×時間帯の勝ちスロットを統計判定
```

- 「勝ち投稿」ではなく **「勝ち仮説」を1つだけ**決める。
  例:「失敗告白型は朝より昼の方がプロフィール遷移率が高い」
- 決めた仮説は `data/ab_test_plan.csv` に反映し、次週その型を別スロットへ動かす。

---

## Skill早見表（どんな時に何を使うか）

| やりたいこと | 使うもの | 補足 |
|---|---|---|
| まとめて今週分を作る | `/x-growth-company` | ネタ〜週次まで統合。まずこれでOK |
| ネタだけ増やしたい | `/x-idea-harvest` | 重複と角度の偏りを避けて backlog に追加 |
| 投稿案だけ3〜5本ほしい | `/x-draft-post` | 型に沿って下書き |
| 規約・景表法・煽り・未実装断定を確認 | `/x-risk-check` | safe / caution / reject で返る |
| 投稿候補を100点で採点 | `/x-score-post` | 90↑投稿可 / 80↑要改善 |
| 投稿後の返信案がほしい | `/x-reply-assistant` | 自分の投稿への返信。人が選ぶ |
| 他人の投稿にリプして伸ばす | `/x-reply-outreach` | ターゲットのリンク/本文を渡す→返信が返る案3つ。自動投稿なし |
| 週次レビューを作る | `/x-weekly-review` | `npm run weekly` の結果を解釈 |

### コマンド早見表（npm）

| コマンド | 用途 |
|---|---|
| `npm run validate` | 文字数・禁止語チェック（標準入力） |
| `npm run score` | 投稿候補を採点（標準入力） |
| `npm run log -- --set ...` | 実績をCSVへ追記/更新（率は自動計算） |
| `npm run weekly` | 週次レビュー（縮小率ランキング） |
| `npm run schedule` | 予約投稿用ワークシートCSV書き出し |
| `npm run tweet -- <URL>` | リプ周り用：ターゲット投稿の本文取得（best-effort） |
| `npm run today` | 本日の全タスク進捗を表示（投稿/リプ/いいね/フォロー、あと何件） |
| `npm run today -- --done reply target_url=...` | 手で送ったリプを1件カウント |
| `npm run today -- --done like count=5` | いいねを5件カウント |
| `npm run today -- --done follow target_url=...` | フォローを1件カウント |
| `npm run notify` | 本日の進捗を実数つきでSlackに通知（要webhook設定） |
| `npm run today -- --done like count=5 --notify` | 記録と同時にSlack通知 |

---

## Slack通知の設定（任意）

スマホに「リプ周り 2/5・あと3件」と**実数つきで届く**ようにできます。

1. Slackで **Incoming Webhook**（無料）を作成し、URL（`https://hooks.slack.com/services/...`）を取得
2. URLを渡す（**どちらか一方。コミットしない**）
   - 環境変数：`export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."`
   - またはファイル：`config/slack_webhook.txt` に貼る（`.gitignore`済み）
3. `npm run notify` で送信。`--notify` を付ければ記録と同時に送信
4. 毎日決まった時刻に送りたい → PC/サーバのcron等で `npm run notify` を叩く（任意）

> webhook URLは秘密情報です。リポジトリにコミットしないこと（`config/slack_webhook.txt` は除外設定済み）。

---

## よくある疑問

**Q. mergeすると自動で投稿が始まる？**
いいえ。merge は「改善版を正式版(main)に取り込む」だけ。投稿は常に手動です。merge すると次に開いたとき改善済みルールが最初から効きます。

**Q. Notionとリポジトリ、どっちが正？**
ルール・採点・記録の「正」はリポジトリ。Notionはそれを人が見る画面です。投稿の予定確認はNotion、生成・分析はリポジトリ、と使い分けます。

**Q. 何を一番見ればいい？**
プロフィール遷移率 → フォロー転換率（= フォロー数 ÷ プロフィール遷移数）。いいね数は参考程度。
