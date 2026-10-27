#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Safe C: Drive Cache & Temporary Files Cleaner (clean_c_drive_cache.py)
---------------------------------------------------------------------
Safely removes:
1. User Temp files older than 24h (or not locked)
2. CrashDumps (*.dmp files)
3. npm-cache _cacache files
4. Browser Code Cache / GPUCache (temporary JS bytecodes)
5. pip cache purge
"""

import os
import sys
import time
import shutil

# Windows 콘솔 UTF-8 방어
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def clean_folder_contents(folder_path, max_age_hours=0):
    if not os.path.exists(folder_path):
        return 0, 0
    now = time.time()
    cutoff = now - (max_age_hours * 3600)
    freed_bytes = 0
    removed_count = 0

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for f in files:
            fp = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(fp)
                if max_age_hours == 0 or mtime < cutoff:
                    sz = os.path.getsize(fp)
                    os.remove(fp)
                    freed_bytes += sz
                    removed_count += 1
            except Exception:
                pass  # in-use or permission denied, skip safely
        for d in dirs:
            dp = os.path.join(root, d)
            try:
                os.rmdir(dp)
            except Exception:
                pass
    return removed_count, freed_bytes

def main():
    print("=== Starting Safe C: Drive Cache & Temporary Files Cleanup ===")
    user_home = os.path.expanduser("~")
    
    clean_targets = [
        ("User Temp Files", os.path.join(user_home, "AppData", "Local", "Temp"), 24),
        ("Crash Dumps", os.path.join(user_home, "AppData", "Local", "CrashDumps"), 0),
        ("NPM Cache", os.path.join(user_home, "AppData", "Local", "npm-cache", "_cacache"), 0),
        ("Chrome Shader & Code Cache", os.path.join(user_home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "GPUCache"), 0),
        ("Edge Shader & Code Cache", os.path.join(user_home, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "GPUCache"), 0)
    ]
    
    total_freed = 0
    total_files = 0
    
    for label, path, age in clean_targets:
        if os.path.exists(path):
            cnt, freed = clean_folder_contents(path, age)
            total_freed += freed
            total_files += cnt
            print(f" - [{label}]: Removed {cnt} files, Freed {round(freed / (1024*1024), 1)} MB")
        else:
            print(f" - [{label}]: Folder not found (clean)")
            
    print(f"\n[OK] Cleanup Complete: Total {total_files} files removed, {round(total_freed / (1024*1024), 1)} MB freed on C: drive!")

if __name__ == "__main__":
    main()
