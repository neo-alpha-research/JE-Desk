#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Academic Paper Search & Vault Ingestion CLI
------------------------------------------------------
Supports natural Korean or English queries:
1. Translates Korean query into optimal academic English keywords.
2. Searches Google Scholar / arXiv via Aside Chromium.
3. Displays TOP 3 candidate papers with title, authors, year, and venue.
4. User selects choice (1, 2, 3), and engine automatically downloads PDF,
   converts to structured Markdown, and ingests into Obsidian Vault!
"""

import os
import sys
import json
import re
import subprocess
import urllib.parse
from pathlib import Path

# Force Windows stdout/stderr to UTF-8
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure paths
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from aside_paper_agent import search_google_scholar_via_aside

SKILL_SCRIPT = SCRIPT_DIR.parent.parent / ".agents" / "skills" / "academic-paper-deconstructor" / "scripts" / "paper_deconstructor.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))
from paper_deconstructor import ingest_paper_to_vaults

AGY_BIN = r"C:\Users\kibae\AppData\Local\agy\bin\agy.EXE"


def translate_to_academic_keywords(query: str) -> str:
    """Translates Korean query to high-density English academic keywords."""
    # Check if query contains Korean
    has_korean = bool(re.search(r'[가-힣]', query))
    if not has_korean:
        return query

    if os.path.exists(AGY_BIN):
        prompt = (
            f"학술 논문 검색을 위해 다음 한글 연구 주제를 가장 정확한 영문 학술 검색 키워드(3~5단어)로만 번역해줘.\n"
            f"사족 없이 영문 키워드만 한 줄로 출력할 것.\n\n[주제]: {query}"
        )
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            res = subprocess.run(
                [AGY_BIN, "-p", prompt, "--model", "gemini-3.8-flash-low"],
                capture_output=True,
                timeout=10,
                env=env
            )
            if res.returncode == 0:
                out = res.stdout.decode("utf-8", errors="replace").strip()
                clean = out.splitlines()[-1].strip().strip('"').strip("'")
                if len(clean) > 3:
                    return clean
        except Exception:
            pass

    return query


def main():
    if len(sys.argv) > 1:
        raw_query = " ".join(sys.argv[1:])
    else:
        print("=" * 65)
        print("📚 [Solo AX] 글로벌 학술 논문 자율 검색 & 옵시디언 적재기")
        print("=" * 65)
        raw_query = input("🔍 찾고 싶은 논문 주제를 한글 또는 영어로 입력하세요: ").strip()

    if not raw_query:
        print("[!] 검색어가 입력되지 않았습니다.")
        return 1

    academic_keywords = translate_to_academic_keywords(raw_query)
    print(f"\n[*] 연구 키워드 변환: '{raw_query}' ➔ '{academic_keywords}'")
    print("[*] Google Scholar 전수 자율 탐색 중 (Aside Browser)...")

    results = search_google_scholar_via_aside(academic_keywords, max_results=3)

    if not results:
        print(f"[!] '{academic_keywords}'에 대한 검색 결과를 찾지 못했습니다.")
        return 1

    print("\n" + "=" * 65)
    print(f"📑 검색된 글로벌 학술 논문 TOP {len(results)}")
    print("=" * 65)

    for idx, r in enumerate(results, start=1):
        print(f"[{idx}] {r['title']}")
        print(f"    - 정보: {r['meta']}")
        print(f"    - 요약: {r['snippet'][:100]}...")
        print(f"    - URL: {r['url']}")
        print("-" * 65)

    choice_str = input(f"\n적재할 논문 번호를 선택하세요 (1~{len(results)}, 기본 1): ").strip()
    try:
        choice = int(choice_str) if choice_str else 1
        if not (1 <= choice <= len(results)):
            choice = 1
    except ValueError:
        choice = 1

    selected = results[choice - 1]
    print(f"\n🚀 [{choice}번 선택] '{selected['title']}' 전문 마크다운 변환 및 볼트 적재 시작...")

    res = ingest_paper_to_vaults(selected['url'])
    print("\n" + "=" * 65)
    print("🎉 [적재 완료] 옵시디언 볼트에 성공적으로 적재되었습니다!")
    print(f"   - 논문 제목: {res['title']}")
    print(f"   - 전문 마크다운: {res['fulltext_file']}")
    print(f"   - 요약 도시에: {res['dossier_file']}")
    print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(main())
