---
name: universal-backup-maintenance
description: |
  어느 컴퓨터(새 데스크톱, 노트북, 외장 드라이브 등)에서든 특정 폴더 하나만 지정하면
  ① 외부 라이브러리 설치 없이(Zero-Dependency, 순수 Python 내장 모듈),
  ② 스마트 캐시/빌드 폴더(node_modules, venv, pycache 등) 자동 제외 및 중복 백업(backup 폴더 재귀 압축) 100% 원천 차단,
  ③ SQLite DB 온라인 핫 스냅샷(트랜잭션 안전 무손실),
  ④ tar.gz 고효율 압축 및 SHA-256 해시 대조 복원 무결성 검증,
  ⑤ 최신 N개(기본 3회) 안전 순환 보관(Retention Rotation) 및 클라우드(Google Drive/OneDrive) 동기화,
  ⑥ 만료 임시 파일(*.tmp) 안심 정리(Cleanup)까지 원스톱으로 완결하는 독립형 범용 백업·유지보수 스킬.
  "백업해줘", "이 폴더 백업해줘", "정리하고 백업해줘", "주간 백업 돌려줘", "새 컴퓨터 백업 세팅해줘" 등의 요청 시 즉시 가동한다.
---

# 🛡️ Universal Backup & Maintenance (독립형 범용 백업·유지보수 스킬)

본 스킬은 **특정 드라이브 문자(`D:`)나 고정 경로에 얽매이지 않고**, 새 컴퓨터의 임의의 폴더를 지정하여 안전하게 백업하고 정리할 수 있도록 설계된 **100% 이식 가능한(Zero-Dependency) 범용 스킬**입니다.

---

## 0. 왜 어디서나 작동하는가? (Portability & Zero-Dependency)

1. **외부 패키지 설치 불필요 (pip 0개)**:
   - 파이썬 기본 내장 라이브러리(`tarfile`, `sqlite3`, `hashlib`, `pathlib`, `shutil`, `argparse`)만으로 작성되어, Python 3.8 이상이 설치된 어떤 윈도우/맥/리눅스 컴퓨터에서도 `pip install` 없이 1초 만에 즉시 실행됩니다.
2. **중복 백업(Recursive Backup) 3중 원천 차단**:
   - 백업 대상 폴더 하위에 `backup` 폴더가 있더라도 파일 탐색기가 해당 경로를 감지하는 즉시 진입을 물리적으로 차단하여, 이전 백업본이 새 백업에 중첩되어 용량이 폭증하는 문제를 100% 원천 방지합니다.
3. **스마트 캐시/임시 파일 자동 제외**:
   - `node_modules`, `.next`, `venv`, `.venv`, `__pycache__`, `.pytest_cache`, `.git/objects` 등 불필요한 빌드 부산물은 자동으로 걸러내어 아카이브 용량을 최소화합니다.
4. **SQLite 데이터베이스 안전 스냅샷**:
   - 실행 중인 SQLite DB가 있더라도 `Online Backup API`를 통해 락(Lock) 없이 읽기 전용 스냅샷을 뜨고 `PRAGMA integrity_check`로 무결성을 검증합니다.
5. **복원 무결성 사전 검증 (Disaster Recovery Verification)**:
   - 압축 후 실제 아카이브에서 파일을 임의 추출하여 SHA-256 해시를 대조하고, 검증이 성공했을 때만 최종 승인합니다.
6. **최신 3회 안전 순환 보관 (Safe Retention Rotation)**:
   - 검증된 최신 3개의 백업만 보존하고 이전 백업은 자동 정리하여 디스크 용량을 쾌적하게 유지합니다.

---

## 1. 새 컴퓨터에서 세팅하는 법 (초간단 1분 세팅)

새로운 컴퓨터를 세팅할 때는 본 스킬 폴더(`universal-backup-maintenance`)를 새 워크스페이스의 `.agents/skills/`에 복사해 넣기만 하면 끝납니다.

```text
[새 컴퓨터 워크스페이스]
  └─ .agents/
      └─ skills/
          └─ universal-backup-maintenance/
              ├─ SKILL.md
              └─ scripts/
                  └─ universal_backup.py
```

---

## 2. 기본 실행 명령어 (CLI Usage)

### ① 기본 실행: 현재 폴더 백업 + 임시파일 정리
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "." --clean
```
- 대상: 현재 작업 디렉터리 전체
- 저장 위치: 상위 폴더의 `backup/` 디렉터리에 타임스탬프별로 저장 (예: `../backup/2026-10-26_113000/`)
- 정리: 7일 이상 경과된 `*.tmp` 임시 파일 자동 정리

### ② 다른 컴퓨터의 특정 폴더 지정 백업
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "C:\Users\username\MyProject" --dest "C:\Backups\MyProject" --clean
```

### ③ 클라우드 드라이브(Google Drive / OneDrive / 외장하드) 동시 백업
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "C:\MyProject" --cloud "G:\내 드라이브\BackupArchive" --clean
```
- 로컬 저장소와 구글 드라이브 마운트 폴더 양쪽에 동시에 최신 3개씩 안전 보관됩니다.

### ④ 사전 점검 (Dry-Run: 실제 백업 없이 파일 수/용량 확인)
```powershell
python .agents/skills/universal-backup-maintenance/scripts/universal_backup.py --target "." --dry-run
```

---

## 3. CLI 옵션 상세 안내

| 옵션 | 단축키 | 기본값 | 설명 |
| :--- | :---: | :---: | :--- |
| `--target` | `-t` | `.` (현재 폴더) | 백업할 소스 디렉터리 경로 |
| `--dest` | `-d` | `<target>/../backup` | 백업 아카이브를 저장할 폴더 (자동 생성 및 탐색 제외) |
| `--cloud` | `-c` | `None` | (선택) Google Drive, OneDrive, 외장하드 등 2차 저장소 경로 |
| `--retention` | `-r` | `3` | 유지할 최신 백업본 개수 (오래된 백업 자동 순환 삭제) |
| `--clean` | | `False` | 백업 완료 후 대상 폴더 내 만료된 임시 파일(*.tmp) 정리 수행 |
| `--dry-run` | | `False` | 압축을 생성하지 않고 스캔 대상 파일 수 및 용량만 진단 |

---

## 4. 생성되는 백업 산출물

백업이 완료되면 지정된 저장소에 다음과 같은 표준 산출물이 생성됩니다:

```text
backup/
  ├─ 2026-10-26_113000/
  │   ├─ MyProject_2026-10-26_113000.tar.gz   (압축 아카이브)
  │   ├─ manifest.json                         (SHA-256 해시, 파일 수, 압축률 메타데이터)
  │   └─ restore-guide.md                      (원클릭 복원 명령어 안내 가이드)
  └─ ... (최신 3개 보존)
```

### 원클릭 복원 방법
어느 컴퓨터에서든 압축을 풀면 백업 시점의 상태로 100% 원상 복구됩니다:
```bash
tar -xzvf "MyProject_2026-10-26_113000.tar.gz" -C "복원할_폴더_경로"
```

---

## 5. 새 컴퓨터 부팅 시 자동 실행 등록 방법 (선택 사항)

새 컴퓨터에서도 컴퓨터를 켜거나(부팅/로그온), 매주 월요일 아침에 자동으로 백업이 실행되도록 설정하는 방법입니다.

### 방법 A. 원클릭 파워셸 스크립트로 자동 등록 (가장 추천)
스킬에 내장된 등록 스크립트를 실행하면 현재 컴퓨터의 파이썬 경로와 폴더를 자동 감지하여 등록을 완료합니다:

```powershell
# 1. 부팅/로그온 시 1분 뒤 자동 실행 등록 (기본값)
powershell -ExecutionPolicy Bypass -File .agents/skills/universal-backup-maintenance/scripts/register_startup_task.ps1 -ScheduleType Logon

# 2. 매주 월요일 오전 9시 + 부팅 시 둘 다 가동 (가장 안전한 주간 루프)
powershell -ExecutionPolicy Bypass -File .agents/skills/universal-backup-maintenance/scripts/register_startup_task.ps1 -ScheduleType Both

# 3. 특정 대상 폴더를 명시하여 등록할 때
powershell -ExecutionPolicy Bypass -File .agents/skills/universal-backup-maintenance/scripts/register_startup_task.ps1 -TargetDir "C:\MyWorkspace" -ScheduleType Both
```

### 방법 B. 수동 명령어 직접 등록
직접 작업 스케줄러를 등록하고자 할 때는 아래 명령어를 PowerShell에 입력합니다:

```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "`"C:\MyProject\.agents\skills\universal-backup-maintenance\scripts\universal_backup.py`" --target `"C:\MyProject`" --clean"
# 부팅/로그온 시 1분 지연 트리거
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$trigger.Delay = "PT1M"
# 노트북 배터리 환경 및 놓친 작업 부팅 즉시 실행(StartWhenAvailable) 보장
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "UniversalWorkspaceBackup" -Action $action -Trigger $trigger -Settings $settings -User $env:USERNAME
```

### 등록 해제 (원치 않을 때 삭제)
```powershell
Unregister-ScheduledTask -TaskName "UniversalWorkspaceBackup" -Confirm:$false
```
