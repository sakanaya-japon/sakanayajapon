#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_old_url.py — Organization 移管後に残っている旧 Pages URL を差し替える

使い方（sakanayajapon リポジトリのルートで実行）:
    python fix_old_url.py            # 確認モード（既定）。何も書き換えない
    python fix_old_url.py --apply    # 実際に書き換える

やること:
  1. サイト本体（*.html と assets/ 配下の .js / .css）にある旧URLを新URLへ置換
     → OGP の og:image / og:url が対象。docs/ は移管の経緯を残すため触らない
  2. README.md の「公開URL」2行を移管後の表記に更新
  3. index.html の「移管後は差し替えること」というコメントを差し替え済みに更新
  4. docs/github-inventory.md の棚卸し表 3行目の状態を「移管済」に更新

安全策:
  - 既定は確認モード。--apply を付けない限りファイルは変更しない
  - 2〜4 は完全一致した場合だけ置換。見つからなければ「手動確認」と表示し、成功扱いにしない
  - 改行コード（LF / CRLF）と UTF-8（BOMなし）を保持する
  - 書き換え後に再スキャンし、対象ファイルに旧URLが残っていたら終了コード 1
"""

import argparse
import re
import sys
from pathlib import Path

OLD_URL_RE = re.compile(r"https://sasuraimitsu\.github\.io/sakanayajapon", re.IGNORECASE)
NEW_URL = "https://sakanaya-japon.github.io/sakanayajapon"

# サイト本体として走査する対象（docs/ と .git/ は除外）
SITE_GLOBS = ["*.html", "business/**/*.html", "assets/**/*.js", "assets/**/*.css"]
EXCLUDE_DIRS = {".git", "docs", "node_modules", "__pycache__"}

# 完全一致で置換する箇所: (ファイル, 旧文字列, 新文字列, 説明)
# ※ 改行は LF で書く。CRLF のファイルは実行時に自動で合わせる
EXACT_EDITS = [
    (
        "README.md",
        "- 公開URL: https://sasuraimitsu.github.io/sakanayajapon/\n"
        "  （`sakanaya-japon` Organization への移管後は `https://sakanaya-japon.github.io/sakanayajapon/`）\n",
        "- 公開URL: https://sakanaya-japon.github.io/sakanayajapon/\n"
        "  （2026-09 に個人アカウント `Sasuraimitsu` から Organization へ移管済み。"
        "旧URL `sasuraimitsu.github.io/sakanayajapon/` は移管により無効。移転案内は docs/github-inventory.md §3 手順3）\n",
        "README の公開URL",
    ),
    (
        "index.html",
        "※ Organization 移管後は下記2行のURLを差し替えること（docs/github-inventory.md §3）",
        "※ 2026-09 の Organization 移管に合わせて差し替え済み（docs/github-inventory.md §3）",
        "index.html の OGP コメント",
    ),
    (
        "docs/github-inventory.md",
        "| 3 | `Sasuraimitsu/sakanayajapon` | 個人向けサイト（本リポジトリ） | 2026-06-15 | **Org へ移管** |",
        "| 3 | `Sasuraimitsu/sakanayajapon` | 個人向けサイト（本リポジトリ） | 2026-06-15 | "
        "✅ **Org へ移管済**（`sakanaya-japon/sakanayajapon`） |",
        "棚卸し表 3行目の状態",
    ),
]


def read_text(path: Path) -> str:
    # newline="" で改行コードをそのまま保持する
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def site_files(root: Path):
    seen = set()
    for pattern in SITE_GLOBS:
        for p in sorted(root.glob(pattern)):
            if not p.is_file() or p in seen:
                continue
            if any(part in EXCLUDE_DIRS for part in p.relative_to(root).parts):
                continue
            seen.add(p)
            yield p


def main() -> int:
    ap = argparse.ArgumentParser(description="旧 Pages URL を新URLへ差し替える")
    ap.add_argument("--apply", action="store_true", help="実際に書き換える（省略時は確認のみ）")
    ap.add_argument("--root", default=".", help="リポジトリのルート（既定: カレント）")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not (root / "index.html").is_file() or not (root / "assets" / "js" / "site-info.js").is_file():
        print(f"[中止] {root} は sakanayajapon リポジトリのルートではなさそうです。"
              "index.html と assets/js/site-info.js が見つかりません。", file=sys.stderr)
        return 2

    mode = "書き換えモード" if args.apply else "確認モード（ファイルは変更しません）"
    print(f"== {mode} ==  root: {root}\n")

    errors = 0
    pending = {}  # path -> 新しい内容（同じファイルへの複数編集をまとめる）

    def current(path: Path) -> str:
        return pending[path] if path in pending else read_text(path)

    # --- 1. サイト本体の旧URL ---
    print("[1] サイト本体の旧URL")
    url_hits = 0
    for p in site_files(root):
        try:
            text = current(p)
        except (OSError, UnicodeDecodeError) as e:
            print(f"  [読込失敗] {p.relative_to(root)}: {e}")
            errors += 1
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if OLD_URL_RE.search(line):
                url_hits += 1
                print(f"  {p.relative_to(root)}:{lineno}: {line.strip()[:120]}")
        new_text = OLD_URL_RE.sub(NEW_URL, text)
        if new_text != text:
            pending[p] = new_text
    if url_hits == 0:
        print("  旧URLは見つかりませんでした（差し替え済み）")
    print()

    # --- 2〜4. 完全一致の置換 ---
    print("[2] 完全一致で更新する箇所")
    for rel, old, new, label in EXACT_EDITS:
        p = root / rel
        if not p.is_file():
            print(f"  [手動確認] {label}: {rel} がありません")
            errors += 1
            continue
        try:
            text = current(p)
        except (OSError, UnicodeDecodeError) as e:
            print(f"  [読込失敗] {rel}: {e}")
            errors += 1
            continue
        # CRLF のファイルなら検索・置換文字列も CRLF に合わせる
        if "\r\n" in text:
            old_n, new_n = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        else:
            old_n, new_n = old, new
        count = text.count(old_n)
        if count == 1:
            pending[p] = text.replace(old_n, new_n)
            print(f"  [対象] {label}（{rel}）")
        elif new_n in text:
            print(f"  [済]   {label}（{rel}）は更新済みです")
        else:
            print(f"  [手動確認] {label}（{rel}）: 想定の文字列が {count} 件。内容が変わっている可能性があります")
            errors += 1
    print()

    # --- 書き込み ---
    if not pending:
        print("変更対象はありません。")
    elif not args.apply:
        print(f"変更予定: {len(pending)} ファイル")
        for p in pending:
            print(f"  - {p.relative_to(root)}")
        print("\n問題なければ  python fix_old_url.py --apply  で反映してください。")
    else:
        written = 0
        for p, text in pending.items():
            try:
                write_text(p, text)
                written += 1
                print(f"  [書込] {p.relative_to(root)}")
            except OSError as e:
                print(f"  [書込失敗] {p.relative_to(root)}: {e}")
                errors += 1
        # 再スキャンして、本当に消えたかを確かめる（書けたつもりで終わらせない）
        remaining = 0
        for p in site_files(root):
            try:
                if OLD_URL_RE.search(read_text(p)):
                    remaining += 1
                    print(f"  [残存] {p.relative_to(root)} に旧URLが残っています")
            except (OSError, UnicodeDecodeError):
                remaining += 1
        if remaining:
            errors += remaining
        print(f"\n書き込み {written}/{len(pending)} ファイル、旧URLの残存 {remaining} ファイル")

    if errors:
        print(f"\n※ 要確認が {errors} 件あります。上の [手動確認] / [失敗] を見てください。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
