#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System & ORCA Performance Comprehensive Audit (system_performance_audit.py)
--------------------------------------------------------------------------
Inspects:
1. Hardware / OS Resource Utilization (RAM, Disk, CPU)
2. Running Processes & Background Resource Hogs (Orca, agy, node, python, etc.)
3. Agent Context & Conversation Bloat (transcript size, brain directory)
4. Workspace & Git Repository Health (.git size, file counts)
5. Network / LLM API Endpoint Latency (Google, Anthropic, GitHub)
"""

import os
import sys
import time
import json
import shutil
import urllib.request
import subprocess

# Windows 콘솔 UTF-8 방어
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_disk_info():
    disks = {}
    for drive in ["C:\\", "D:\\"]:
        if os.path.exists(drive):
            try:
                total, used, free = shutil.disk_usage(drive)
                disks[drive] = {
                    "total_gb": round(total / (1024**3), 1),
                    "used_gb": round(used / (1024**3), 1),
                    "free_gb": round(free / (1024**3), 1),
                    "free_pct": round(free / total * 100, 1)
                }
            except Exception as e:
                disks[drive] = str(e)
    return disks

def get_memory_and_cpu():
    res = {}
    try:
        # PowerShell CIM query for memory
        ps_cmd = "$os = Get-CimInstance Win32_OperatingSystem; [PSCustomObject]@{ TotalGB=[math]::Round($os.TotalVisibleMemorySize/1MB,2); FreeGB=[math]::Round($os.FreePhysicalMemory/1MB,2); UsedPct=[math]::Round((($os.TotalVisibleMemorySize - $os.FreePhysicalMemory)/$os.TotalVisibleMemorySize)*100,1) } | ConvertTo-Json"
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_cmd], text=True).strip()
        res["memory"] = json.loads(out)
    except Exception as e:
        res["memory"] = str(e)

    try:
        # CPU Load
        ps_cpu = "(Get-CimInstance Win32_Processor).LoadPercentage"
        out_cpu = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_cpu], text=True).strip()
        res["cpu_load_pct"] = int(out_cpu)
    except Exception as e:
        res["cpu_load_pct"] = str(e)
    return res

def get_top_processes():
    try:
        ps_cmd = """
        Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 15 Id, ProcessName, @{N='RAM_MB';E={[math]::Round($_.WorkingSet64/1MB)}}, @{N='CPU_s';E={[math]::Round($_.CPU,1)}} | ConvertTo-Json
        """
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_cmd], text=True).strip()
        return json.loads(out)
    except Exception as e:
        return str(e)

def get_orca_and_agy_processes():
    try:
        ps_cmd = """
        Get-Process | Where-Object { $_.ProcessName -match 'Orca|agy|node|python|chrome|msedge' } | Group-Object ProcessName | Select-Object Name, Count, @{N='Total_RAM_MB';E={[math]::Round(($_.Group | Measure-Object WorkingSet64 -Sum).Sum/1MB)}} | ConvertTo-Json
        """
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps_cmd], text=True).strip()
        return json.loads(out)
    except Exception as e:
        return str(e)

def get_context_and_brain_health():
    info = {}
    appdata = os.path.expanduser("~\\.gemini\\antigravity-cli")
    brain_dir = os.path.join(appdata, "brain")
    info["brain_dir"] = brain_dir
    if os.path.exists(brain_dir):
        total_size = 0
        file_count = 0
        for root, dirs, files in os.walk(brain_dir):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total_size += os.path.getsize(fp)
                    file_count += 1
                except Exception:
                    pass
        info["brain_total_mb"] = round(total_size / (1024**2), 1)
        info["brain_file_count"] = file_count
    
    # Current conversation transcript size
    conv_id = "146d15e0-0205-4977-a06f-f89bcd8d5a6a"
    conv_dir = os.path.join(brain_dir, conv_id, ".system_generated", "logs")
    if os.path.exists(conv_dir):
        trans_compact = os.path.join(conv_dir, "transcript.jsonl")
        trans_full = os.path.join(conv_dir, "transcript_full.jsonl")
        info["current_transcript_compact_mb"] = round(os.path.getsize(trans_compact) / (1024**2), 2) if os.path.exists(trans_compact) else 0
        info["current_transcript_full_mb"] = round(os.path.getsize(trans_full) / (1024**2), 2) if os.path.exists(trans_full) else 0
    return info

def get_workspace_git_health():
    ws_dir = r"C:\Users\kibae\orca\workspaces\AX_Desk_Lab\JE-Desk"
    git_dir = os.path.join(ws_dir, ".git")
    info = {"workspace": ws_dir}
    if os.path.exists(git_dir):
        total_size = 0
        for root, dirs, files in os.walk(git_dir):
            for f in files:
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except Exception:
                    pass
        info["git_dir_mb"] = round(total_size / (1024**2), 1)
    return info

def test_api_latency():
    endpoints = [
        ("GitHub", "https://api.github.com"),
        ("Google Generative Language API", "https://generativelanguage.googleapis.com"),
        ("Anthropic API", "https://api.anthropic.com")
    ]
    latencies = {}
    for name, url in endpoints:
        start = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                elapsed = round((time.time() - start) * 1000, 1)
                latencies[name] = f"{elapsed} ms (HTTP {resp.status})"
        except urllib.error.HTTPError as e:
            elapsed = round((time.time() - start) * 1000, 1)
            latencies[name] = f"{elapsed} ms (HTTP {e.code})"
        except Exception as e:
            latencies[name] = f"Timeout/Error: {str(e)}"
    return latencies

def main():
    print("=== Running System & ORCA Performance Comprehensive Audit ===")
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "disks": get_disk_info(),
        "memory_and_cpu": get_memory_and_cpu(),
        "app_process_groups": get_orca_and_agy_processes(),
        "top_processes": get_top_processes(),
        "context_brain_health": get_context_and_brain_health(),
        "workspace_git_health": get_workspace_git_health(),
        "api_latency": test_api_latency()
    }
    
    out_file = os.path.join(os.path.dirname(__file__), "..", "out", "system_performance_audit.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n[OK] Audit Complete. Saved to: {out_file}")

if __name__ == "__main__":
    main()
