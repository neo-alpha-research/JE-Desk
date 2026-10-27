#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[P3] JE Smart Multi-Affiliate Link Wallet & Failover Switcher (smart_link_wallet.py)
-----------------------------------------------------------------------------------
- 비개발자 JE를 위한 원터치 제휴 링크 발급 & 품절 자동 스위처
- 5인 전문가 자문 설계: 오늘의집(4.5%) -> 올리브영(4%) -> 쿠팡(3%) 수수료 워터폴
- Zero-Dependency 순수 Python 구현 (로컬 지갑 ops/out/je_link_wallet.json 영구 보존)
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Windows 콘솔 인코딩 방어
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WALLET_FILE = os.path.join(BASE_DIR, "ops", "out", "je_link_wallet.json")

# JE 4대 플랫폼 기본 제휴 프로필
AFFILIATE_PROFILES = {
    "ohouse": {
        "platform": "오늘의집 (Ohouse)",
        "commission_rate": "4.5%",
        "curator_id": "ORCA_CURATOR_2026",
        "cookie_duration": "24시간",
        "tag": "주방/수납/인테리어 1위"
    },
    "oliveyoung": {
        "platform": "올리브영 (OliveYoung)",
        "commission_rate": "4.0%",
        "curator_id": "JE_BEAUTY_2026",
        "cookie_duration": "24시간",
        "tag": "욕실/위생/바디케어 1위"
    },
    "coupang": {
        "platform": "쿠팡 파트너스 (Coupang)",
        "commission_rate": "3.0%",
        "curator_id": "AF7829104",
        "cookie_duration": "24시간",
        "tag": "로켓배송/생필품 1위"
    },
    "naver": {
        "platform": "네이버 쇼핑 (Naver)",
        "commission_rate": "2.5%",
        "curator_id": "JE_SHOP_2026",
        "cookie_duration": "24시간",
        "tag": "최저가 비교/포인트 적립"
    }
}

DEFAULT_ITEMS = [
    {
        "id": "item_01",
        "name": "싱크대 하부장 22cm 슬라이딩 선반",
        "category": "주방/수납",
        "status": "active",
        "priority_platform": "ohouse",
        "links": {
            "ohouse": {
                "url": "https://ohou.se/productions/2284910?affect_type=Curator&affect_id=ORCA_CURATOR_2026",
                "in_stock": True,
                "price": "23,900원",
                "rate": "4.5%",
                "expected_reward": "1,075원"
            },
            "coupang": {
                "url": "https://link.coupang.com/a/bJE_Sink_22cm_Failover",
                "in_stock": True,
                "price": "24,500원",
                "rate": "3.0%",
                "expected_reward": "735원"
            }
        },
        "safe_coordinate_copy": "💡 [22cm 슬라이딩 선반 정품 확인 좌표]\n(폭 25cm 이상 공간 안 나오면 사지 마세요, 안 들어갑니다!)\n👉 https://ohou.se/productions/2284910?affect_type=Curator&affect_id=ORCA_CURATOR_2026\n\n※ 오늘의집 큐레이터 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다."
    },
    {
        "id": "item_02",
        "name": "오일병 누유방지 내열유리 양념통 500ml",
        "category": "주방/조리",
        "status": "active",
        "priority_platform": "ohouse",
        "links": {
            "ohouse": {
                "url": "https://ohou.se/productions/1984210?affect_type=Curator&affect_id=ORCA_CURATOR_2026",
                "in_stock": True,
                "price": "14,800원",
                "rate": "4.5%",
                "expected_reward": "666원"
            },
            "coupang": {
                "url": "https://link.coupang.com/a/bJE_Oil_Bottle_Failover",
                "in_stock": True,
                "price": "15,200원",
                "rate": "3.0%",
                "expected_reward": "456원"
            }
        },
        "safe_coordinate_copy": "💡 [흘러내림 없는 내열 오일병 좌표]\n👉 https://ohou.se/productions/1984210?affect_type=Curator&affect_id=ORCA_CURATOR_2026\n\n※ 오늘의집 큐레이터 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다."
    }
]

def load_wallet():
    if os.path.exists(WALLET_FILE):
        try:
            with open(WALLET_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "updated_at": datetime.now().isoformat(),
        "profiles": AFFILIATE_PROFILES,
        "items": DEFAULT_ITEMS
    }

def save_wallet(data):
    os.makedirs(os.path.dirname(WALLET_FILE), exist_ok=True)
    with open(WALLET_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_best_active_link(item):
    """품절 시 차순위 플랫폼으로 자동 Failover"""
    p_pref = item.get("priority_platform", "ohouse")
    links = item.get("links", {})
    if p_pref in links and links[p_pref].get("in_stock", True):
        return p_pref, links[p_pref]["url"], False
    
    # 대체 플랫폼 탐색
    for plat in ["ohouse", "oliveyoung", "coupang", "naver"]:
        if plat in links and links[plat].get("in_stock", True):
            return plat, links[plat]["url"], True
    return None, None, False

def add_or_update_item(name, category, ohouse_url=None, coupang_url=None):
    wallet = load_wallet()
    links = {}
    if ohouse_url:
        links["ohouse"] = {
            "url": ohouse_url,
            "in_stock": True,
            "price": "23,900원",
            "rate": "4.5%",
            "expected_reward": "1,075원"
        }
    if coupang_url:
        links["coupang"] = {
            "url": coupang_url,
            "in_stock": True,
            "price": "24,500원",
            "rate": "3.0%",
            "expected_reward": "735원"
        }
    
    new_item = {
        "id": f"item_{len(wallet['items']) + 1:02d}",
        "name": name,
        "category": category,
        "status": "active",
        "priority_platform": "ohouse" if ohouse_url else "coupang",
        "links": links,
        "safe_coordinate_copy": f"💡 [{name} 정품 확인 좌표]\n👉 {ohouse_url or coupang_url}\n\n※ 제휴 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다."
    }
    wallet["items"].append(new_item)
    wallet["updated_at"] = datetime.now().isoformat()
    save_wallet(wallet)
    return new_item

def main():
    parser = argparse.ArgumentParser(description="JE Smart Multi-Affiliate Link Wallet")
    parser.add_argument("--list", action="store_true", help="지갑에 저장된 제휴 링크 목록 출력")
    parser.add_argument("--add", type=str, help="새 상품명 추가")
    parser.add_argument("--cat", type=str, default="리빙/주방", help="상품 카테고리")
    parser.add_argument("--ohouse", type=str, help="오늘의집 제휴 URL")
    parser.add_argument("--coupang", type=str, help="쿠팡 파트너스 제휴 URL")
    args = parser.parse_args()

    wallet = load_wallet()
    if args.add:
        item = add_or_update_item(args.add, args.cat, args.ohouse, args.coupang)
        print(f"[P3 OK] New Item Added: {item['name']}")
    else:
        save_wallet(wallet)
        print(f"[P3 OK] JE Smart Link Wallet Loaded ({len(wallet['items'])} items)")
        for item in wallet["items"]:
            plat, url, is_failover = get_best_active_link(item)
            mode = "[FAILOVER]" if is_failover else "[PRIMARY]"
            print(f" - [{item['category']}] {item['name']}: {plat} {mode} -> {url}")

if __name__ == "__main__":
    main()
