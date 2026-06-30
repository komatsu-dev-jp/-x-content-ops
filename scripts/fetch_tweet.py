#!/usr/bin/env python3
"""ターゲットX投稿の本文を best-effort で取得する補助スクリプト。

x-reply-outreach Skill 用。X本体は未ログインだと 403 を返すため、
公開ミラー（fxtwitter / vxtwitter）のJSON APIを順に試す。
どれも取れなければ「取得不可」を返すので、Skill側は本文の貼付を依頼すること。

使い方:
    python3 scripts/fetch_tweet.py https://x.com/<user>/status/<id>

ネットワーク制限のある環境では取得できないことがある（その場合は本文を手で貼る）。
依存はPython標準ライブラリのみ。追加課金・外部SaaSなし。
"""
import json
import re
import sys
import urllib.error
import urllib.request

MIRRORS = ["api.fxtwitter.com", "api.vxtwitter.com"]
UA = "Mozilla/5.0 (compatible; pachitracker-reply-outreach/1.0)"


def extract_id(url: str):
    m = re.search(r"/status(?:es)?/(\d+)", url)
    return m.group(1) if m else None


def try_mirror(host: str, tweet_id: str):
    api = f"https://{host}/status/{tweet_id}"
    req = urllib.request.Request(api, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8", "replace")
    data = json.loads(raw)
    tw = data.get("tweet") or data  # fxtwitter:{tweet:{...}} / vxtwitter:{...}
    text = tw.get("text") or tw.get("full_text") or ""
    author = tw.get("author") or {}
    name = author.get("screen_name") or author.get("user_screen_name") or tw.get("user_screen_name") or ""
    media = tw.get("media") or {}
    has_media = bool(media.get("all") or media.get("photos") or media.get("videos") or tw.get("mediaURLs"))
    if not text:
        raise ValueError("empty text")
    return {"author": name, "text": text, "has_media": has_media, "via": host}


def main():
    if len(sys.argv) < 2:
        print("usage: python3 scripts/fetch_tweet.py <tweet_url>", file=sys.stderr)
        sys.exit(2)
    url = sys.argv[1].strip()
    tweet_id = extract_id(url)
    if not tweet_id:
        print(json.dumps({"ok": False, "reason": "URLからツイートIDを抽出できませんでした"}, ensure_ascii=False))
        return
    errors = []
    for host in MIRRORS:
        try:
            result = try_mirror(host, tweet_id)
            print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
            return
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, json.JSONDecodeError, OSError) as e:
            errors.append(f"{host}: {e}")
    print(json.dumps({
        "ok": False,
        "reason": "取得不可。X本体は未ログインだと403、ミラーもネットワーク制限で届かない場合があります。"
                  "投稿本文をコピペして渡してください。",
        "tried": errors,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
