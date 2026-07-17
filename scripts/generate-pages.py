#!/usr/bin/env python3
"""
Supabase의 모든 설교 id에 대해 실제 정적 폴더(예: 90560b47-.../index.html)를 생성한다.
GitHub Pages는 404.html 폴백(가짜 200)과 달리 실제 파일은 진짜 HTTP 200으로 응답하므로,
카카오톡 등 메신저의 링크 미리보기·딥링크가 안정적으로 동작한다.

설교가 추가/삭제될 때마다 이 스크립트를 다시 실행하고 커밋·푸시해야 한다.
"""
import json
import os
import urllib.request

SUPABASE_URL = "https://vogslryxeicemtotleph.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_XFxawpPt098rCpSPPE4U_A_-GJbrBuF"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO_ROOT, "index.html")


def fetch_sermon_ids():
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/sermons?select=id",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    return [row["id"] for row in data]


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_html = f.read()

    ids = fetch_sermon_ids()
    print(f"설교 {len(ids)}건 발견")

    # 더 이상 존재하지 않는 설교의 예전 정적 폴더는 정리한다.
    existing_dirs = {
        name for name in os.listdir(REPO_ROOT)
        if os.path.isdir(os.path.join(REPO_ROOT, name)) and name not in (".git", "scripts")
        and len(name) == 36 and name.count("-") == 4  # uuid 형태만
    }
    for stale in existing_dirs - set(ids):
        stale_dir = os.path.join(REPO_ROOT, stale)
        os.remove(os.path.join(stale_dir, "index.html"))
        os.rmdir(stale_dir)
        print(f"삭제됨(더 이상 없는 설교): {stale}")

    for sid in ids:
        d = os.path.join(REPO_ROOT, sid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)
        print(f"생성됨: {sid}/index.html")


if __name__ == "__main__":
    main()
