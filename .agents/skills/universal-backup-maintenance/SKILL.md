---
name: universal-backup-maintenance
description: |
  어느 컴퓨터(새 데스크톱, 노트북, 외장 드라이브 등)에서든 특정 폴더 하나만 지정하면
  ① 외부 라이브러리 설치 없이(Zero-Dependency, 순수 Python 내장 모듈),
  ② 스마트 캐시/빌드 폴더(node_modules, venv, pycache 등) 자동 제외 및 중복 백업(backup 폴더 재귀 압축) 100% 원천 차단,
  ③ SQLite DB 온라인 핫 스냅샷(트랜잭션 안전 무손실),
  ④ tar.gz 고효율 압축 및 SHA-256 해시 대조 복원 무결성 검증,
  ⑤ 최신 N개(기본 3회) 안전 순환 보관(Retention Rotation) 및 클라우드(Google Drive/OneDrive) 동기화,
  ⑥ 만료 임시 파일(*.tmp) 정리뿐 아니라 C: 드라이브 전사 소모성 캐시(Temp, pip, npm, crash dumps) 및 에이전트 브레인 스텝 덤프 동적 정화까지 원스톱으로 완결하는 독립형 범용 백업·유지보수 스킬.
  "백업해줘", "이 폴더 백업해줘", "정리하고 백업해줘", "주간 백업 돌려줘", "새 컴퓨터 백업 세팅해줘", "캐시 정리하고 백업해줘" 등의 요청 시 즉시 가동한다.
---

# 🛡️ Universal Backup & Maintenance (독립형 범용 백업·멀티티어 유지보수 스킬)

본 스킬은 **특정 드라이브 문자(`D:`)나 고정 경로에 얽매이지 않고**, 새 컴퓨터의 임의의 폴더를 지정하여 안전하게 백업하고, 백업 무결성 검증 후 시스템 전반의 소모성 캐시를 동적으로 정화할 수 있도록 설계된 **100% 이식 가능한(Zero-Dependency) 전사 표준 스킬**입니다.

---

## 0. 왜 어디서나 작동하는가? (Portability & Zero-Dependency)

1. **외부 패키지 설치 불필요 (pip 0개)**:
   - 파이썬 기본 내장 라이브러리(`tarfile`, `sqlite3`, `hashlib`, `pathlib`, `shutil`, `tempfile`, `argparse`)만으로 작성되어, Python 3.8 이상이 설치된 어떤 윈도우/맥/리눅스 컴퓨터에서도 `pip install` 없이 즉시 실행됩니다.
2. **Fail-Safe 순서 보장 (백업 무결성 통과 후 효율화 가동)**:
   - 타깃 워크스페이스의 압축 및 SHA-256 해시 검증, SQLite PRAGMA 무결성 검증이 100% 성공했을 때만 캐시 정화에 진입하여 데이터 안전성을 절대 보장합니다.
3. **Zero-Hardcoding 동적 경로 탐색**:
   - `tempfile.gettempdir()`, `Path.home()`, `LOCALAPPDATA` 환경변수를 통해 운영체제 공인 경로를 실시간 조회하므로, 사용자 계정명이나 드라이브 문자가 다른 컴퓨터에서도 무결하게 작동합니다.
4. **24시간 쿨다운 & 락(Lock) 무간섭 패스**:
   - 방금 생성된 작업 중인 파일은 보호하고 최소 24시간 이상 지난 소모성 임시파일만 선별하며, 다른 프로세스가 사용 중인 파일은 조용히 건너뛰어 시스템 충돌이 전혀 없습니다.
5. **실제 누적량 동적 실측 리포트**:
   - 매번 변하는 캐시 용량을 실시간으로 측정하여 실제 확보된 용량(MB/GB)과 파일 수를 `manifest.json`에 정밀 기록합니다.

---

## 1. 기본 실행 명령어 (CLI Usage)

### ① 기본 실행: 현재 폴더 백업 + 로컬 임시파일 정리
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "." --clean
```

### ② 올인원 최고 효율 실행: 백업 + C: 드라이브 전사 캐시 + 브레인 위생 일괄 정화 (가장 추천)
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "." --clean-all
```
- 백업 검증 완료 후:
  - 1단계: 타깃 폴더 내 7일 경과 `*.tmp` 정리
  - 2단계: C: 드라이브 소모성 캐시(Temp 24h 경과분, pip 다운로드 캐시, npm _npx, CrashDumps, 브라우저 셰이더) 동적 정화
  - 3단계: 과거 에이전트 브레인 step 덤프(7일 경과분) 선별 청소로 NTFS 조회 랙 해소

### ③ 다른 컴퓨터의 특정 폴더 지정 백업 + 시스템 캐시 정화
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "C:\Users\username\MyProject" --dest "C:\Backups\MyProject" --system-clean
```

### ④ 클라우드 드라이브(Google Drive / OneDrive / 외장하드) 동시 백업
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "." --cloud "G:\내 드라이브\BackupArchive" --clean-all
```

### ⑤ 사전 점검 (Dry-Run: 실제 백업 없이 파일 수/용량 확인)
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "." --dry-run
```

---

## 2. CLI 옵션 상세 안내

| 옵션 | 단축키 | 기본값 | 설명 |
| :--- | :---: | :---: | :--- |
| `--target` | `-t` | `.` (현재 폴더) | 백업할 소스 디렉터리 경로 |
| `--dest` | `-d` | `<target>/../backup` | 백업 아카이브를 저장할 폴더 (자동 생성 및 탐색 제외) |
| `--cloud` | `-c` | `None` | (선택) Google Drive, OneDrive, 외장하드 등 2차 저장소 경로 |
| `--retention` | `-r` | `3` | 유지할 최신 백업본 개수 (오래된 백업 자동 순환 삭제) |
| `--clean` | | `False` | 백업 완료 후 타깃 폴더 내 만료된 임시 파일(*.tmp) 정리 수행 |
| `--system-clean` | `-sc` | `False` | 백업 완료 후 C: 드라이브 전사 소모성 캐시(Temp, pip, npx, 덤프) 동적 정화 |
| `--brain-clean` | `-bc` | `False` | 백업 완료 후 7일 이상 경과한 과거 에이전트 브레인 step 덤프 선별 위생 청소 |
| `--clean-all` | | `False` | 로컬 정리 + 시스템 캐시 정화 + 브레인 위생 올인원 풀코스 실행 |
| `--dry-run` | | `False` | 압축을 생성하지 않고 스캔 대상 파일 수 및 용량만 진단 |

---

## 3. 생성되는 백업 산출물 및 매니페스트

백업이 완료되면 지정된 저장소에 다음과 같은 표준 산출물이 생성되며, 정화된 실측 통계가 매니페스트에 영구 보존됩니다:

```text
backup/
  ├─ 2026-10-28_090000/
  │   ├─ MyProject_2026-10-28_090000.tar.gz   (압축 아카이브)
  │   ├─ manifest.json                         (SHA-256 해시, 압축률, 동적 캐시 확보량 통계)
  │   └─ restore-guide.md                      (원클릭 복원 명령어 안내 가이드)
  └─ ... (최신 3개 보존)
```

### manifest.json 내 효율화 실측 기록 예시
```json
{
  "run_id": "backup_2026-10-28_090000",
  "verification_status": "VERIFIED_OK",
  "cleanup_execution": {
    "local": { "cleaned_count": 12, "cleaned_mb": 4.5 },
    "system": { "cleaned_files": 4136, "cleaned_mb": 813.4, "details": { ... } },
    "brain": { "cleaned_files": 250, "cleaned_mb": 18.2 }
  }
}
```

---

## 4. 새 컴퓨터 부팅 시 자동 실행 등록 방법 (선택 사항)

새 컴퓨터에서도 컴퓨터를 켜거나(부팅/로그온), 매주 월요일 아침에 자동으로 백업과 올인원 정화가 실행되도록 설정하는 방법입니다:

```powershell
# 1. 부팅/로그온 시 1분 뒤 자동 실행 등록 (기본값)
powershell -ExecutionPolicy Bypass -File .agents/skills/universal-backup-maintenance/scripts/register_startup_task.ps1 -ScheduleType Logon

# 2. 매주 월요일 오전 9시 + 부팅 시 둘 다 가동 (가장 안전한 주간 루프)
powershell -ExecutionPolicy Bypass -File .agents/skills/universal-backup-maintenance/scripts/register_startup_task.ps1 -ScheduleType Both
```
