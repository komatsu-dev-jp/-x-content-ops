#!/usr/bin/env python3
"""禁止表現の共有リスト（validate_post.py / score_posts.py から import する）。

正典は prompts/banned-patterns.md。ここは同じリストをスクリプトから使うための
Python化版。banned-patterns.md を更新したら、このファイルも合わせて更新する
（Markdownはプロンプト用、ここはコード用で、フォーマットが違うため自動同期はできない）。
"""

BANNED = [
    "絶対勝てる",
    "勝率爆上げ",
    "誰でも稼げる",
    "パチンコで生活できる",
    "必勝",
    "攻略法",
    "爆益",
    "最強",
    "革命",
    "人生変わる",
    "今すぐ登録",
    "これを使わない人は損",
    "勝ち組になれる",
    "期待値だけで勝てる",
    "これだけで収支改善",
    "他アプリより確実に優秀",
]

# 実在の機種名・雑誌名など、禁止語を含むが問題ない固有名詞。
# その固有名詞が本文に含まれていれば、対応する禁止語の誤検知としてスキップする。
SAFE_CONTEXTS = {
    "革命": ["革命機ヴァルヴレイヴ"],
    "必勝": ["パチンコ必勝ガイド", "必勝ガイド", "必勝本"],
}


def find_flags(text: str):
    """text中の禁止語を検出する。SAFE_CONTEXTSに該当する固有名詞由来の出現は除外する。"""
    flags = []
    for word in BANNED:
        idx = text.find(word)
        if idx == -1:
            continue
        safe_ctxs = SAFE_CONTEXTS.get(word, [])
        if any(ctx in text for ctx in safe_ctxs):
            continue
        flags.append(word)
    return flags
