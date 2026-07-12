# Weekly X Review

> 重点KPI: profile_visit_rate → follow_conv_rate（= follows_gained / profile_visits）
> ⚠️ 1週内の朝/昼/夜は型と交絡するので直接比較しない。型×時間帯（週またぎ）で判断する。
> ⚠️ 今週の投稿は全て impressions<500（最大160）。**生rateでの勝敗断定はしない**。経験ベイズ縮小率（prior=0.0018, K=500）でのランキングを参考値として扱う。

## 期間

2026-06-23 〜 2026-06-30（+ 参考: 6/20固定ポスト分を追加登録）

## 今週の投稿数

- 投稿数: 8件（week00-p0, week00-p1, week01-p1, week01-p2, week01-p2b, week01-p3, week01-p4, week01-p4b, week01-p5）※p2b/p4b/p0はスクショのみでpost_log未記録だった投稿を追加登録
- 画像あり / なし: screenshot 1件（week01-p4 UIスクショ型） / none 5件 / 未設定2件
- β導線あり: week01-p5（β募集型, night）

## 上位投稿（quality_score順・参考値）

| rank | post_id | post_type | time_slot | pv_rate | follow_conv | why_won |
|---|---|---|---|---:|---:|---|
| 1 | week01-p4 | UIスクショ型 | night | 0.0145 | - | 今週最高のpv_rate（1/69）。imp=69で低n。画像=screenshotの唯一の投稿 |
| 2 | week01-p2 | あるある型 | noon | 0.0120 | - | pv 1/83。低n |
| 3 | week01-p4b | （未設定・記憶バイアス系） | - | 0.0000 | - | likes=2と反応はあるがpv=0。post_log未記録だった投稿を追加 |
| 4 | week00-p0 | 問題提起型 | - | 0.0000 | - | 6/20の固定ポスト。imp=277と今回登録分で最多だがpv=0。post_log未記録だった投稿を追加 |
| 5 | week01-p1 | 問題提起型 | morning | 0.0000 | - | 印象数は107まで伸びたがpv=0 |

縮小率（信頼度補正）順でもweek01-p4（UIスクショ型・night, shrunk_pv=0.0037）が僅差で最上位、僅差でweek01-p2（あるある型・noon, shrunk_pv=0.0036）が続く。どちらもn=1・imp<100で「低n」のため**勝ち確定ではなく仮説**として扱う。UIスクショ型は唯一の画像投稿でもあり、「型」と「画像あり」が交絡している点に注意（画像の効果か型の効果か本データだけでは分離できない）。

## 下位投稿

| rank | post_id | post_type | time_slot | quality_score | why_lost |
|---|---|---|---|---:|---|
| 1 | week01-p3 | 失敗告白型 | morning | 0.00 | pv/likes/repost全て0。impressions=53と母数も小さい |
| 2 | week00-p1 | 失敗告白型 | - | 0.00 | pv=0、time_slot未記録 |
| 3 | week01-p2b | （台選び系） | - | 0.00 | impressions=160とこの週で最多だがpv=0 |

## セグメント別平均（pv_rate / follow_conv_rate）

- 型別: あるある型のみpv_rate>0（0.0120, n=1）。他の型は全てpv_rate=0（n=1〜2ずつ）
- 時間帯別（※型と交絡。参考）: noon(n=1)のみpv_rate>0、morning/night(各n=2)は0
- 画像タイプ別: none(n=4)がpv_rate=0.0040、screenshot(n=1)は0
- 曜日別: fri(n=1, week01-p2)のみpv_rate>0

## 型×時間帯（同型の週またぎ比較）

| post_type | morning | noon | night | 暫定の勝ちスロット |
|---|---|---|---|---|
| 問題提起型 | 0.0000(n=1) | - | - | 要追加データ |
| あるある型 | - | 0.0120(n=1) | - | 要追加データ |
| 失敗告白型 | 0.0000(n=1) | - | - | 要追加データ |
| UIスクショ型 | - | - | -(n=1, 未取得) | 要追加データ |
| β募集型 | - | - | -(n=1, 未取得) | 要追加データ |

各セルn=1のため、まだ「型×時間帯」の比較は成立しない（週またぎで同型を複数スロットに置いて初めて判定可能）。

## 勝ちフック / 負けパターン

- 勝ち: 現時点では「勝ちフック」と断定できる型・パターンはない（全投稿n<500、profile_visitが発生したのは1件のみ）
- 負け: 特定の負けパターンも断定不可。台選び系（week01-p2b, imp=160）はimpressionsは伸びてもpv=0だった点だけは観測事実として記録

## 次週の仮説（1つだけ）

```text
あるある型はnoonでprofile_visit_rateが他枠より高い可能性がある（今週唯一の遷移がnoon×あるある型、n=1のため検証不足）。
検証法: 次週もあるある型をnoonに配置して再現性を確認する（data/ab_test_plan.csvのW2行=morning予定だったが、再現性確認のためnoon維持を検討）。
```

**追記の観察（仮説変更はせず記録のみ）**: week01-p4（UIスクショ型・night）が僅差で今週最高のpv_rateだった。ただしn=1・screenshot画像も唯一のためあるある型の仮説と競合はしない。次々週以降、UIスクショ型を複数回投稿して型×画像あり/なしの再現性も別途検証したい。

## 更新するファイル

- [x] data/ab_test_plan.csv（あるある型の行にメモ追記）
- [ ] prompts/post-patterns.md（勝ちフック未確定のため今回は更新しない）
- [ ] prompts/banned-patterns.md（負けパターン未確定のため今回は更新しない）
- [ ] docs/integrated-strategy.md（変更なし）

## 補足: インプレッション500未満問題について

今週の投稿は全てimpressions<500（最大160）。これは現時点のフォロワー規模・初動拡散力では想定内の数字。対応方針:

1. **個別の投稿を「勝ち/負け」と断定しない** — n<500は偶然のブレが支配的（`prompts/scoring-rubric.md`の統計ルール）
2. **ランキングは縮小率で行う** — `npm run weekly`が自動算出。生rateだけで判断しない
3. **主軸はprofile_visit_rate→follow_conv_rate** — impressionsの絶対量より「来た人が次の行動を取ったか」を見る
4. **型×時間帯を週をまたいで蓄積する** — 1週間では交絡するため、同型を複数週・複数スロットに置いて初めて比較可能になる。今は「要追加データ」の段階
5. **リプ周り（こちらは別途tier別に追跡中）でプロフィール流入経路を太くする** — 投稿単体のオーガニックimpressionsが小さい初期段階では、リプ経由の流入が相対的に効く
