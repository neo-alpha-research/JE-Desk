---
name: lifestyle-viral-factory
description: 주방·살림·리빙 N잡 및 제휴마케팅 팩토리 자동화 스킬. 상품명 하나로 ① 5대 제휴 링크 매핑 및 품절 방어, ② 네이버 모바일 홈판 DIA+ 기획, ③ 1080x1080 정방형 3단 카드뉴스, ④ 6단계 인간미 자가퇴고(95점 컷오프), ⑤ 네이버 스마트에디터 ONE 리치 HTML, ⑥ 스레드 4-Beat 바이럴 카루셀 배포본을 0.8초 만에 원스톱으로 생성한다. "살림 글 써줘", "블로그 포스팅 생성", "스레드 카루셀 만들어줘", "제휴 링크 만들어줘" 요청 시 즉각 가동한다.
---

# Lifestyle Viral Factory (살림/리빙 고전환 자동화 스킬)

1인 사업자 및 아내(JE)를 위한 초경량 고전환 팩토리 파이프라인.

## 실행 도구
- **통합 파이프라인**: `ops/tools/run_lifestyle_viral_pipeline.py`
- **웹 스튜디오**: `ops/tools/je_desk_web_studio.py` (포트 8900 로컬 웹 UI)
- **스레드 배포기**: `ops/tools/threads_carousel_publisher.py`
- **카드뉴스 생성기**: `ops/tools/generate_hyperrealistic_cards.py`

## CLI 사용법
```bash
python ops/tools/run_lifestyle_viral_pipeline.py --product "상품명" --category "카테고리" --specs "핵심 스펙 및 실사용 메모"
```

## 핵심 산출물
1. `ops/out/threads_carousel_post.md` (스레드 4-Beat 및 첫 댓글 브릿지)
2. `ops/out/final_viral_post.md` (6단계 자가퇴고 통과 블로그 본문)
3. `ops/out/naver_smarteditor_preview.html` (스마트에디터 ONE 서식)
4. `ops/out/sample_living_card_hyper_01~03.png` (3단 시퀀스 카드뉴스)
5. `ops/out/safe_link_status.json` (실시간 활성 제휴처 상태)
