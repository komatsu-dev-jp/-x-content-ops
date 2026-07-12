#!/usr/bin/env python3
"""投稿候補のヒューリスティック採点（stdin入力）。

prompts/scoring-rubric.md の7項目配点（100点満点）に沿って部分点を出す。
機械的なキーワード一致による下限チェックであり、読者の痛みの具体性・自然さ・
トーンの妥当性までは判定できない。最終判断は x-score-post Skill（AI/人間の判断）を正とする。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from banned_words import find_flags  # noqa: E402

PAIN_WORDS = ["台選び", "続行", "撤退", "記録", "記憶", "感覚", "入力", "判断"]
CONNECTION_WORDS = ["判断ログ", "PachiTracker", "記録", "見直"]
HARD_SELL = ["今すぐ", "使えば", "登録して", "ダウンロードして", "絶対に"]
CURIOSITY_ENDINGS = ["作っています", "作っている", "開発", "予定です", "試してもらう"]

MAX = {
    "first_line_hook": 20,
    "pain_specificity": 20,
    "pachitracker_connection": 15,
    "profile_visit_potential": 15,
    "low_sales_smell": 10,
    "risk_safety": 10,
    "readability": 10,
}


def score_first_line_hook(first_line: str):
    s, reasons = 0, []
    n = len(first_line)
    if 8 <= n <= 40:
        s += 12
        reasons.append("first_line_length_ok")
    elif n > 0:
        s += 4
        reasons.append("first_line_length_suboptimal")
    if any(k in first_line for k in PAIN_WORDS + ["負け", "ヤメ", "ブレ"]):
        s += 8
        reasons.append("first_line_has_pain_hook")
    return min(s, MAX["first_line_hook"]), reasons


def score_pain_specificity(text: str):
    hits = [w for w in PAIN_WORDS if w in text]
    s = min(len(hits) * 7, MAX["pain_specificity"])
    reasons = [f"pain_hit:{w}" for w in hits] or ["no_pain_word"]
    return s, reasons


def score_connection(text: str):
    hits = [w for w in CONNECTION_WORDS if w in text]
    s = min(len(hits) * 6, MAX["pachitracker_connection"])
    reasons = [f"connection_hit:{w}" for w in hits] or ["no_connection"]
    return s, reasons


def score_profile_visit_potential(text: str):
    s, reasons = 0, []
    if any(k in text for k in CURIOSITY_ENDINGS):
        s += 10
        reasons.append("curiosity_gap_present")
    if "？" in text or "?" in text:
        s += 5
        reasons.append("question_present")
    return min(s, MAX["profile_visit_potential"]), reasons


def score_low_sales_smell(text: str):
    hits = [w for w in HARD_SELL if w in text]
    if hits:
        return max(MAX["low_sales_smell"] - 5 * len(hits), 0), [f"hard_sell:{w}" for w in hits]
    return MAX["low_sales_smell"], ["no_hard_sell"]


def score_risk_safety(text: str):
    flags = find_flags(text)
    if flags:
        return 0, [f"banned:{w}" for w in flags]
    return MAX["risk_safety"], ["no_banned_words"]


def score_readability(text: str):
    s, reasons = 0, []
    if len(text) <= 140:
        s += 6
        reasons.append("within_140")
    else:
        reasons.append("over_140")
    hashtags = text.count("#")
    if hashtags <= 2:
        s += 2
        reasons.append("hashtags_ok")
    else:
        reasons.append("hashtags_excessive")
    if "\n" in text:
        s += 2
        reasons.append("has_line_breaks")
    return min(s, MAX["readability"]), reasons


def score(text: str):
    first_line = text.splitlines()[0] if text.splitlines() else ""
    breakdown = {}
    reasons = []

    for key, fn in [
        ("first_line_hook", lambda: score_first_line_hook(first_line)),
        ("pain_specificity", lambda: score_pain_specificity(text)),
        ("pachitracker_connection", lambda: score_connection(text)),
        ("profile_visit_potential", lambda: score_profile_visit_potential(text)),
        ("low_sales_smell", lambda: score_low_sales_smell(text)),
        ("risk_safety", lambda: score_risk_safety(text)),
        ("readability", lambda: score_readability(text)),
    ]:
        pts, rs = fn()
        breakdown[key] = pts
        reasons.extend(rs)

    total = sum(breakdown.values())
    return total, breakdown, reasons, len(text)


def main():
    text = sys.stdin.read().strip()
    total, breakdown, reasons, chars = score(text)
    print(f"score: {total}/100")
    print(f"chars: {chars}")
    print("breakdown:")
    for k, v in breakdown.items():
        print(f"- {k}: {v}/{MAX[k]}")
    print("reasons:")
    for r in reasons:
        print(f"- {r}")
    print("\n⚠️ これは機械的な下限チェック（キーワード一致ベース）。読者の痛みの具体性・自然さ・"
          "トーンの妥当性は x-score-post Skill（AIの読解）または人間の判断を優先すること。")


if __name__ == "__main__":
    main()
