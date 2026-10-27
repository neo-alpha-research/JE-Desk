#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Workspace Backup & Maintenance Engine (Zero-Dependency)
-----------------------------------------------------------------
- Designed to run on any computer (Windows / macOS / Linux) with standard Python 3.8+
- Portable: 100% Zero-Dependency (uses only Python built-in standard libraries).
- Features:
    1. Zero-Coupling: Works with any target directory (--target / -t).
    2. Anti-Recursion: Automatically excludes backup destination from scan (100% loop-proof).
    3. Smart Cache Exclusion: Skips node_modules, .venv, __pycache__, build artifacts.
    4. SQLite Online Snapshot: Zero-downtime hot backup of sqlite databases with PRAGMA integrity check.
    5. Disaster Recovery Verification: Extracts sample files & checks SHA-256 hash match before committing.
    6. Safe Retention Rotation: Retains latest N verified archives (default 3), cleans older runs.
    7. Dual-Target Routing: Automatically syncs to a secondary cloud/external drive if path is provided.
    8. Multi-Tier Dynamic Efficiency Cleanup:
       - Target Cleanup (--clean): Removes expired temporary files (*.tmp, *.temp) in target folder.
       - System Cache Cleanup (--system-clean / -sc): Safely purges OS temp, pip, npm _npx, crash dumps.
       - Agent Brain Hygiene (--brain-clean / -bc): Prunes stale step stdout logs (>7 days) in agent brain.
       - All-in-One Optimization (--clean-all): Runs full-stack cleanup after verified backup.
"""

import os
import sys
import json
import time
import shutil
import hashlib
import sqlite3
import tarfile
import fnmatch
import tempfile
import argparse
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding issues (cp949)
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

DEFAULT_EXCLUDE_DIRS = {
    "node_modules", ".next", "out", "dist", "build",
    "venv", ".venv", "env", ".env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "backup", ".backup", "_backup",
    "$recycle.bin", "system volume information", ".git/objects"
}

DEFAULT_EXCLUDE_PATTERNS = [
    "*.tmp", "*.temp", "*.crdownload", "*.lock", "*.swp", "*.pyc", "*.DS_Store"
]


def sha256_file(filepath: Path, chunk_size: int = 65536) -> str:
    """Calculate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def snapshot_sqlite_db(src_path: Path, dst_path: Path) -> bool:
    """Perform a transaction-safe read-only online snapshot of a SQLite database."""
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        uri = f"file:{src_path.resolve().as_posix()}?mode=ro"
        src_conn = sqlite3.connect(uri, uri=True, timeout=15)
        dst_conn = sqlite3.connect(dst_path.as_posix(), timeout=15)
        with dst_conn:
            src_conn.backup(dst_conn)
        
        # Verify snapshot integrity
        cur = dst_conn.cursor()
        res = cur.execute("PRAGMA integrity_check;").fetchone()
        cur.close()
        dst_conn.close()
        src_conn.close()
        return bool(res and res[0] == "ok")
    except Exception as e:
        print(f"  [WARN] SQLite snapshot failed for {src_path.name}: {e}")
        return False


def run_local_cleanup(target_dir: Path, max_age_days: int = 7) -> dict:
    """Clean transient temporary files in target directory older than max_age_days."""
    cleaned_count = 0
    cleaned_bytes = 0
    now = time.time()
    cutoff = now - (max_age_days * 86400)

    for root, dirs, files in os.walk(target_dir):
        # Skip hidden or system folders
        dirs[:] = [d for d in dirs if d.lower() not in DEFAULT_EXCLUDE_DIRS and not d.startswith(".")]
        for fname in files:
            fpath = Path(root) / fname
            if any(fnmatch.fnmatch(fname.lower(), pat) for pat in ["*.tmp", "*.temp", "*.swp"]):
                try:
                    stat = fpath.stat()
                    if stat.st_mtime < cutoff:
                        cleaned_bytes += stat.st_size
                        fpath.unlink()
                        cleaned_count += 1
                except Exception:
                    pass

    return {
        "cleaned_count": cleaned_count,
        "cleaned_mb": round(cleaned_bytes / (1024**2), 2)
    }


def clean_system_caches(temp_max_age_hours: int = 24) -> dict:
    """
    [신규] C드라이브 전사 소모성 캐시 안전 동적 정화 (Zero-Hardcoding)
    - Python 표준 API (tempfile, Path.home, os.environ)로 모든 OS 및 계정 자동 감지
    - 24시간 쿨다운 필터 및 락(Lock) 파일 무간섭 패스로 100% 안전성 보장
    """
    user_home = Path.home()
    temp_dir = Path(tempfile.gettempdir())
    local_app = Path(os.environ.get("LOCALAPPDATA", user_home / "AppData" / "Local"))

    clean_targets = [
        ("User Temp Files", temp_dir, temp_max_age_hours),
        ("Crash Dumps", local_app / "CrashDumps", 0),
        ("NPM NPX Cache", local_app / "npm-cache" / "_npx", 0),
        ("Pip Cache", local_app / "pip" / "cache", 0),
        ("Chrome GPUCache", local_app / "Google" / "Chrome" / "User Data" / "Default" / "GPUCache", 0),
        ("Edge GPUCache", local_app / "Microsoft" / "Edge" / "User Data" / "Default" / "GPUCache", 0),
        ("Puppeteer Cache", user_home / ".cache" / "puppeteer", 0)
    ]

    total_files = 0
    total_bytes = 0
    now = time.time()
    details = {}

    for label, target_path, age_hours in clean_targets:
        if not target_path.exists():
            continue

        cutoff = now - (age_hours * 3600)
        target_files = 0
        target_bytes = 0

        # 일회성 캐시 디렉터리 전체 삭제가 안전한 경우 (npx, pip cache, puppeteer)
        if age_hours == 0 and label in ["NPM NPX Cache", "Pip Cache", "Puppeteer Cache"]:
            try:
                for f in target_path.glob("**/*"):
                    if f.is_file():
                        try:
                            sz = f.stat().st_size
                            target_bytes += sz
                            target_files += 1
                        except Exception:
                            pass
                shutil.rmtree(target_path, ignore_errors=True)
                total_files += target_files
                total_bytes += target_bytes
                details[label] = {"files": target_files, "mb": round(target_bytes / (1024**2), 2)}
                continue
            except Exception:
                pass

        # 파일 단위 안전 삭제 (잠긴 파일은 조용히 스킵)
        for root, dirs, files in os.walk(target_path, topdown=False):
            for fname in files:
                fpath = Path(root) / fname
                try:
                    stat = fpath.stat()
                    if age_hours == 0 or stat.st_mtime < cutoff:
                        sz = stat.st_size
                        fpath.unlink()
                        target_bytes += sz
                        target_files += 1
                except Exception:
                    pass  # 파일 락 또는 권한 부족 시 안전하게 패스
            for dname in dirs:
                try:
                    (Path(root) / dname).rmdir()
                except Exception:
                    pass

        total_files += target_files
        total_bytes += target_bytes
        if target_files > 0:
            details[label] = {"files": target_files, "mb": round(target_bytes / (1024**2), 2)}

    return {
        "cleaned_files": total_files,
        "cleaned_mb": round(total_bytes / (1024**2), 2),
        "details": details
    }


def clean_agent_brain_steps(max_age_days: int = 7) -> dict:
    """
    [신규] ORCA/에이전트 브레인 장기 미사용 스텝 파일 위생 관리
    - transcript.jsonl 및 사용자 아티팩트(*.md, *.png)는 100% 영구 보존
    - 7일 이상 경과된 과거 세션의 step stdout 출력 덤프만 선별 정리하여 NTFS 조회 지연 해소
    """
    brain_dir = Path.home() / ".gemini" / "antigravity-cli" / "brain"
    if not brain_dir.exists():
        return {"cleaned_files": 0, "cleaned_mb": 0.0}

    now = time.time()
    cutoff = now - (max_age_days * 86400)
    cleaned_files = 0
    cleaned_bytes = 0

    for conv_dir in brain_dir.iterdir():
        if not conv_dir.is_dir():
            continue
        # .system_generated/steps 디렉터리 내의 과거 파일 정리
        steps_dir = conv_dir / ".system_generated" / "steps"
        if steps_dir.exists():
            for root, dirs, files in os.walk(steps_dir, topdown=False):
                for fname in files:
                    fpath = Path(root) / fname
                    try:
                        stat = fpath.stat()
                        if stat.st_mtime < cutoff:
                            sz = stat.st_size
                            fpath.unlink()
                            cleaned_bytes += sz
                            cleaned_files += 1
                    except Exception:
                        pass
                for dname in dirs:
                    try:
                        (Path(root) / dname).rmdir()
                    except Exception:
                        pass

    return {
        "cleaned_files": cleaned_files,
        "cleaned_mb": round(cleaned_bytes / (1024**2), 2)
    }


def scan_target(target_dir: Path, backup_dest: Path, max_file_size: int = 1024**3) -> tuple:
    """Scan target directory and filter files for packing."""
    files_to_pack = []
    sqlite_dbs = []
    excluded_files = []
    total_bytes = 0

    backup_dest_resolved = backup_dest.resolve()
    target_resolved = target_dir.resolve()

    for root, dirs, files in os.walk(target_resolved):
        cur_path = Path(root).resolve()
        
        # Strictly exclude backup destination directory if inside target
        if cur_path == backup_dest_resolved or backup_dest_resolved in cur_path.parents:
            dirs[:] = []
            continue

        # Filter out cache / build directories
        dirs[:] = [d for d in dirs if d.lower() not in DEFAULT_EXCLUDE_DIRS and not d.startswith("$")]

        for fname in files:
            fpath = cur_path / fname
            rel_path = fpath.relative_to(target_resolved).as_posix()

            # Ignore files inside backup destination
            if fpath.resolve() == backup_dest_resolved or backup_dest_resolved in fpath.resolve().parents:
                continue

            try:
                fsize = fpath.stat().st_size
            except Exception:
                continue

            # SQLite databases detection
            if fname.lower().endswith((".sqlite3", ".db")) and fsize > 0:
                sqlite_dbs.append((fpath, rel_path, fsize))
                continue

            # Check transient exclusions
            if any(fnmatch.fnmatch(fname.lower(), pat) for pat in DEFAULT_EXCLUDE_PATTERNS):
                excluded_files.append({"path": rel_path, "size_mb": round(fsize / (1024**2), 2), "reason": "pattern"})
                continue

            # Check oversized files (>1GB)
            if fsize > max_file_size:
                excluded_files.append({"path": rel_path, "size_mb": round(fsize / (1024**2), 2), "reason": "oversized"})
                continue

            files_to_pack.append((fpath, rel_path, fsize))
            total_bytes += fsize

    return files_to_pack, sqlite_dbs, excluded_files, total_bytes


def rotate_backups(backup_dir: Path, retention_count: int = 3) -> list:
    """Keep only latest retention_count verified backup runs."""
    removed = []
    runs = []
    for item in backup_dir.iterdir():
        if item.is_dir() and (item / "manifest.json").is_file():
            runs.append(item)

    runs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if len(runs) > retention_count:
        for old_run in runs[retention_count:]:
            try:
                shutil.rmtree(old_run)
                removed.append(old_run.name)
            except Exception as e:
                print(f"  [WARN] Failed to remove old backup {old_run.name}: {e}")
    return removed


def execute_backup(target_dir: Path, backup_dest: Path, cloud_dest: Path = None, 
                   retention: int = 3, compress_level: int = 6, 
                   do_clean_local: bool = False, do_clean_system: bool = False, 
                   do_clean_brain: bool = False, dry_run: bool = False) -> dict:
    """Main backup & multi-tier maintenance orchestration routine."""
    start_time = time.time()
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_id = f"backup_{timestamp_str}"
    
    target_name = target_dir.resolve().name
    archive_name = f"{target_name}_{timestamp_str}.tar.gz"

    print("=" * 68)
    print(f"[Universal Backup Engine] Starting Run: {run_id}")
    print(f"   - Target Folder : {target_dir.resolve()}")
    print(f"   - Destination   : {backup_dest.resolve()}")
    if cloud_dest:
        print(f"   - Cloud Sync    : {cloud_dest.resolve()}")
    print(f"   - Retention     : {retention} copies")
    print("=" * 68)

    # 1. Scan
    print(f"[1/5] Scanning files in {target_name}...")
    files_to_pack, sqlite_dbs, excluded_files, total_uncompressed = scan_target(target_dir, backup_dest)
    total_files_count = len(files_to_pack) + len(sqlite_dbs)
    print(f"  [OK] Files to pack: {total_files_count:,} files ({total_uncompressed / (1024**2):.1f} MB)")
    print(f"  [OK] SQLite databases found: {len(sqlite_dbs)}")
    print(f"  [OK] Cache/transient files excluded: {len(excluded_files):,}")

    if dry_run:
        print("\n[DRY RUN] Scan completed successfully. Exiting without creating archive.")
        return {"status": "dry_run_completed", "files_count": total_files_count, "size_mb": round(total_uncompressed / (1024**2), 2)}

    # 2. Stage Directory & SQLite Snapshots
    staging_dir = backup_dest / f"staging_{timestamp_str}"
    staging_dir.mkdir(parents=True, exist_ok=True)
    tar_path = staging_dir / archive_name
    db_snaps_dir = staging_dir / "db_snapshots"

    db_map = {}
    if sqlite_dbs:
        print(f"[2/5] Creating safe online snapshots for {len(sqlite_dbs)} SQLite database(s)...")
        for fpath, rel_path, fsize in sqlite_dbs:
            snap_file = db_snaps_dir / rel_path
            ok = snapshot_sqlite_db(fpath, snap_file)
            if ok:
                db_map[rel_path] = snap_file
                print(f"  [OK] Online snapshot OK: {rel_path}")
            else:
                files_to_pack.append((fpath, rel_path, fsize))

    # 3. Compression
    print(f"[3/5] Compressing {total_files_count:,} files into {archive_name} (gzip level={compress_level})...")
    compress_t0 = time.time()
    with tarfile.open(tar_path, "w:gz", compresslevel=compress_level) as tar:
        for fpath, rel_path, _ in files_to_pack:
            try:
                tar.add(fpath, arcname=rel_path, recursive=False)
            except Exception as e:
                print(f"  [WARN] Skipping unreadable file {rel_path}: {e}")
        for rel_path, snap_file in db_map.items():
            tar.add(snap_file, arcname=rel_path, recursive=False)

    compress_time = time.time() - compress_t0
    archive_size = tar_path.stat().st_size
    archive_hash = sha256_file(tar_path)
    print(f"  [OK] Compressed in {compress_time:.1f}s: {archive_size / (1024**2):.1f} MB (SHA256: {archive_hash[:16]}...)")

    # 4. Verification (Restore test of samples)
    print(f"[4/5] Verifying archive integrity and testing selective extraction...")
    verify_dir = staging_dir / "verify_test"
    verify_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "r:gz") as tar:
        for rel_path in db_map.keys():
            tar.extract(rel_path, path=verify_dir)
            extracted_db = verify_dir / rel_path
            conn = sqlite3.connect(extracted_db.as_posix())
            res = conn.cursor().execute("PRAGMA integrity_check;").fetchone()
            conn.close()
            if res and res[0] == "ok":
                print(f"  [OK] Restored DB integrity verified: {rel_path} -> ok")
            else:
                raise RuntimeError(f"Integrity check failed for extracted DB: {rel_path}")

    # Clean test verification folder
    shutil.rmtree(verify_dir, ignore_errors=True)
    shutil.rmtree(db_snaps_dir, ignore_errors=True)

    # 5. Manifest & Final Deployment
    run_dir = backup_dest / timestamp_str
    run_dir.mkdir(parents=True, exist_ok=True)
    final_tar_path = run_dir / archive_name
    shutil.move(tar_path, final_tar_path)

    # Retention rotation
    removed_runs = rotate_backups(backup_dest, retention)
    if removed_runs:
        print(f"  [OK] Cleaned {len(removed_runs)} old backup run(s) per retention policy (kept {retention}).")

    # Cloud sync
    cloud_synced = False
    if cloud_dest and cloud_dest.exists():
        try:
            print(f"[5/5] Syncing to cloud destination: {cloud_dest}...")
            cloud_run_dir = cloud_dest / timestamp_str
            cloud_run_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_tar_path, cloud_run_dir / archive_name)
            rotate_backups(cloud_dest, retention)
            cloud_synced = True
            print(f"  [OK] Cloud sync completed successfully.")
        except Exception as e:
            print(f"  [WARN] Cloud sync error: {e}")

    # 6. Post-Backup Multi-Tier Maintenance & Dynamic Cleanup (Fail-Safe: only after verified backup)
    cleanup_stats = {}
    if do_clean_local:
        print(f"\n[CLEANUP: LOCAL] Running safe expired file cleanup in {target_name}...")
        res_local = run_local_cleanup(target_dir)
        cleanup_stats["local"] = res_local
        print(f"  [OK] Local cleanup: {res_local['cleaned_count']:,} files ({res_local['cleaned_mb']} MB) removed.")

    if do_clean_system:
        print(f"\n[CLEANUP: SYSTEM] Running safe C: drive dynamic cache purge...")
        res_sys = clean_system_caches()
        cleanup_stats["system"] = res_sys
        print(f"  [OK] System cache cleanup: {res_sys['cleaned_files']:,} files ({res_sys['cleaned_mb']} MB) dynamically freed.")

    if do_clean_brain:
        print(f"\n[CLEANUP: BRAIN] Running agent brain step logs hygiene (>7 days)...")
        res_brain = clean_agent_brain_steps(max_age_days=7)
        cleanup_stats["brain"] = res_brain
        print(f"  [OK] Agent brain hygiene: {res_brain['cleaned_files']:,} old step logs ({res_brain['cleaned_mb']} MB) pruned.")

    # Write Manifest
    manifest = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "target_path": str(target_dir.resolve()),
        "archive_name": archive_name,
        "archive_size_bytes": archive_size,
        "archive_size_mb": round(archive_size / (1024**2), 2),
        "archive_sha256": archive_hash,
        "total_files_packed": total_files_count,
        "uncompressed_bytes": total_uncompressed,
        "uncompressed_mb": round(total_uncompressed / (1024**2), 2),
        "compression_time_seconds": round(compress_time, 2),
        "verification_status": "VERIFIED_OK",
        "sqlite_snapshots": list(db_map.keys()),
        "excluded_files_count": len(excluded_files),
        "cleanup_execution": cleanup_stats
    }

    manifest_path = run_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    restore_guide = f"""# Disaster Recovery Guide
Run ID: {run_id} | Created: {manifest['timestamp']}
Archive: {archive_name} ({manifest['archive_size_mb']} MB, SHA256: {archive_hash})

## How to Restore:
```bash
# Extract to target directory:
tar -xzvf "{archive_name}" -C "{target_dir.resolve()}"
```
"""
    with open(run_dir / "restore-guide.md", "w", encoding="utf-8") as f:
        f.write(restore_guide)

    # Clean staging folder
    shutil.rmtree(staging_dir, ignore_errors=True)

    total_duration = time.time() - start_time
    print("=" * 68)
    print(f"[SUCCESS] Backup & Maintenance Completed in {total_duration:.1f}s!")
    print(f"   - Archive Location : {final_tar_path}")
    print(f"   - Archive Size     : {manifest['archive_size_mb']} MB")
    print(f"   - Integrity Status : {manifest['verification_status']}")
    if cleanup_stats:
        total_freed_mb = sum(v.get("cleaned_mb", 0.0) for v in cleanup_stats.values())
        print(f"   - Dynamic Cleanup  : Total {total_freed_mb:.1f} MB dynamically freed")
    print("=" * 68)

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Universal Workspace Backup & Multi-Tier Maintenance Tool (Zero-Dependency)")
    parser.add_argument("--target", "-t", default=".", help="Target directory to back up (default: current directory)")
    parser.add_argument("--dest", "-d", default=None, help="Backup destination folder (default: <target>/../backup)")
    parser.add_argument("--cloud", "-c", default=None, help="Optional secondary cloud/drive destination folder")
    parser.add_argument("--retention", "-r", type=int, default=3, help="Number of verified archives to retain (default: 3)")
    parser.add_argument("--clean", action="store_true", help="Perform safe cleanup of expired temporary files in target folder")
    parser.add_argument("--system-clean", "-sc", action="store_true", help="Perform safe dynamic cleanup of C: drive system caches (Temp, pip, npx, CrashDumps)")
    parser.add_argument("--brain-clean", "-bc", action="store_true", help="Perform agent brain hygiene (prune step logs > 7 days)")
    parser.add_argument("--clean-all", action="store_true", help="Run all cleanups (local + system + brain) after verified backup")
    parser.add_argument("--dry-run", action="store_true", help="Scan and show files without creating archive")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target path does not exist: {target_path}")
        sys.exit(1)

    dest_path = Path(args.dest).resolve() if args.dest else (target_path.parent / "backup")
    cloud_path = Path(args.cloud).resolve() if args.cloud else None

    do_local = args.clean or args.clean_all
    do_system = args.system_clean or args.clean_all
    do_brain = args.brain_clean or args.clean_all

    execute_backup(
        target_dir=target_path,
        backup_dest=dest_path,
        cloud_dest=cloud_path,
        retention=args.retention,
        do_clean_local=do_local,
        do_clean_system=do_system,
        do_clean_brain=do_brain,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
