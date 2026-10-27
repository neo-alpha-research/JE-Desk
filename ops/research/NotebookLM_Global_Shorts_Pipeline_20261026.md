# NotebookLM 딥리서치 프롬프트: 글로벌 숏폼 AI 자동화 파이프라인 및 오픈소스/API 하이브리드 아키텍처

> 용도: AX_Desk_Lab의 1인 AX 솔루션 개발을 위해, 글로벌 쇼츠(유튜브 쇼츠, 인스타 릴스, 틱톡) 무인 양산 파이프라인(대본 ➔ 다국어 번역 ➔ AI 음성 ➔ FFmpeg 렌더링 ➔ 다이내믹 자막)의 기술적 아키텍처와 최적 구현 방식을 심층 리서치한다.  
> 원칙: 비공개 내부 코드나 크레덴셜은 포함하지 않으며, 실무적으로 검증된 오픈소스 구조와 API 연동 규격을 [검증 사실]과 [벤치마크 데이터] 위주로 심층 조사한다.

---

## SR-1. 숏폼 자동화 오픈소스(MoneyPrinterTurbo, ShortGPT 등)의 렌더링 코어 아키텍처 및 FFmpeg 파이프라인 분석

```
유튜브 쇼츠 및 인스타그램 릴스를 대량 자동 생성하는 대표적인 오픈소스 프로젝트(MoneyPrinterTurbo, ShortGPT, AI-Shorts, Remotion 기반 도구 등)의 비디오 합성 엔진 및 FFmpeg 파이프라인을 심층 분석해 주십시오.

1. 오픈소스별 비디오 생성 아키텍처 비교:
   - MoneyPrinterTurbo, ShortGPT, Remotion 기반 숏폼 도구의 파이프라인 단계별 처리 구조 (Script ➔ TTS ➔ B-roll 매칭 ➔ Subtitle Overlay ➔ Final Render).
   - 무거운 외부 라이브러리(Torch, OpenCV, CUDA) 없이 경량 순수 Python + FFmpeg CLI 조합만으로 동일한 렌더링 품질을 달성하기 위한 최소 아키텍처 설계 방안.

2. FFmpeg 기반 세로형(1080x1920, 9:16) 고화질 영상 합성 파라미터:
   - 오디오-비디오 타임스탬프 싱크 불일치 방지 및 프레임 드롭(Frame Drop) 방지 필터 설정 (`aresample`, `fps=30` 또는 `60`, `scale=1080:1920:force_original_aspect_ratio=increase`, `crop=1080:1920`).
   - 배경음악(BGM) 오토 덕킹(Auto-Ducking: 나레이션 음성이 나올 때 BGM 볼륨이 자동으로 줄어들고 끝날 때 복원되는 필터)의 정확한 FFmpeg 필터그래프(`sidechaincompress` 또는 `volume` 표현식) 구문.

3. 음성 타임코드 기반 자막 생성 및 스타일링 기법:
   - Whisper 타임스탬프 데이터를 ASS(Advanced Substation Alpha) 또는 SRT 형식으로 변환하여, 모바일 화면의 1/3을 차지하는 굵은 폰트(Yellow/White Bold), 테두리(Outline), 그림자(Drop-shadow), 단어 단위 팝업(Karaoke effect)을 구현하는 기술적 표준.

4. 위 내용을 비교 표("도구/방식 | 장점 | 단점 | 시스템 리소스 소모량 | 경량 데스크탑 적용 적합도")로 체계적으로 정리해 주십시오.
```

## SR-2. 다국어(스페인어 LATAM/중남미) 고품질 로컬라이제이션 및 AI 보이스(Typecast/ElevenLabs) 기계식 엔지니어링

```
한국어 원본 쇼츠를 글로벌 시장(특히 5.5억 스페인어/남미 시장)으로 확장할 때 필요한 기계식 로컬라이제이션 및 AI 음성(TTS) 합성 기술 규격을 심층 분석해 주십시오.

1. 스페인어권(중남미 vs 스페인 본토) 숏폼 번역 최적화:
   - DeepL API 및 LLM(Claude/GPT/Gemini) 프롬프트 엔지니어링을 결합하여, 스페인 본토 표현(Vosotros 등)이 아닌 멕시코/남미 표준 구어체(Tuteo, 직관적 숏폼 슬랭, 훅 문구)로 변환하는 프롬프트 및 시스템 파이프라인 규칙.
   - 직역 시 음절 수가 늘어나 영상 길이가 늘어나는 현상을 방지하는 '음절 수 제약 및 호흡 압축(Pacing Compression)' 기법.

2. AI 보이스(Typecast, ElevenLabs) 기계식 파라미터 세팅값:
   - 숏폼 시청 지속 시간(Retention)을 극대화하기 위한 배속(1.1x ~ 1.2x), 피치(Pitch), 안정성(Stability), 명료도(Clarity/Similarity Boost)의 최적 엔지니어링 수치.
   - 국내 타입캐스트(Typecast API)와 일레븐랩스(ElevenLabs Multilingual v2 API)의 레이턴시, 단가(Cost per minute), 스페인어 음성 자연스러움 및 감정 표현력 비교 분석.

3. 무인 자동화를 위한 API 통신 규격:
   - Zero-Dependency 순수 Python 환경에서 Typecast 및 ElevenLabs REST API를 호출하여 텍스트를 고품질 MP3/WAV 오디오로 받아오고, 각 문장별 재생 시간(Duration)을 밀리초 단위로 정확히 추출하는 절차.

4. 위 내용을 "언어 처리 단계 | 입력 데이터 | 처리 도구 및 파라미터 | 산출물 | 알고리즘 기여 효과" 표로 정리해 주십시오.
```

## SR-3. 플랫폼(유튜브/인스타그램/틱톡) '재사용 콘텐츠(Reused Content)' 제재 방어 및 바이럴 알고리즘 최적화 기술

```
유튜브 쇼츠 및 릴스에서 AI 대량 생성 콘텐츠가 '재사용 콘텐츠(Reused Content)' 또는 '반복적인 콘텐츠(Repetitious Content)'로 판정되어 수익 창출이 정지되거나 노출이 제한되는 것을 방지하기 위한 기술적 방어책을 심층 분석해 주십시오.

1. 플랫폼의 중복 영상 탐지 알고리즘 메커니즘:
   - 유튜브 Content ID 및 해시 기반 비디오/오디오 지문(Fingerprinting) 탐지 방식.
   - 무료 스톡 비디오(Pexels, Pixabay)를 그대로 반복 사용할 때 발생하는 패널티 구조.

2. 프로그래밍 방식의 비주얼 지터링(Visual Jittering) 및 고유화(De-duplication) 기술:
   - FFmpeg 필터 수준에서 원본 비디오 해시를 완전히 변조하는 기법: 미세 크롭(1~3% Zoom), 미세 컬러 그레이딩(Color Curves/LUT), 프레임 레이트 미세 변조, 미세 노이즈 오버레이, 미러링(Flip) 적용 방안.
   - AI 이미지 생성(Stable Diffusion/Flux)을 활용한 맞춤형 B-roll 생성 vs 스톡 영상 다중 분할 레이어링 기법의 실효성 및 공수 비교.

3. 알고리즘 초기 시드 피드(Seed Feed) 강제 할당 전략:
   - 한국 PC/IP에서 업로드 시 남미/스페인어권 현지 시드 피드로 정상 분류되도록 만드는 메타데이터(Title, Description, Tags, Audio Track Language, Default Language Metadata) 완결 구조.

4. 위 내용을 "리스크 항목 | 플랫폼 탐지 원리 | 엔지니어링 방어 기술 | 구현 복잡도 | 안전도" 표로 정리해 주십시오.
```

---

## 후속 질문

### Q1. Python 표준 라이브러리(`urllib`, `subprocess`)와 독립 실행형 `ffmpeg.exe`만으로 외부 pip 패키지 설치 없이 완전한 숏폼 렌더링 파이프라인을 구축하는 구체적인 코드 아키텍처는 어떻게 구성해야 합니까?
### Q2. MoneyPrinterTurbo의 오픈소스 코드 중 실제 운영에서 가장 자주 발생하는 3대 버그/에러(자막 줄바꿈 깨짐, Whisper 오인식 싱크 오류, 긴 영상 렌더링 멈춤)와 이에 대한 확실한 해결책은 무엇입니까?
### Q3. DeepL API 번역 결과물과 LLM(Gemini/Claude)의 교정(Post-editing) 단계를 결합할 때, 숏폼 대본 1편당 API 비용과 소요 시간을 최소화하는 최적의 워크플로우는 무엇입니까?
### Q4. 타입캐스트(Typecast) API를 직접 연동할 때, 스페인어/다국어 숏폼에 가장 적합한 추천 캐릭터 ID와 안정적인 오디오 스트리밍/다운로드 구현 팁은 무엇입니까?
### Q5. ASS(Advanced Substation Alpha) 자막 스크립트를 동적으로 생성하여 틱톡/캡컷 스타일의 통통 튀는 바운스 애니메이션과 하이라이트 색상 변화를 FFmpeg로 입히는 표준 템플릿 구문은 무엇입니까?
### Q6. 1인 사업자/개발자가 하루 10~20편의 글로벌 쇼츠를 무인 배치(Batch)로 생성하여 안전하게 관리하기 위한 데이터 구조(JSON/SQLite 장부) 및 폴더 아키텍처 권장안은 무엇입니까?
