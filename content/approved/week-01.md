# X投稿候補 — Week 01（2026-06-24 〜 2026-06-30）

## 目的（CEO / Strategy Lead）

- 今週の重点: **プロフィール遷移率**の最大化（フォロー率は副指標）
- フェーズ: Phase 0（MVP前 / フォロワー50人未満）
- 投稿比率（Phase 0）: 問題提起35% / あるある20% / 失敗告白20% / UIスクショ15% / β募集10%
- A/Bテスト変数（1週目）: **時間帯**（型・テーマは固定し、朝/昼/夜で比較）
- 評価指標: profile_visit_rate を最優先で記録する

KPI優先順位: profile_visit_rate → follow_rate → reply_rate → repost_rate → bookmark_rate →（参考）like_rate / impressions

> スコアは `scripts/validate_post.py` と `scripts/score_posts.py` の実測値を併記。
> risk_flags は `x-risk-check` 基準（規約 / 景表法 / ギャンブル煽り / 内部ロジック漏洩 / 未実装断定 / スクショ権利）。
> 該当なしは `none`。

---

## Post 1｜6/25(木) — 問題提起型（Lane A）

```
昨日出ていた台に、今日も座ってしまう。

「昨日のアレ」は、台の実力じゃなくて自分の記憶かもしれない。

その記憶を疑うために、台選び・続行・撤退を記録して後から見直すアプリを作っています。

#パチンコ #個人開発
```

- post_type: 問題提起型
- char_count: 102（140字以内 ✅）
- score: 85/100（validate: pass）
- breakdown: 1行目フック○ / 痛点具体性○（昨日出ていた台）/ PachiTracker接続○ / プロフィール遷移期待○ / 売り込み臭 低 / リスク 低
- risk_flags: `none`
- recommended_time_slot: **朝 08:00〜09:30**（分析・思想枠 / 記憶バイアスの気づき系）
- image_suggestion: なし（本文完結型）
- reply_templates:
  1. （深掘り）「それ、ありますよね。昨日と今日で一番ブレやすいのは、台選び・続行・撤退のどこですか？」
  2. （思想接続）「『昨日のアレ』って、その場では根拠に感じるんですよね。あとで記録を見ると印象だけだったことが多くて、だから残せる形にしたいと思ってます。」

---

## Post 2｜6/26(金) — あるある型（Lane B）

```
これ、やりがち。

・昨日出ていた台に座る
・前半回った記憶で続ける
・投資したからヤメられない

どれも、判断が感情に寄ってるサイン。
記録して後で見直すと、続けた理由がいつの間にか変わってる。
```

- post_type: あるある型
- char_count: 91（140字以内 ✅）
- score: 85/100（validate: pass）
- breakdown: 箇条書きで自分事化○ / 痛点3点○ / PachiTracker接続（思想）○ / 売り込み臭 ほぼ無 / リスク 低
- risk_flags: `none`
- recommended_time_slot: **昼 12:00〜13:00**（軽いあるある枠）
- image_suggestion: なし
- reply_templates:
  1. （深掘り）「全部やったことあります、で終わりがちですよね。自分だとどれが一番抜けられないですか？」
  2. （共感+思想）「『感情に寄ってるサイン』、ほんとそれです。記録すると、続行した理由が後から変わってるのが見えて面白いですよ。」

---

## Post 3｜6/27(土) — 失敗告白型（Lane C）★今週の本命

```
記録アプリを自分で作ってるのに、昨日は入力をサボって続行判断をミスった。

便利な機能より、面倒でも続く入力導線のほうが先だと思い知った。

PachiTrackerは、実戦中に迷わない入力を優先しています。
```

- post_type: 失敗告白型
- char_count: 100（140字以内 ✅）
- score: 95/100（validate: pass）
- breakdown: 1行目フック○ / 痛点（記録が続かない）○ / 開発者の人間味○ / PachiTracker接続○ / 売り込み臭 低 / リスク 低
- risk_flags: `none`
- recommended_time_slot: **朝 08:00〜09:30**（開発・思想枠 / build-in-public）
- image_suggestion: 任意で記録画面の入力導線スクショ（権利・個人情報・店舗名なしを確認）
- reply_templates:
  1. （深掘り）「サボる瞬間って、だいたい忙しい時ですよね。どのタイミングの入力が一番おっくうですか？」
  2. （思想接続）「便利さより継続、すごく分かります。入力が重いと、正しい判断より楽な判断を選んじゃうので、そこを軽くするのを最優先にしてます。」

---

## Post 4｜6/29(月) — UIスクショ型（Lane D）

```
入力が面倒だと、正しい判断より「楽な判断」を選ぶ。

だからPachiTrackerは、実戦中に迷わず押せる記録画面を優先しました。

台選び・続行・撤退を、その場でサッと記録。

#個人開発
```

- post_type: UIスクショ型
- char_count: 90（140字以内 ✅）
- score: 90/100（validate: pass）
- breakdown: 1行目フック○ / 痛点（入力負担）○ / PachiTracker接続○ / プロフィール遷移期待◎（実画面）/ リスク 低
- risk_flags: `none`（※採点スクリプトの `product_name_too_early` はスタイル上の軽微指摘。本文構造上、問題なしと判断）
- recommended_time_slot: **夜 21:00〜22:30**（UI相談・実戦者枠）
- image_suggestion: **記録画面のスクショ必須**（店舗名・個人情報・他社UI流用・未実装機能の写り込みがないか確認）
- reply_templates:
  1. （深掘り）「実戦中だと何タップで入れたいですか？ 入力が多いと感じる場面ってありますか？」
  2. （UI相談返信）「ありがとうございます。見た目より『迷わず押せるか』を優先したいので、その視点で調整してみます。」

---

## Post 5｜6/30(火) — β募集型（Lane F）

```
パチンコの台選び・続行・撤退を、感覚じゃなく記録で見直したい人へ。

PachiTrackerのβ版を、少人数で触ってもらう準備をしています。

あとで判断を振り返れる部分から、試してもらう予定です。
```

- post_type: β募集型
- char_count: 96（140字以内 ✅）
- score: 90/100（validate: pass）
- breakdown: 対象明確○ / 痛点接続○ / 控えめCTA○（Phase 0は煽らない）/ リスク 低
- risk_flags: `none`（※採点スクリプトの `product_name_too_early` はスタイル上の軽微指摘。募集文として許容）
- recommended_time_slot: **夜 21:00〜22:30**（β募集枠）
- image_suggestion: なし、または判断ログ画面のスクショ
- reply_templates:
  1. （β候補への返信）「ありがとうございます。準備でき次第ご案内します。台選び・続行・撤退の振り返り部分から試してもらう予定です。」
  2. （深掘り）「ちなみに今、振り返りで一番モヤつくのはどの判断ですか？ β版の優先順位の参考にさせてください。」

---

## A/B割り当て（型×時間帯ローテーションの Week 1）

> ⚠️ 検証設計の前提（重要）: 1週内では「時間帯」と「型」が交絡するため、**同じ週の朝/昼/夜を直接比較しない**。
> 各型を週ごとに別の時間帯へローテーションし、**同じ型の時間帯差を週またぎで比較する**（設計の全体像は `data/ab_test_plan.csv`）。
> Week 1 はローテーションの基準（baseline）スロット。

| post_id | 型 | 時間帯（W1=baseline） | 次週の移動先 |
|---|---|---|---|
| week01-p1 | 問題提起 | 朝 08:00-09:30 | → 夜（W2） |
| week01-p3 | 失敗告白 | 朝 08:00-09:30 | → 昼（W2） |
| week01-p2 | あるある | 昼 12:00-13:00 | → 朝（W2） |
| week01-p4 | UIスクショ | 夜 21:00-22:30 | → 昼（W2） |
| week01-p5 | β募集 | 夜 21:00-22:30 | （隔週運用 / W3で朝） |

投稿後24〜48時間で `data/post_log.csv` に実績入力（`weekday` / `image_type` も必ず埋める）→ `python3 scripts/weekly_review.py` でセグメント別（型・時間帯・画像有無・曜日）に `profile_visit_rate` とフォロー転換率を集計する。

---

## post_log.csv 追記用テンプレ（投稿後に値を埋めて追記）

投稿前は以下を `data/post_log.csv` に追記しておき、24〜48時間後に impressions 以降の実績を埋める。
カラム順は `data/post_log.csv` のヘッダに準拠。

予約行は `data/post_log.csv` に登録済み。新カラム `image_type`（none/screenshot/card/mockup）と `weekday` も投稿前に埋める。投稿後は `npm run log` で実績を追記する（カラム順は自動整列されるので手書きより安全）:

```bash
npm run log -- --set post_id=week01-p1 status=posted \
  impressions=1200 engagements=90 profile_visits=48 follows_gained=3 \
  weekday=thu image_type=none
```

`profile_visit_rate` / `follow_rate` / `follow_conv_rate` / `quality_score` は自動計算される。
投稿が完了したら `status` を `scheduled` → `posted` に更新する。
