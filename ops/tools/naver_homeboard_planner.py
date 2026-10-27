#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naver Mobile Homeboard Planner (ops/tools/naver_homeboard_planner.py)
-------------------------------------------------------------------
- 단순 키워드 검색 노출(SEO)을 넘어 네이버 모바일 메인 '홈판(리빙판, 살림판)'
  추천 알고리즘에 선정되는 4단계 바이럴 기획서 자동 생성
- 4대 공략 공식:
  1. 트렌드 벤치마킹 (다이소 실패 정착기, 틈새 수납 극대화 등)
  2. 결핍/손실회피 트리거 (클릭 유발 훅 제목 5종 생성)
  3. 차별화 실증 관점 주입 (22cm 실측 틈새, 6.0kg 하중 처짐 0% 등)
  4. 스마트블록 DIA+ 3단 스토리보드 연동 (Before -> Install -> After)
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

class HomeboardPlanner:
    """네이버 모바일 리빙/살림 홈판 알고리즘 저격 기획기"""

    DEFAULT_HOOK_TEMPLATES = [
        "아직도 다이소 쓰세요? 3번 무너지고 결국 정착한 {product_name} 3주 찐후기",
        "버리기 전에 꼭 보세요! {metric_gap}로 {target_area} 2배 넓히는 살림 10년 차 꿀팁",
        "살림 고수들이 왜 이것만 쓰는지 알겠네요... {product_name} {metric_weight} 실사용 체감",
        "매번 허리 숙여 뒤적거리던 고통 끝! {metric_weight} 올려도 처짐 0% {product_name}",
        "배수관 때문에 포기했던 {target_area}, {metric_gap} 맞춤으로 완벽 살려낸 비포애프터"
    ]

    BENCHMARK_PATTERNS = [
        {
            "pattern_name": "다이소 실패 후 종결템 정착기 (Trial & Error)",
            "psychology": "저가형 바구니/선반의 휘청거림과 파손 경험 공유 -> 비용 낭비 공감 -> 튼튼한 종결템 안착",
            "key_trigger": "5천원짜리 3개 사고 버린 돈이면 진작 이거 살 걸 그랬습니다."
        },
        {
            "pattern_name": "애매한 틈새 극대화 (Dead Space Recovery)",
            "psychology": "집 구조상 버려지는 20~25cm 데드스페이스를 실측 맞춤으로 살려내는 공간 쾌감",
            "key_trigger": "배수관 파이프 때문에 아무것도 못 넣던 공간이 황금 수납존으로 변했습니다."
        },
        {
            "pattern_name": "살림 10년 차 동선 단축 꿀팁 (Workflow Efficiency)",
            "psychology": "요리 중 허리 굽히지 않고 한 손으로 양념통을 1초 만에 꺼내는 피로도 제로 동선",
            "key_trigger": "프라이팬 불 올리고 소스 찾느라 태워먹던 주방 일상이 180도 달라집니다."
        },
        {
            "pattern_name": "극적 비포 & 애프터 시각화 (Dramatic Visual Contrast)",
            "psychology": "혼돈의 하부장 카오스 -> 쇼룸처럼 각 맞춰 정돈된 애프터 시각적 쾌감",
            "key_trigger": "열 때마다 한숨 나오던 싱크대 문, 이제는 손님 오면 열어서 보여주고 싶어요."
        }
    ]

    def __init__(self):
        pass

    def generate_homeboard_plan(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        입력된 상품 정보(상품명, 카테고리, 핵심 스펙, 실측치 등)를 기반으로
        네이버 리빙 홈판 알고리즘 저격 4단계 기획서 생성
        """
        product_name = product_info.get("product_name", "22cm 슬라이딩 하부장 싱크대 선반")
        category = product_info.get("category", "주방/수납/살림")
        target_area = product_info.get("target_area", "싱크대 하부장")
        metric_gap = product_info.get("metric_gap", "22cm 틈새")
        metric_weight = product_info.get("metric_weight", "6.0kg 하중")
        assembly_metric = product_info.get("assembly_metric", "볼트 4개 5분 조립")
        stability_metric = product_info.get("stability_metric", "바닥 흡착판 쏠림 0%")

        # 1. 결핍/손실회피 트리거 제목 5종 생성
        title_hooks = []
        for tmpl in self.DEFAULT_HOOK_TEMPLATES:
            title = tmpl.format(
                product_name=product_name,
                target_area=target_area,
                metric_gap=metric_gap,
                metric_weight=metric_weight
            )
            title_hooks.append(title)

        # 2. 실증 관점 수치 바인딩
        empirical_metrics = [
            {"label": "틈새 맞춤 규격", "value": f"{metric_gap} 슬림 핏 (배수관 간섭 0%)", "proof": "실측 줄자 인증 컷"},
            {"label": "내하중 테스트", "value": f"{metric_weight} 3주 연속 실사용 (처짐 0%)", "proof": "1.8L 대용량 간장 2병 + 식용유 거치 컷"},
            {"label": "조립 난이도", "value": f"{assembly_metric} (공구 불필요, 여성 혼자 완성)", "proof": "볼트 체결 과정 컷"},
            {"label": "안전성 지표", "value": f"{stability_metric} (앞 꼬꾸라짐 방지)", "proof": "서랍 최대 인출 시 흡착판 고정 컷"},
            {"label": "소재/마감", "value": "탄소강 프레임 방수 분체 도장 (물티슈 1초 컷)", "proof": "양념 국물 닦아내는 클로즈업 컷"}
        ]

        # 3. 스마트블록 DIA+ 3단 스토리보드 연동
        storyboard = {
            "step1_before": {
                "step_title": "1단: 현실의 고통 (Before - 어지러운 배수관)",
                "visual_cut": "sample_living_card_hyper_01.png",
                "pain_point": "싱크대 문 열면 저 안쪽에 박혀있는 양념통 꺼내느라 허리 굽히고 뒤적거림",
                "loss_trigger": "배수관 파이프 간섭으로 일반 선반 미진입 + 안쪽 양념통 유통기한 지나 버림",
                "empathy_copy": "다이소에서 5천 원짜리 철제 바구니 사서 넣어봤자, 무거운 기름통 올리면 휘청거리고 결국 대참사 반복..."
            },
            "step2_install": {
                "step_title": "2단: 22cm 틈새 실측 검증 (Install - 간섭 0%)",
                "visual_cut": "sample_living_card_hyper_02.png",
                "empirical_proof": f"가로 {metric_gap}, 세로 40cm 규격으로 배수 호스 옆 애매한 25cm 공간에 쏙 진입",
                "assembly_point": f"{assembly_metric}, 바닥 실리콘 흡착판으로 프레임 단단히 밀착 고정",
                "empathy_copy": "볼트 4개 손으로 조이고 흡착판 꾹 누르면 끝. 똥손인 저도 5분 만에 끝냈어요."
            },
            "step3_after": {
                "step_title": "3단: 6kg 수납 쾌감 (After - 처짐 없는 레일)",
                "visual_cut": "sample_living_card_hyper_03.png",
                "experience_delight": f"{metric_weight} 대용량 양념통 거치 후에도 한 손으로 스르륵 부드러운 슬라이딩",
                "benefit": "요리 동선 1초 단축, 상단 소형 양념통 + 하단 대형 오일병 분리 수납으로 공간 2배 활용",
                "empathy_copy": "1.8L 간장 2통을 올려도 처짐 없이 드르륵 빠져나올 때의 쾌감... 주방 삶의 질이 수직 상승합니다."
            }
        }

        # 4. 홈판 에디터 추천 키워드 및 해시태그
        naver_seo = {
            "main_keyword": f"{target_area} 정리",
            "sub_keywords": ["틈새 슬라이딩 선반", "싱크대 하부장 수납", "주방 정리 꿀팁", "다이소 수납 실패", "살림 꿀템"],
            "target_homeboard": "네이버 모바일 리빙판 / 푸드판 살림 꿀팁 코너",
            "dia_plus_factors": [
                "1인칭 실제 경험 서술 (3주 실사용)",
                "직접 촬영한 3단 시퀀스 카드 (Glassmorphism UI 및 실측 화살표)",
                "수치 기반 실증 데이터 (22cm, 6kg, 5분 조립)",
                "솔직한 단점 명시 (높이 30cm 초과 업소용 간장통 세로 수납 불가 사전 안내)"
            ]
        }

        return {
            "product_name": product_name,
            "category": category,
            "target_area": target_area,
            "title_hooks": title_hooks,
            "benchmark_patterns": self.BENCHMARK_PATTERNS,
            "empirical_metrics": empirical_metrics,
            "storyboard": storyboard,
            "naver_seo": naver_seo
        }

    def format_markdown_report(self, plan_data: Dict[str, Any]) -> str:
        """기획서 딕셔너리를 마크다운 리포트 규격으로 변환"""
        sb = plan_data["storyboard"]
        seo = plan_data["naver_seo"]

        lines = [
            f"# [네이버 모바일 홈판 저격 기획서: {plan_data['product_name']}]",
            f"**타깃 홈판**: {seo['target_homeboard']}  ",
            f"**카테고리**: {plan_data['category']} | **타깃 공간**: {plan_data['target_area']}  ",
            f"**DIA+ 경험치 가산점 공략**: 1인칭 3주 실사용 실측 데이터 기반  ",
            "",
            "---",
            "",
            "## 1. 결핍/손실회피 트리거 제목 5종 (A/B 테스트용)",
            ""
        ]

        for i, hook in enumerate(plan_data["title_hooks"], 1):
            badge = "★ 1순위 추천" if i == 1 else f"대체 {i}안"
            lines.append(f"- **[제{i}안 ({badge})]**: {hook}")

        lines.extend([
            "",
            "---",
            "",
            "## 2. 홈판 알고리즘 벤치마킹 4대 패턴",
            ""
        ])

        for p in plan_data["benchmark_patterns"]:
            lines.append(f"### ▶ {p['pattern_name']}")
            lines.append(f"- **심리 기제**: {p['psychology']}")
            lines.append(f"- **핵심 훅 문장**: *\"{p['key_trigger']}\"*")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 3. 차별화 실증 지표 바인딩 (수치적 팩트 검증)",
            ""
        ])

        for m in plan_data["empirical_metrics"]:
            lines.append(f"- **{m['label']}**: `{m['value']}` (검증 방식: {m['proof']})")

        lines.extend([
            "",
            "---",
            "",
            "## 4. 스마트블록 DIA+ 3단 스토리보드 연동",
            "",
            f"### [1단] {sb['step1_before']['step_title']}",
            f"- **카드 이미지**: `{sb['step1_before']['visual_cut']}`",
            f"- **현실의 고통**: {sb['step1_before']['pain_point']}",
            f"- **손실 트리거**: {sb['step1_before']['loss_trigger']}",
            f"- **공감 스크립트**: *\"{sb['step1_before']['empathy_copy']}\"*",
            "",
            f"### [2단] {sb['step2_install']['step_title']}",
            f"- **카드 이미지**: `{sb['step2_install']['visual_cut']}`",
            f"- **실측 검증**: {sb['step2_install']['empirical_proof']}",
            f"- **조립/고정**: {sb['step2_install']['assembly_point']}",
            f"- **공감 스크립트**: *\"{sb['step2_install']['empathy_copy']}\"*",
            "",
            f"### [3단] {sb['step3_after']['step_title']}",
            f"- **카드 이미지**: `{sb['step3_after']['visual_cut']}`",
            f"- **쾌감 지점**: {sb['step3_after']['experience_delight']}",
            f"- **체감 효용**: {sb['step3_after']['benefit']}",
            f"- **공감 스크립트**: *\"{sb['step3_after']['empathy_copy']}\"*",
            "",
            "---",
            "",
            "## 5. 네이버 스마트블록 검색 및 DIA+ 최적화 키워드",
            f"- **메인 키워드**: `{seo['main_keyword']}`",
            f"- **서브 키워드**: {', '.join([f'`{k}`' for k in seo['sub_keywords']])}",
            "- **알고리즘 가산점 체크리스트**:"
        ])

        for f in seo["dia_plus_factors"]:
            lines.append(f"  - [x] {f}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Naver Mobile Homeboard Planner CLI")
    parser.add_argument("--product", type=str, default="22cm 슬라이딩 하부장 싱크대 선반", help="상품명")
    parser.add_argument("--category", type=str, default="주방/수납/살림", help="카테고리")
    parser.add_argument("--out", type=str, default="", help="출력 마크다운 파일 경로")
    args = parser.parse_args()

    planner = HomeboardPlanner()
    product_info = {
        "product_name": args.product,
        "category": args.category,
        "target_area": "싱크대 하부장",
        "metric_gap": "22cm 틈새",
        "metric_weight": "6.0kg 하중",
        "assembly_metric": "볼트 4개 5분 조립",
        "stability_metric": "바닥 흡착판 쏠림 0%"
    }

    plan_data = planner.generate_homeboard_plan(product_info)
    md_content = planner.format_markdown_report(plan_data)

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[HomeboardPlanner] Saved plan to: {args.out}")
    else:
        print(md_content)

if __name__ == "__main__":
    main()
