# AGENTS.md — AX_Desk_Lab (1인 AX 데스크 솔루션 연구소) 마스터 지침 (Claude · Antigravity · ORCA 단일 정본)

최종 갱신: 2026-10-26 | 단일 정본(Single SSOT): `AGENTS.md`
담당 워크스페이스: `D:/AX_Desk_Lab`
상위 헌법: `D:/Brand_Command/00_Admin/EVS_BRAND_CONSTITUTION.md` · `D:/Obsidian/내 회사 허브/00_회사/SOP_v1.md` · `D:/Obsidian/내 회사 허브/00_회사/지침.md`
전사 라우팅 맵: `D:/Brand_Command/04_Business_OS/NEO_SYSTEM_ROUTING_MAP.md`
전사 모델 원장: `D:/Brand_Command/04_Business_OS/model_ledger/MODEL_LEDGER.json`

---

> [EXECUTION_MODE: ZERO-QUESTION AUTONOMOUS]
> 1. 작업 도중 사소한 선택지 질문(ask_question)을 엄격히 금지하며, 최우선 권장안(Recommended Option)을 즉각 채택하여 무인 완주한다.
> 2. 오직 3대 절대 경계(비가역적 영구 파괴, 유료 결제/대외 발행, 헌법 충돌)에서만 질문을 허용한다.
> 3. 완료 후 [수행 결과] + [자동 채택 근거] + [롤백 방법] 3대 블록으로 사후 보고한다.
> 4. [전사 모델 원장 강제] 모든 스킬·작업의 모델 워터폴은 D:/Brand_Command/04_Business_OS/model_ledger/MODEL_LEDGER.json의 skill_matrix를 단일 정본으로 따르며, 임의 모델 강등을 엄격히 금지한다.
> 5. [프론트라인 역할 한계] 상주 Flash 모델은 기획서·질문지·설계서 본문을 직접 작성할 권한이 없으며, 오직 워터폴 오케스트레이터 실행 및 모니터링만 수행한다.

---

## 0. 프로젝트 목적 및 핵심 거버넌스

- **소유자/총괄**: 대표 Neo
- **프로젝트 목적**: 1~2인 사업자 및 개인을 위한 초경량 고품질 PC AX(AI Transformation) 전환 패키지 연구, 개발, 골든마스터 패키징 및 원클릭 배포
- **핵심 4대 원칙**:
  1. **골든 마스터 분리**: `01_Golden_Master/`는 고객 납품용 순수 볼트이므로 개인 메모나 기밀 절대 유입 금지.
  2. **범용 엔진 유지**: 모든 스킬과 도구는 특정 드라이브나 경로 하드코딩 없는 Zero-Dependency 유지 (순수 파이썬 + 포터블 AHK).
  3. **3분 온보딩**: 고객 PC에서는 3가지 질문(`00_내_맞춤설정.md`)으로 즉석 맞춤 컴파일.
  4. **무인 롤아웃**: 기존 고객 데이터 훼손 없이 엔진만 원클릭 최신화(`update_ax.bat`).

---

## 1. 전사 범용 스킬 4대 번들 (`.agents/skills/`)

본 연구소 및 골든 마스터에 탑재되는 4대 표준 범용 스킬은 다음과 같습니다:
1. `universal-backup-maintenance`: 임의의 폴더 지정 백업, 중복 백업 원천 차단, SQLite 핫 스냅샷, 복원 무결성 사전 검증, 7일 임시파일 안심 정리.
2. `omni-intelligence-pipeline`: 유튜브, 블로그, 리포트, 뉴스 기사 URL ➔ 0-토큰 추출 ➔ 린터 ➔ Toss 모바일 반응형 HTML 및 옵시디언 품의서 생성.
3. `notebooklm-run`: 7개 Google Pro 계정 풀 기반 Direct CLI 무손실 정보 추출 러너.
4. `notebooklm-deep-research`: 도메인별 딥리서치 자동화 및 지식 구조화 파이프라인.
