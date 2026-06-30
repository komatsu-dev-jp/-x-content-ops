#!/usr/bin/env python3
"""本日のタスク進捗を実数つきで Slack に通知する（任意機能）。

自動投稿はしない。本日の進捗（npm run today と同じ集計）を Slack の Incoming Webhook に
送るだけ。追加課金なし（Slack無料プランのwebhookで動く）。依存は標準ライブラリのみ。

webhook URL の渡し方（機密。コミットしない）:
  1) 環境変数 SLACK_WEBHOOK_URL  ← 推奨
  2) config/slack_webhook.txt に貼る（.gitignore 済み）

使い方:
  python3 scripts/notify_slack.py          # 現在の進捗をSlackへ送信
  npm run notify
  npm run today -- --done like count=5 --notify   # 記録と同時に送信
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import daily_tracker as dt  # noqa: E402

WEBHOOK_FILE = Path("config/slack_webhook.txt")
SETUP_HINT = (
    "設定方法: 環境変数 SLACK_WEBHOOK_URL に webhook URL を入れるか、"
    "config/slack_webhook.txt に貼ってください（gitignore済み・コミットされません）。\n"
    "webhook URL は Slack の Incoming Webhooks（無料）で発行できます。"
)


def resolve_webhook():
    url = (os.environ.get("SLACK_WEBHOOK_URL") or "").strip()
    if url:
        return url
    if WEBHOOK_FILE.exists():
        url = WEBHOOK_FILE.read_text(encoding="utf-8").strip()
        if url and not url.startswith("#"):
            return url
    return None


def build_message(st):
    lines = [f"*📅 本日のタスク ({st['date']})*"]
    for t in st["tasks"]:
        if t["goal"] <= 0:
            continue
        if t["done"] >= t["goal"]:
            lines.append(f"• {t['label']} {t['done']}/{t['goal']} ✅")
        else:
            lines.append(f"• {t['label']} {t['done']}/{t['goal']}（あと{t['goal'] - t['done']}件）")
    remain = st["goal_total"] - st["done_total"]
    if remain <= 0 and st["goal_total"] > 0:
        lines.append(f"*合計 {st['done_total']}/{st['goal_total']} 🎉 本日達成！*")
    else:
        lines.append(f"*合計 {st['done_total']}/{st['goal_total']} — 残り{remain}件*")
    return "\n".join(lines)


def send(url, text):
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status


def run():
    st = dt.compute_status()
    text = build_message(st)
    url = resolve_webhook()
    if not url:
        print("⚠️ Slack webhook URL が未設定です。送信せず内容だけ表示します:\n")
        print(text)
        print("\n" + SETUP_HINT)
        return False
    try:
        send(url, text)
        print("✅ Slackに送信しました:\n")
        print(text)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"❌ Slack送信失敗: {e}\n内容:\n{text}")
        return False


if __name__ == "__main__":
    run()
