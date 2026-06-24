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
記録して後で見直すと、わりと冷静になれる。
```

- post_type: あるある型
- char_count: 83（140字以内 ✅）
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

台選び・続行・撤退を、その場で一押し。

#個人開発
```

- post_type: UIスクショ型
- char_count: 88（140字以内 ✅）
- score: 90/100（validate: pass）
- breakdown: 1行目フック○ / 痛点（入力負担）○ / PachiTracker接続○ / プロフィール遷移期待◎（実画面）/ リスク 低
- risk_flags: `none`（※採点スクリプトの `product_name_too_early` はスタイル上の軽微指摘。本文構造上、問題なしと判断）
- recommended_time_slot: **夜 21:00〜22:30**（UI相談・実戦者枠）
- image_suggestion: **記録画面のスクショ必須**（店舗名・個人情報・他社UI流用・未実装機能の写り込みがないか確認）
- reply_templates:
  1. （深掘り）「実戦中だと何タップで入れたいですか？ 一押しでも多いと感じる場面ありますか？」
  2. （UI相談返信）「ありがとうございます。見た目より『迷わず押せるか』を優先したいので、その視点で調整してみます。」

---

## Post 5｜6/30(火) — β募集型（Lane F）

```
パチンコの台選び・続行・撤退を、感覚じゃなく記録で見直したい人へ。

PachiTrackerのβ版を、少人数で触ってもらう準備をしています。

あとで判断を振り返れる部分から試せます。
```

- post_type: β募集型
- char_count: 89（140字以内 ✅）
- score: 90/100（validate: pass）
- breakdown: 対象明確○ / 痛点接続○ / 控えめCTA○（Phase 0は煽らない）/ リスク 低
- risk_flags: `none`（※採点スクリプトの `product_name_too_early` はスタイル上の軽微指摘。募集文として許容）
- recommended_time_slot: **夜 21:00〜22:30**（β募集枠）
- image_suggestion: なし、または判断ログ画面のスクショ
- reply_templates:
  1. （β候補への返信）「ありがとうございます。準備でき次第ご案内します。台選び・続行・撤退の振り返り部分から試してもらう予定です。」
  2. （深掘り）「ちなみに今、振り返りで一番モヤつくのはどの判断ですか？ β版の優先順位の参考にさせてください。」

---

## 時間帯A/Bの割り当て（今週の検証設計）

| post_id | 型 | 時間帯 | 検証狙い |
|---|---|---|---|
| week01-p1 | 問題提起 | 朝 08:00-09:30 | 朝の思想系の遷移率 |
| week01-p3 | 失敗告白 | 朝 08:00-09:30 | 朝の開発系の遷移率 |
| week01-p2 | あるある | 昼 12:00-13:00 | 昼の軽い投稿の遷移率 |
| week01-p4 | UIスクショ | 夜 21:00-22:30 | 夜の実戦者向け遷移率 |
| week01-p5 | β募集 | 夜 21:00-22:30 | 夜のβ反応 |

朝2 / 昼1 / 夜2 で全3枠をカバー。投稿後24〜48時間で `data/post_log.csv` に実績入力 → `python3 scripts/weekly_review.py` で勝ち時間帯を判定する。

---

## post_log.csv 追記用テンプレ（投稿後に値を埋めて追記）

投稿前は以下を `data/post_log.csv` に追記しておき、24〜48時間後に impressions 以降の実績を埋める。
カラム順は `data/post_log.csv` のヘッダに準拠。

```csv
2026-06-25,week01-p1,scheduled,判断ミス,問題提起型,memory_bias,FALSE,FALSE,FALSE,2,morning,102,昨日出ていた台に今日も座ってしまう,soft,,,,,,,,,,,,,,,
2026-06-26,week01-p2,scheduled,撤退判断,あるある型,relatable,FALSE,FALSE,FALSE,0,noon,83,これやりがち,none,,,,,,,,,,,,,,,
2026-06-27,week01-p3,scheduled,継続設計,失敗告白型,confession,FALSE,FALSE,FALSE,0,morning,100,記録アプリを自分で作ってるのに入力をサボった,soft,,,,,,,,,,,,,,,
2026-06-29,week01-p4,scheduled,UI,UIスクショ型,pain_hook,TRUE,FALSE,FALSE,1,night,88,入力が面倒だと楽な判断を選ぶ,soft,,,,,,,,,,,,,,,
2026-06-30,week01-p5,scheduled,β募集,β募集型,target_call,FALSE,FALSE,FALSE,0,night,89,記録で見直したい人へ,beta,,,,,,,,,,,,,,,
```

投稿が完了したら `status` を `scheduled` → `posted` に更新する。
