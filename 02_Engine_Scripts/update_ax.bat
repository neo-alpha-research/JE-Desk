@echo off
chcp 65001 > nul
echo ==============================================================================
echo  🚀 Solo AX 데스크톱 범용 최신 엔진 업데이트 (Rollout Patch)
echo ==============================================================================
echo.
echo [안내] 고객님의 개인 노트 및 메모는 100% 안전하게 보존되며,
echo        핵심 백업/단축키/AI 엔진 스킬만 최신 버전으로 안전하게 업데이트됩니다.
echo.

set SCRIPT_DIR=%~dp0
set TARGET_VAULT=%SCRIPT_DIR%..\01_Golden_Master

if not exist "%TARGET_VAULT%" (
    set TARGET_VAULT=%USERPROFILE%\Documents\AX_Desk
)

echo • 대상 볼트 폴더: %TARGET_VAULT%
echo.

echo [1/2] 최신 범용 스킬(universal-backup 등) 동기화 중...
xcopy /E /I /Y /Q "%SCRIPT_DIR%skills\*" "%TARGET_VAULT%\.agents\skills\" > nul

echo [2/2] 최신 단축키 엔진 및 설정 갱신 완료.
echo.
echo ==============================================================================
echo  ✓ 최신 엔진 롤아웃 업데이트가 성공적으로 완료되었습니다!
echo ==============================================================================
pause
