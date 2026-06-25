#!/usr/bin/env python3
import sys

BANNED = ["絶対勝てる", "勝率爆上げ", "誰でも稼げる", "必勝", "攻略法", "爆益", "最強", "革命"]
GOOD = ["判断", "記録", "見直", "台選び", "続行", "撤退", "感覚", "PachiTracker"]


def score(text: str):
    compact = text.replace("\n", "")
    score = 50
    reasons = []

    first = text.splitlines()[0] if text.splitlines() else ""
    if 8 <= len(first) <= 40:
        score += 15
        reasons.append("first_line_length_ok")
    if any(k in first for k in ["判断", "記録", "感覚", "負け", "台選び", "ヤメ"]):
        score += 10
        reasons.append("first_line_has_core_pain")
    if len(compact) <= 140:
        score += 10
        reasons.append("within_140")
    else:
        score -= 15
        reasons.append("over_140")
    if any(k in text for k in GOOD):
        score += 10
        reasons.append("pachitracker_connection")
    banned = [w for w in BANNED if w in text]
    if banned:
        score -= 40
        reasons.append("banned:" + ",".join(banned))
    if "PachiTracker" in text and text.find("PachiTracker") < len(text) * 0.5:
        score -= 5
        reasons.append("product_name_too_early")

    score = max(0, min(100, score))
    return score, reasons, len(compact)


def main():
    text = sys.stdin.read().strip()
    s, reasons, chars = score(text)
    print(f"score: {s}/100")
    print(f"chars: {chars}")
    print("reasons:")
    for r in reasons:
        print(f"- {r}")

if __name__ == "__main__":
    main()
