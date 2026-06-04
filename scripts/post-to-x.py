#!/usr/bin/env python3
"""
Notionの「X投稿スケジュール｜PachiTracker」データベースを読み込み、
今日の投稿（ステータス=予定）をX（Twitter）に自動投稿する。
投稿後はNotionのステータスを「投稿済み」に更新する。

必要な環境変数:
  NOTION_TOKEN           - Notion API トークン
  NOTION_DATABASE_ID     - NotionデータベースID
  X_API_KEY              - X API Key (Consumer Key)
  X_API_SECRET           - X API Secret (Consumer Secret)
  X_ACCESS_TOKEN         - X Access Token
  X_ACCESS_TOKEN_SECRET  - X Access Token Secret
"""

import os
import sys
from datetime import datetime, timezone, timedelta

import requests
import tweepy

# ─── 設定 ─────────────────────────────────────────────────
JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y-%m-%d")

NOTION_TOKEN       = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type":  "application/json",
    "Notion-Version": "2022-06-28",
}

# ─── Notion: 今日の「予定」投稿を取得 ──────────────────────
def get_today_posts():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    payload = {
        "filter": {
            "and": [
                {"property": "投稿日",    "date":   {"equals": TODAY}},
                {"property": "ステータス", "select": {"equals": "予定"}},
            ]
        },
        "sorts": [{"property": "投稿日", "direction": "ascending"}],
    }
    res = requests.post(url, headers=NOTION_HEADERS, json=payload)
    res.raise_for_status()
    return res.json().get("results", [])


def extract_post(page):
    props = page["properties"]
    title_parts = props.get("投稿タイトル", {}).get("title", [])
    body_parts  = props.get("投稿本文",   {}).get("rich_text", [])
    title = "".join(t["plain_text"] for t in title_parts)
    body  = "".join(t["plain_text"] for t in body_parts)
    return page["id"], title, body


# ─── Notion: ステータスを「投稿済み」に更新 ─────────────────
def mark_as_posted(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": {"ステータス": {"select": {"name": "投稿済み"}}}}
    res = requests.patch(url, headers=NOTION_HEADERS, json=payload)
    res.raise_for_status()


# ─── X API クライアント ──────────────────────────────────
def get_x_client():
    return tweepy.Client(
        consumer_key        = os.environ["X_API_KEY"],
        consumer_secret     = os.environ["X_API_SECRET"],
        access_token        = os.environ["X_ACCESS_TOKEN"],
        access_token_secret = os.environ["X_ACCESS_TOKEN_SECRET"],
    )


# ─── メイン ─────────────────────────────────────────────
def main():
    print(f"[{TODAY}] 投稿チェック開始")

    posts = get_today_posts()
    if not posts:
        print("今日の予定投稿はありません。")
        return

    client = get_x_client()

    for page in posts:
        page_id, title, body = extract_post(page)
        if not body.strip():
            print(f"  スキップ（本文なし）: {title}")
            continue

        print(f"  投稿: {title}")
        print(f"  本文: {body[:50]}...")

        try:
            response = client.create_tweet(text=body)
            tweet_id = response.data["id"]
            print(f"  ✅ 投稿成功 tweet_id={tweet_id}")
            mark_as_posted(page_id)
            print(f"  ✅ Notionステータスを「投稿済み」に更新")
        except tweepy.TweepyException as e:
            print(f"  ❌ 投稿失敗: {e}", file=sys.stderr)
            sys.exit(1)

    print("完了")


if __name__ == "__main__":
    main()
