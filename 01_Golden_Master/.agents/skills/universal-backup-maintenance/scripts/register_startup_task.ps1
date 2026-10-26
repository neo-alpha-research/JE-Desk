# Register Startup & Weekly Maintenance Task in Windows Task Scheduler
# Designed to run on ANY Windows PC without hardcoded paths
[CmdletBinding()]
param (
    [string]$TargetDir = "",
    [string]$TaskName = "UniversalWorkspaceBackup",
    [string]$ScheduleType = "Logon", # Logon | WeeklyMonday | Both
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$enginePy = Join-Path $scriptDir "universal_backup.py"

# Resolve target directory (default: parent of .agents or current directory)
if (-not $TargetDir) {
    # Check if inside .agents/skills/...
    if ($scriptDir -match "([A-Za-z]:\\[^;]+?)\\.agents\\skills") {
        $TargetDir = $Matches[1]
    } else {
        $TargetDir = (Get-Item ".").FullName
    }
}
$TargetDir = (Resolve-Path $TargetDir).Path

# Find Python executable
$pythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
if (-not $pythonExe) {
    $commonPy = @(
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe",
        "C:\Python311\python.exe"
    )
    foreach ($p in $commonPy) {
        if (Test-Path $p) { $pythonExe = $p; break }
    }
}

if (-not $pythonExe) {
    Write-Error "[ERROR] python.exe not found in PATH or standard locations. Please install Python."
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " [Universal Backup Task Scheduler Registration]" -ForegroundColor Cyan
Write-Host "  - Target Directory : $TargetDir"
Write-Host "  - Engine Script    : $enginePy"
Write-Host "  - Python Binary    : $pythonExe"
Write-Host "  - Task Name        : $TaskName"
Write-Host "  - Schedule Mode    : $ScheduleType"
Write-Host "=========================================================="

# Construct Arguments: Run backup with --clean and --target
$pyArgs = "`"$enginePy`" --target `"$TargetDir`" --clean"
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument $pyArgs -WorkingDirectory $TargetDir

# Construct Triggers based on ScheduleType
$triggers = @()
if ($ScheduleType -eq "Logon" -or $ScheduleType -eq "Both") {
    # Trigger 1: On User Logon with 1 minute delay
    $tLogon = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
    $tLogon.Delay = "PT1M"
    $triggers += $tLogon
}

if ($ScheduleType -eq "WeeklyMonday" -or $ScheduleType -eq "Both") {
    # Trigger 2: Every Monday morning at 09:00 AM
    $tMonday = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 09:00am
    $triggers += $tMonday
}

# Task Settings: StartWhenAvailable (catch-up if PC was off), AllowStartIfOnBatteries, StopIfGoingOnBatteries=False
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -MultipleInstances IgnoreNew

# Unregister existing task if present
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "  [INFO] Unregistering existing task '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Register Task under current user
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $triggers -Settings $settings -User $env:USERNAME | Out-Null

Write-Host "`n[SUCCESS] Scheduled Task '$TaskName' registered successfully!" -ForegroundColor Green
Write-Host "  ✓ Triggers: $($triggers.Count) active triggers ($ScheduleType)"
Write-Host "  ✓ Catch-up (StartWhenAvailable): Enabled"
Write-Host "  ✓ Battery Support: Enabled"
Write-Host "  ✓ Target Folder: $TargetDir"
Write-Host "=========================================================="
