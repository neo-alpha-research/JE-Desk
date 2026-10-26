---
name: notebooklm-run
description: 중요 단계(기획 착수·법령/고증 보강·아크/카테고리 확장·감리)에서 NotebookLM 3단 도메인 확충 파이프라인(① 질문 설계 -> ② Direct CLI 7계정 풀 무손실 수집 -> ③ Argon/Sonnet 팩트 압축 및 Opus 마스터 청사진 확정 -> ④ Hermes/GBrain 적재)을 실행한다. "NotebookLM 돌려", "딥리서치 맡겨", "도메인 확충 리서치" 요청에 사용.
---

# NotebookLM 3단 도메인 확충 파이프라인 (전사 표준 단일 정본 v2.3 — Direct CLI & 7계정 자동 풀)

> ※ **전사 모델 원장 강제 준용**: 본 스킬의 모든 단계별 실행 모델 및 워터폴 순위는 최상위 원장([D:/Brand_Command/04_Business_OS/model_ledger/MODEL_LEDGER.json](file:///D:/Brand_Command/04_Business_OS/model_ledger/MODEL_LEDGER.json))의 `skill_matrix['notebooklm-run']`을 엄격히 강제 준용합니다.

Claude(Opus/Sonnet) 및 워커 토큰을 극한으로 절약하고 도메인 깊이를 극대화하기 위해 **질문 설계(헤드) ➔ Direct CLI 7계정 풀 무손실 수집(`nlm_direct_runner.py`, 에이전트 수집 토큰 0) ➔ 팩트 압축(`argon` / `sonnet`) ➔ 마스터 청사진 확정(`opus` 헤드) ➔ 정본·GBrain 반영**의 루프로 실행한다.

---

## 1단계: 빈칸 진단 및 질문 설계 (Phase A — 헤드 워터폴)

1. **Phase A 전담 모델 4단계 워터폴 (MODEL_LEDGER.json 강제)**:
   - **1순위 (최우선)**: `claude-opus-5-5` (Effort: High) — Anthropic Pro 쿼터 가용 시 1순위 전담 설계
   - **2순위 (폴백 1)**: `gemini-4-argon-high` (Effort: High) — Opus 한도 소진 시 주간 Argon 잔여 쿼터 확인 후 호출
   - **3순위 (폴백 2)**: `claude-sonnet-5-5` (Effort: High) — Argon 소진 시 내부/외부 Sonnet 5.5 고추론 호출
   - **4순위 (폴백 3)**: `gemini-3.8-flash-high` (Effort: High) — Sonnet 한도 소진 시 Flash High 최대 노력도로 방어 설계
   - *실행 수칙*: 1순위부터 시도하며, 쿼터 에러(Rate limit) 발생 시 차순위 모델로 순차 페일오버한다. 하위 모델의 임의 자의적 선점 집행은 엄격히 금지된다.
2. 작업 착수 전 `python D:/Brand_Command/04_Business_OS/knowledge_retrieval/query.py search "<주제>" --json`으로 현재 원장의 빈칸(미확인 법령·수치·연대기·벤치마크 부족분)을 먼저 파악한다.
3. 현재 워크스페이스 안의 `ops/research/NotebookLM_<주제>_<YYYYMMDD>.md`에 프롬프트 파일을 작성한다:
   - `## SR-1 ~ SR-3`: 딥리서치(Deep Research)용 구조화 프롬프트 (표 형식·기간·필수 포함 항목·출처 명시 요구)
   - `## 후속 질문`: 딥리서치 완료 후 순서대로 던질 심층 꼬리질문 (`Q1` ~ `Q6`)
   - **보안 절대 원칙**: 미공개 웹소설 원고(`*/manuscripts/*`), 미출간 전자책 본문, `.env`·비밀키·개인정보는 절대 프롬프트에 넣거나 업로드하지 않는다.

---

## 2단계: Direct CLI 7계정 자동 풀 무손실 수집 (Phase B — 토큰 0)

기존 브라우저 UI 조작 방식을 폐기하고, **`notebooklm-py` 백엔드 직결 실행기(`D:/Brand_Command/04_Business_OS/ops/tools/nlm_direct_runner.py`)**를 트리거하여 에이전트 수집 토큰 소모를 0으로 만든다. 7개 인증 프로필(`default`, `acct2` ~ `acct7`)이 자동으로 활용된다.

1. **단일 리서치 실행 (`--profile auto` 기본 작동 — 한도 시 자동 계정 스위칭)**:
   ```powershell
   python D:/Brand_Command/04_Business_OS/ops/tools/nlm_direct_runner.py -i ops/research/NotebookLM_<주제>_<YYYYMMDD>.md -o ops/research/notebooklm/<주제>_<YYYYMMDD>.md -t "<노트북_제목>"
   ```
2. **복수 리서치 동시 실행 (`--batch` — 7개 계정 풀 1:1 라운드로빈 자동 병렬 분산)**:
   ```powershell
   python D:/Brand_Command/04_Business_OS/ops/tools/nlm_direct_runner.py --batch "ops/research/A.md|ops/research/notebooklm/A_out.md|노트북A" "ops/research/B.md|ops/research/notebooklm/B_out.md|노트북B"
   ```

---

## 3단계: 팩트 시트 사전 압축 및 마스터 청사진 확정 (Phase C — 워커 ➔ 헤드)

1. **Phase C-Pre (고농축 팩트 패킷 압축 — 토큰 70% 절감 프로토콜)**:
   - 8만~15만 자의 원천 딥리서치 코퍼스를 Opus에 직접 넣지 않고, **`gemini-4-argon-high`** (Argon 한도 소진 시 **`claude-sonnet-5-5`**)를 호출하여 `PACKET_OPUS_READY.md`로 사전 정제한다.
   - *절대 원칙*: Flash 강등 금지. 수치·가격·출처는 `STRICT_FACT`로 100% 보존하며, 크롤링 노이즈만 제거하여 8,000자 내외의 고밀도 표 중심 패킷으로 압축한다.
2. **Phase C-Final (마스터 청사진 및 전략 의사결정 확정 — Opus 5.5)**:
   - 상위 총괄 **`claude-opus-5-5` (Effort: High)** 수석 의장이 팩트 패킷을 입력받아 핵심 전략 딜레마(D-1 ~ D-n)를 판정하고 마스터 설계서를 최종 확정한다.
3. **정본 및 GBrain 환류**:
   - 정본 반영 후 `python D:/Brand_Command/04_Business_OS/hermes_loop/scripts/ingest_business_assets.py`를 실행하여 Hermes 및 GBrain 원장에 즉시 영구 자산화한다.
