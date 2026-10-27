#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Omni Vertical Affiliate Link Hub (ops/tools/multi_affiliate_hub.py)
------------------------------------------------------------------
- Coupang 3% 한계를 넘어 고단가·고전환 11대 버티컬 제휴 플랫폼을 통합 관리
- 지원 플랫폼: Coupang, Ohouse(오늘의집), OliveYoung(올리브영), KakaoGift(카카오 선물하기), NaverConnect(네이버 쇼핑 커넥트) 등
- 카테고리/키워드 기반 최우선 플랫폼 자동 추천 및 트래킹 파라미터 결합 링크 생성 엔진
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

class AffiliateHub:
    """통합 제휴 플랫폼 메타데이터 및 트래킹 링크 생성·추천 허브"""

    DEFAULT_PLATFORMS = {
        "Ohouse": {
            "name": "오늘의집 큐레이터 (Ohouse Curator)",
            "alias": ["오늘의집", "ohouse", "오하우스"],
            "base_commission": 0.06,  # 6.0% (5~8%)
            "commission_label": "5.0% ~ 8.0% (기본 6.0%)",
            "primary_categories": ["인테리어", "수납", "정리", "가구", "주방", "식기", "홈스타일링", "선반", "하부장"],
            "target_keywords": [
                "하부장", "선반", "수납", "정리", "싱크대", "서랍", "틈새", "인테리어",
                "주방", "식기건조대", "양념통", "욕실수납", "행거", "러그", "커튼", "조명"
            ],
            "url_template": "https://ohou.se/productions/{product_id}?affect_type=Curator&affect_id={tracking_id}",
            "default_tracking_id": "ORCA_CURATOR_2026",
            "strengths": "2040 여성·주부 인테리어 감성 신뢰도 1위, 고단가 수납/가구군 5~8% 고수수료"
        },
        "OliveYoung": {
            "name": "올리브영 셔터/제휴 (OliveYoung Affiliate)",
            "alias": ["올리브영", "oliveyoung", "올영"],
            "base_commission": 0.05,  # 5.0% (4~7%)
            "commission_label": "4.0% ~ 7.0% (기본 5.0%)",
            "primary_categories": ["뷰티", "스킨케어", "바디", "헤어", "위생", "핸드크림", "청결", "이너뷰티"],
            "target_keywords": [
                "핸드크림", "바디로션", "선크림", "샴푸", "클렌징", "세럼", "앰플", "립밤",
                "향수", "마스크팩", "핸드워시", "치약", "비타민", "다이어트", "화장솜"
            ],
            "url_template": "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.oy?goodsNo={product_id}&trackingCd={tracking_id}",
            "default_tracking_id": "ORCA_OY_PARTNER",
            "strengths": "올영세일 기간 폭발적 트래픽, 2030 여성 구매 전환율 1위, 오프라인 매장 인지도 결합"
        },
        "KakaoGift": {
            "name": "카카오 선물하기 크리에이터 (Kakao Gift Creator)",
            "alias": ["카카오선물하기", "kakaogift", "선물하기"],
            "base_commission": 0.045,  # 4.5% (4~6%)
            "commission_label": "4.0% ~ 6.0% (기본 4.5%)",
            "primary_categories": ["선물", "프리미엄 리빙", "스몰럭셔리", "디저트", "생일", "답례품"],
            "target_keywords": [
                "선물", "생일", "답례품", "디퓨저", "티세트", "고급", "패키지", "기프트",
                "케이크", "스몰럭셔리", "각인", "핸드워시세트", "수건세트", "찻잔"
            ],
            "url_template": "https://gift.kakao.com/product/{product_id}?ref={tracking_id}",
            "default_tracking_id": "ORCA_KAKAO_CREATOR",
            "strengths": "지인 선물·생일 1초 간편 결제, 높은 객단가 및 반품률 0%에 수렴하는 전환 구조"
        },
        "NaverConnect": {
            "name": "네이버 쇼핑 커넥트 (Naver Shopping Connect)",
            "alias": ["네이버쇼핑", "naverconnect", "스마트스토어"],
            "base_commission": 0.05,  # 5.0% (4~8%)
            "commission_label": "4.0% ~ 8.0% (기본 5.0%)",
            "primary_categories": ["스마트스토어", "네이버페이", "산지직송", "쇼핑라이브", "브랜드스토어"],
            "target_keywords": [
                "스마트스토어", "네이버페이", "산지직송", "단독특가", "농축수산", "핸드메이드",
                "주방소품", "맞춤제작", "특가공구", "블로그마켓"
            ],
            "url_template": "https://cr.shopping.naver.com/adcr.nhn?x={tracking_id}&nvMid={product_id}",
            "default_tracking_id": "ORCA_NAVER_CONNECT_2026",
            "strengths": "네이버 블로그/모바일 홈판 인앱 원클릭 N페이 결제, 네이버 알고리즘 가산점 연계"
        },
        "Coupang": {
            "name": "쿠팡 파트너스 (Coupang Partners)",
            "alias": ["쿠팡", "coupang", "쿠파스"],
            "base_commission": 0.03,  # 3.0%
            "commission_label": "3.0% (고정)",
            "primary_categories": ["생활용품", "주방소모품", "식품", "가전", "로켓배송", "생필품", "주방/수납", "리빙"],
            "target_keywords": [
                "로켓배송", "생필품", "주방세제", "물티슈", "키친타올", "간장", "식용유",
                "고무장갑", "종이컵", "비닐봉투", "건전지", "세탁세제", "탈취제",
                "하부장", "선반", "수납", "정리", "주방", "싱크대", "서랍"
            ],
            "url_template": "https://link.coupang.com/a/{tracking_id}",
            "default_tracking_id": "ORCA_COUPANG_PROMO",
            "strengths": "익일 새벽 로켓배송 보장, 최다 SKU, 구매 허들이 가장 낮은 전 국민 결제 인프라"
        }
    }

    def __init__(self, custom_platforms: Optional[Dict[str, Any]] = None):
        self.platforms = dict(self.DEFAULT_PLATFORMS)
        if custom_platforms:
            self.platforms.update(custom_platforms)

    def register_platform(self, key: str, metadata: Dict[str, Any]) -> None:
        """신규 제휴 플랫폼 동적 등록"""
        self.platforms[key] = metadata

    def get_platform(self, key: str) -> Optional[Dict[str, Any]]:
        return self.platforms.get(key)

    def recommend_best_platform(self, product_name: str, category: str = "") -> Dict[str, Any]:
        """
        상품명과 카테고리를 분석하여 최우선(1순위) 및 차선(2순위) 제휴 플랫폼을 자동 추천.
        - 키워드 매칭 점수 + 카테고리 연관도 + 기본 수수료율 가중치 결합
        """
        combined_text = f"{product_name} {category}".lower()
        scored_platforms = []

        for p_key, meta in self.platforms.items():
            keyword_score = 0.0

            # 1. 키워드 매칭 (개당 15점)
            for kw in meta["target_keywords"]:
                if kw.lower() in combined_text:
                    keyword_score += 15.0

            # 2. 카테고리 매칭 (개당 20점)
            for cat in meta["primary_categories"]:
                if cat.lower() in combined_text:
                    keyword_score += 20.0

            # 키워드/카테고리 매칭이 전혀 없는 경우 기본 점수 0
            if keyword_score == 0:
                total_score = 0.0
            else:
                # 3. 수수료율 가중치 (수수료 1%당 5점 가산 -> 동점 또는 유사 점수 시 고수수료 우대)
                fee_bonus = meta["base_commission"] * 500.0
                total_score = keyword_score + fee_bonus

            scored_platforms.append({
                "platform_key": p_key,
                "name": meta["name"],
                "score": total_score,
                "base_commission": meta["base_commission"],
                "commission_label": meta["commission_label"],
                "strengths": meta["strengths"]
            })

        # 점수 내림차순 정렬
        scored_platforms.sort(key=lambda x: x["score"], reverse=True)

        rank_1 = scored_platforms[0]
        rank_2 = scored_platforms[1]

        reason = (
            f"'{product_name}' 상품은 '{rank_1['name']}'의 주력 타깃 카테고리와 "
            f"일치하며, {rank_1['commission_label']}의 고수수료 혜택이 제공됩니다. "
            f"차선책(대체 옵션)으로는 로켓배송 전환율을 보장하는 '{rank_2['name']}'을 복합 추천합니다."
        )

        return {
            "product_name": product_name,
            "category": category,
            "primary": rank_1,
            "secondary": rank_2,
            "all_ranked": scored_platforms,
            "recommendation_reason": reason
        }

    def resolve_affiliate_links(
        self,
        product_name: str,
        category: str = "",
        base_urls: Optional[Dict[str, str]] = None,
        custom_tracking_ids: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        입력된 상품 정보에 대해 등록된 각 제휴처별 트래킹 파라미터가 포함된
        최종 제휴 링크 딕셔너리 생성
        """
        custom_tracking_ids = custom_tracking_ids or {}
        base_urls = base_urls or {}
        recommendation = self.recommend_best_platform(product_name, category)

        resolved_links = {}
        for p_key, meta in self.platforms.items():
            track_id = custom_tracking_ids.get(p_key, meta["default_tracking_id"])
            
            # 사용자 지정 base_url이 있으면 우선 사용
            if p_key in base_urls:
                raw_url = base_urls[p_key]
                if "?" in raw_url:
                    final_url = f"{raw_url}&ref_orca={track_id}"
                else:
                    final_url = f"{raw_url}?ref_orca={track_id}"
            else:
                # 템플릿 기반 샘플 프로덕션 ID 할당
                sample_prod_id = "sample_item_22cm_shelf"
                if p_key == "Ohouse":
                    sample_prod_id = "2284910"
                elif p_key == "OliveYoung":
                    sample_prod_id = "A00000019284"
                elif p_key == "KakaoGift":
                    sample_prod_id = "849201"
                elif p_key == "NaverConnect":
                    sample_prod_id = "98234190"
                elif p_key == "Coupang":
                    sample_prod_id = "8491039841"

                final_url = meta["url_template"].format(
                    product_id=sample_prod_id,
                    tracking_id=track_id
                )

            is_primary = (p_key == recommendation["primary"]["platform_key"])
            is_secondary = (p_key == recommendation["secondary"]["platform_key"])

            resolved_links[p_key] = {
                "platform_name": meta["name"],
                "commission_rate": meta["commission_label"],
                "affiliate_url": final_url,
                "priority_badge": "1순위 (추천)" if is_primary else ("2순위 (대체)" if is_secondary else "일반"),
                "is_primary": is_primary,
                "is_secondary": is_secondary,
                "strengths": meta["strengths"]
            }

        return {
            "product_name": product_name,
            "category": category,
            "best_platform": recommendation["primary"]["name"],
            "secondary_platform": recommendation["secondary"]["name"],
            "recommendation_summary": recommendation["recommendation_reason"],
            "links": resolved_links
        }


def main():
    parser = argparse.ArgumentParser(description="Omni Vertical Affiliate Hub CLI")
    parser.add_argument("--product", type=str, default="22cm 슬라이딩 하부장 싱크대 선반", help="상품명")
    parser.add_argument("--category", type=str, default="주방/수납/살림", help="카테고리")
    parser.add_argument("--out", type=str, default="", help="출력 JSON 파일 경로")
    args = parser.parse_args()

    hub = AffiliateHub()
    result = hub.resolve_affiliate_links(args.product, args.category)

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[AffiliateHub] Saved affiliate links mapping to: {args.out}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
