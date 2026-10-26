; ==============================================================================
; AX_QuickKey.ahk - 1MB 무설치 포터블 AX 단축키 엔진 (AutoHotkey v2)
; - 컴파일 시 단일 ax_key.exe (약 1.2MB)로 패키징되어 무설치로 동작합니다.
; - 단축키:
;     Win + A       : 화면에서 드래그한 텍스트를 즉시 Obsidian 오늘_수집.md에 기록
;     Win + Shift + A : Obsidian CEO 조종석 창 즉시 포커스/실행
; ==============================================================================

#Requires AutoHotkey v2.0
#SingleInstance Force

TraySetIcon("shell32.dll", 44)  ; 별 모양 아이콘
A_IconTip := "Solo AX QuickKey Engine (v1.0)"

; 1. Win + A: 선택 텍스트 퀵 캡처
#a::
{
    ; 클립보드 백업
    clipSaved := A_Clipboard
    A_Clipboard := ""
    
    ; 현재 선택된 텍스트 복사 (Ctrl+C)
    Send("^c")
    if !ClipWait(0.5)
    {
        ToolTip("선택된 텍스트가 없습니다.")
        SetTimer(() => ToolTip(), -1500)
        A_Clipboard := clipSaved
        return
    }
    
    capturedText := A_Clipboard
    A_Clipboard := clipSaved  ; 기존 클립보드 복원
    
    ; 타임스탬프 생성
    timeStr := FormatTime(, "yyyy-MM-dd HH:mm:ss")
    dateStr := FormatTime(, "yyyy-MM-dd")
    
    ; 대상 볼트 경로 (기본: 상위 01_Golden_Master 또는 내 문서의 AX_Desk)
    vaultPath := A_ScriptDir . "\..\01_Golden_Master"
    if !DirExist(vaultPath)
        vaultPath := A_MyDocuments . "\AX_Desk"
    
    collectDir := vaultPath . "\지식_보관함"
    if !DirExist(collectDir)
        DirCreate(collectDir)
        
    targetFile := collectDir . "\" . dateStr . "_수집메모.md"
    
    ; 마크다운 형식으로 추가 기록
    entry := "`n`n### ⚡ 퀵 캡처 (" . timeStr . ")`n> " . StrReplace(capturedText, "`n", "`n> ") . "`n"
    FileAppend(entry, targetFile, "UTF-8")
    
    ToolTip("✓ AX 조종석에 저장되었습니다: " . targetFile)
    SetTimer(() => ToolTip(), -2000)
}

; 2. Win + Shift + A: Obsidian 조종석 열기
+#a::
{
    Run("obsidian://open")
    ToolTip("Obsidian 조종석을 엽니다.")
    SetTimer(() => ToolTip(), -1500)
}
