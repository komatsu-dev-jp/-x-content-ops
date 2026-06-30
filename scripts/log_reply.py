#!/usr/bin/env python3
"""data/reply_outreach_log.csv へのリプ周り記録（追加課金なし・ローカルCSVのみ）。

tier はNotionの「対象比率」基準:
  A = 500〜5,000フォロワーの濃い収支・期待値垢（目標50%）
  B = 5,000〜50,000の中堅アカウント（目標30%、5万〜10万もBに含む）
  C = 10万超・万人アカウント（目標20%）
follow/profile_visit/got_reply は送信直後は空でよく、後日 --update で追記する。

アカウント別フォロワー数は data/account_tiers.csv に登録しておくと、
同じアカウントへの2回目以降のリプで tier を省略しても自動参照される。

使い方:
  # アカウントのフォロワー数を登録（tierは自動計算）
  python3 scripts/log_reply.py --set-account handle=matutakenet followers=14113

  # 送信直後に記録（tier省略時はaccount_tiers.csvから自動参照。なければ未設定）
  python3 scripts/log_reply.py --add target_url=https://x.com/matutakenet/status/123 \
      archetype=同意+一歩 note=期待値vs展開

  # 後日、反応が分かったら同じ target_url で更新
  python3 scripts/log_reply.py --update target_url=https://x.com/matutakenet/status/123 \
      got_reply=1 profile_visit=1 follow=0
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

LOG = Path("data/reply_outreach_log.csv")
ACCOUNTS = Path("data/account_tiers.csv")
ACCOUNT_COLS = ["handle", "followers", "tier", "updated", "note"]
COLS = ["date", "target_url", "tier", "archetype", "got_reply", "profile_visit", "follow", "note"]
VALID_TIERS = {"A", "B", "C"}


def today():
    return date.today().isoformat()


def followers_to_tier(followers):
    """500未満は floor 例外としてAに含める（フラグはset_accountの表示側で出す）。
    50,000〜100,000未満はNotion表の隙間なのでBに含める。"""
    if followers >= 100_000:
        return "C"
    if followers >= 5_000:
        return "B"
    return "A"


def extract_handle(target_url):
    m = re.search(r"(?:x\.com|twitter\.com)/([A-Za-z0-9_]+)", target_url or "")
    return m.group(1) if m else None


def load_accounts():
    if not ACCOUNTS.exists():
        return []
    return list(csv.DictReader(ACCOUNTS.open(encoding="utf-8")))


def save_accounts(rows):
    with ACCOUNTS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ACCOUNT_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in ACCOUNT_COLS})


def lookup_tier(target_url):
    """target_url からハンドルを推定し、account_tiers.csv に登録があればtierを返す。"""
    handle = extract_handle(target_url)
    if not handle:
        return ""
    for r in load_accounts():
        if (r.get("handle") or "").lstrip("@").lower() == handle.lower():
            return r.get("tier") or ""
    return ""


def set_account(argv):
    data = {}
    for p in argv[argv.index("--set-account") + 1:]:
        if p.startswith("--"):
            break
        if "=" not in p:
            sys.exit(f"bad pair (need key=value): {p}")
        k, v = p.split("=", 1)
        data[k.strip()] = v.strip()
    if "handle" not in data or "followers" not in data:
        sys.exit("usage: --set-account handle=<@なし> followers=<数値>")
    handle = data["handle"].lstrip("@")
    try:
        followers = int(data["followers"])
    except ValueError:
        sys.exit(f"followers は整数で指定してください: {data['followers']}")
    tier = followers_to_tier(followers)

    rows = load_accounts()
    target = next((r for r in rows if (r.get("handle") or "").lower() == handle.lower()), None)
    if target is None:
        target = {c: "" for c in ACCOUNT_COLS}
        rows.append(target)
    target.update({"handle": handle, "followers": str(followers), "tier": tier, "updated": today()})
    save_accounts(rows)

    floor_note = ""
    if followers < 500:
        floor_note = "（500未満。tier表のA下限より小さいので暫定でAに分類）"
    print(f"✅ {handle}: followers={followers} → tier={tier} を登録{floor_note}")


def parse_pairs(argv, mode_flag):
    pairs = argv[argv.index(mode_flag) + 1:]
    data = {}
    for p in pairs:
        if "=" not in p:
            sys.exit(f"bad pair (need key=value): {p}")
        k, v = p.split("=", 1)
        data[k.strip()] = v.strip()
    if "target_url" not in data:
        sys.exit("target_url is required")
    unknown = [k for k in data if k not in COLS]
    if unknown:
        sys.exit(f"unknown keys: {unknown} (使えるのは {[c for c in COLS if c != 'date']})")
    if data.get("tier") and data["tier"] not in VALID_TIERS:
        sys.exit(f"tier は A/B/C のいずれか（500-5000=A, 5000-50000=B, 10万超=C）")
    return data


def load_rows():
    if not LOG.exists():
        return []
    return list(csv.DictReader(LOG.open(encoding="utf-8")))


def save_rows(rows):
    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})


def append_row(record_date, target_url, tier="", archetype="", note=""):
    """他スクリプト（daily_tracker.py の --done reply）からも呼べる共通追記処理。
    tier省略時は account_tiers.csv にハンドル登録があれば自動で引く。"""
    if tier and tier not in VALID_TIERS:
        sys.exit("tier は A/B/C のいずれか（500-5000=A, 5000-50000=B, 10万超=C）")
    if not tier:
        tier = lookup_tier(target_url)
    row = {c: "" for c in COLS}
    row.update({"date": record_date, "target_url": target_url, "tier": tier,
                "archetype": archetype, "note": note})
    rows = load_rows()
    rows.append(row)
    save_rows(rows)
    return row


def add(argv):
    data = parse_pairs(argv, "--add")
    row = append_row(today(), data["target_url"], data.get("tier", ""),
                      data.get("archetype", ""), data.get("note", ""))
    tier_note = "（tier未設定。後で --update で埋められます）" if not row.get("tier") else ""
    print(f"✅ 記録: {row['target_url']} tier={row.get('tier') or '?'} {tier_note}")


def update(argv):
    data = parse_pairs(argv, "--update")
    rows = load_rows()
    target = next((r for r in reversed(rows) if r.get("target_url") == data["target_url"]), None)
    if target is None:
        sys.exit(f"target_url が見つかりません: {data['target_url']}（先に --add してください）")
    target.update({k: v for k, v in data.items() if k != "target_url"})
    save_rows(rows)
    print(f"✅ 更新: {data['target_url']}")


def main():
    argv = sys.argv[1:]
    if "--add" in argv:
        add(argv)
    elif "--update" in argv:
        update(argv)
    elif "--set-account" in argv:
        set_account(argv)
    else:
        sys.exit("usage: --add target_url=... [tier=A/B/C archetype=... note=...]\n"
                 "       --update target_url=... [tier=A/B/C got_reply=1 profile_visit=1 follow=1]\n"
                 "       --set-account handle=... followers=...")


if __name__ == "__main__":
    main()
