# 📊 PACKET_OPUS_READY: AI 공부 음악 음향 설계 및 유튜브 흥행 전략 (고농축 팩트 시트)

- **출처 문서**: `ops/research/notebooklm/Study_Music_YouTube_Strategy_20261027.md` (원문 70,791자)
- **작성 일시**: 2026-10-27
- **원칙**: `STRICT_FACT` 보존 (수치, BPM, 데시벨, 알고리즘 수식, 프롬프트 전문 무손실 압축)

---

## 1. 뇌과학·신경음향학적 공부 음악 설계 파라미터 (STRICT_FACT)

| 항목 | 최적 수치 / 파라미터 | 신경과학적 메커니즘 및 근거 |
| :--- | :--- | :--- |
| **권장 템포 (BPM)** | **55 ~ 75 BPM** (평균 60~68 BPM) | 안정기 성인·아동 심박수(60~80 bpm) 동기화, 알파파(8~12Hz) 뇌파 유도 [SR-1] |
| **리듬 구조** | 4/4박자 단일 리듬 루프, 싱코페이션(당김음) 및 폴리리듬 배제 | 리듬 불확실성 0%, 전두엽(Prefrontal Cortex) 작업 기억 간섭 원천 차단 [SR-1] |
| **주파수 제어 (EQ)** | **2,000 ~ 4,000 Hz 대역 -3dB~-6dB 감쇄**, 200Hz 이하 롤오프 | 브로카(Broca)·베르니케(Wernicke) 언어 중추 간섭 차단, 마스킹 효과 방지 [SR-1] |
| **배경 노이즈** | **핑크 노이즈($1/f$) 및 자연 백색소음 40~50 dB(A)** 레이어링 | 확률적 공명(Stochastic Resonance)으로 ADHD 및 아동 집중력 유지 [SR-1] |
| **다이내믹 레인지** | **-14 LUFS** (True Peak -1.0 dBTP), Low Crest Factor | 급작스러운 다이내믹 피크 배제, 지속적 각성 상태(Moderate Brain Arousal) 유지 [SR-1] |
| **화성 진행** | 2~4마디 반복 순환 루프 (Maj7, Min7, Sus4 중심) | 미해결 서스펜스 배제, 귀에 거슬리지 않는 예측 가능한 배경음 형성 [SR-1] |

---

## 2. Suno AI 학습용 인스트루멘탈 3대 킬러 프롬프트 (STRICT_FACT)

### [전사 공통 Exclude 방어막]
- `vocals, singing, humming, vocal chops, lyrics, heavy drops, climax, aggressive buildup, sudden transitions, harsh frequencies, piercing cymbals`

### [트랙별 정밀 Style 프롬프트]
1. **Track 4: 숲속 아침 루틴 (Forest Morning Routine)**
   - **Style**: `lo-fi acoustic, fingerpicked acoustic guitar, soft felt piano, warm tape saturation, gentle organic room reverb, dusty lo-fi drums, peaceful morning vibe, 72 BPM, instrumental`
   - **Exclude**: `vocals, singing, humming, electric guitar, heavy drop, climax, piercing cymbals, aggressive buildup, sudden transitions`
   - **음향 설계**: 어쿠스틱 핑거피킹 + 펠트 건반, 72 BPM으로 상쾌한 아침 공부 진입 유도
2. **Track 5: 조용한 도서관 재즈 (Quiet Library Jazz)**
   - **Style**: `library jazz, jazz hop, mellow felt piano, upright bass, soft brushed drums, dusty vinyl crackle, intimate room acoustics, warm analog mix, 75 BPM, instrumental`
   - **Exclude**: `vocals, vocal chops, singing, loud brass, trumpet solo, sharp cymbals, harsh hi-hats, sudden drops, climax`
   - **음향 설계**: 관악기 원천 차단, 피아노 3중주(펠트 피아노 + 업라이트 베이스 + 브러시 드럼) 75 BPM으로 깊은 몰입감 형성
3. **Track 6: 달빛 마무리 (Moonlight Wind-down)**
   - **Style**: `ambient synth, slow evolving drone, granular pad bed, sparse felt piano notes, deep sub pulse, ethereal, peaceful atmospheric soundscape, spacious reverb, 60 BPM, instrumental`
   - **Exclude**: `vocals, singing, humming, drums, percussion, beats, sudden drops, climax, sharp highs, brass`
   - **음향 설계**: 비트/타악기 완전 0%, 60 BPM 서스테인 패드와 서브 펄스로 복습 후 이완/정리 지원

---

## 3. 유튜브 BGM 플레이리스트 채널 알고리즘 흥행 공식 (STRICT_FACT)

### 가. 알고리즘 3대 핵심 지표 공식
$$\text{노출 순위 지수} = f(\text{CTR 6~10\%+}) \times f(\text{AVD 40\%+}) \times \text{세션 연장(Playlist Loop)}$$

### 나. 노출 클릭률(CTR) 극대화 시각 패키징
- **색온도**: 2700K~3500K 웜우드/스탠드 조명 + 6500K 창밖 비/풍경 대비 (대비감 30% 증가)
- **구도**: 3/4 측면에서 책/노트북에 몰입하는 인물 + 1/3 지점 황금비율 창가 데스크
- **썸네일 카피**: 모바일 가독성을 위해 텍스트는 좌측 하단 2~3단어 이내 (`Deep Focus`, `50/10 뽀모도로`, `숙제 집중`)

### 다. AVD(시청 지속시간) 유지 구조
- **첫 30초 킬러 트랙 선배치**: 인트로 0.5초 이내 즉시 진입, 60초 이탈률(55%) 억제
- **전환 크로스페이드**: 곡 간 2.0초 동일 출력 크로스페이드(Equal-Power Crossfade)로 무음 끊김 차단
- **길이 규격**: 25~30분(단기 숏세션) / 1시간(표준 스터디) / 3시간(50분 집중 + 10분 휴식 뽀모도로)

### 라. 유튜브 2026 정책 컴플라이언스 및 수익화 (YPP)
- **단일곡 무한반복 엄격 금지**: 최소 6곡 이상의 다변화된 멀티 트랙 구성 필수
- **시각적 비진정성 차단**: 단순 정지 1장 이미지 지양, 로파이 미세 루프 애니메이션(비 내림, 증기 피어오름) 결합
- **AI 생성 콘텐츠 공시**: 유튜브 스튜디오 업로드 시 '합성/변형된 콘텐츠' 체크박스 성실 표기
