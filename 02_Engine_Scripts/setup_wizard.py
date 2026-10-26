#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solo AX Onboarding Setup Wizard (Zero-Dependency)
- Reads '00_내_맞춤설정.md' or interactive terminal Q&A
- Automatically generates personalized 'AGENTS.md' and tailored 'CEO_대시보드.md'
- Guarantees clean separation of Universal Engine and User Persona
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# Windows encoding fix
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def generate_agents_md(user_name: str, company_name: str, core_tasks: list, persona_style: str) -> str:
    """Generate personalized AGENTS.md single SSOT rulebook."""
    tasks_formatted = "\n".join([f"   - {t}" for t in core_tasks if t.strip()])
    if not tasks_formatted:
        tasks_formatted = "   - 일일 업무 일정 및 핵심 태스크 관리\n   - 외부 자료 수집 및 3줄 요약\n   - 비즈니스 이메일 및 커뮤니케이션 초안 작성"

    return f"""# AGENTS.md — {company_name} (CEO 전용 AI 조종석 · 단일 정본)

- **소유자/대표**: {user_name}
- **회사/브랜드**: {company_name}
- **최종 갱신**: {datetime.now().strftime("%Y-%m-%d")}
- **단일 정본(SSOT)**: 본 파일(`AGENTS.md`) 및 `CEO_대시보드.md`

---

## 1. 대표님 핵심 비즈니스 및 주요 업무
{tasks_formatted}

---

## 2. AI 비서 행동 및 답변 원칙 (Persona)
- **성향 및 어조**: {persona_style}
- **원칙 1 (팩트 제일주의)**: 모호한 추측이나 과장 없이, 제공된 문서와 원천 데이터에 기반하여 답변합니다.
- **원칙 2 (결론 우선)**: 장황한 서론을 배제하고 핵심 결론과 3대 실행 요점을 먼저 제시합니다.
- **원칙 3 (데이터 무결성)**: 대표님의 개인 문서나 노트를 임의로 삭제하거나 덮어쓰지 않습니다.

---

## 3. 일일 운영 루프 (Daily Routine)
1. **아침 기동**: `CEO_대시보드.md`를 열고 오늘의 최우선 실행 1가지 확인.
2. **상시 수집**: 웹서핑/업무 중 `Win + A` 단축키로 필요한 텍스트를 즉시 조종석에 캡처.
3. **무인 백업**: 매일 부팅 시 백그라운드 3중 자동 백업(`universal-backup-maintenance`)으로 데이터 유실 0% 유지.
"""


def run_wizard():
    print("=" * 60)
    print(" 🚀 [Solo AX 3분 온보딩 맞춤설정 마법사]")
    print("=" * 60)

    script_dir = Path(__file__).resolve().parent
    vault_dir = (script_dir.parent / "01_Golden_Master").resolve()
    config_file = vault_dir / "00_내_맞춤설정.md"

    user_name = "대표님"
    company_name = "내 비즈니스"
    core_tasks = []
    persona_style = "정중하고 전문적이며 핵심만 명확히 요약하는 스타일"

    if config_file.exists():
        print(f"[INFO] '{config_file.name}' 작성 내용을 탐색합니다...")
        text = config_file.read_text(encoding="utf-8")
        
        # Parse 1. Name & Company
        m1 = re.search(r"1\.\s*대표님\s*성함.*?:\s*\[?(.*?)\]?$", text, re.MULTILINE)
        if m1 and m1.group(1).strip() and not m1.group(1).startswith("예:"):
            parts = [p.strip() for p in m1.group(1).split("/")]
            if len(parts) >= 1: user_name = parts[0]
            if len(parts) >= 2: company_name = parts[1]

        # Parse 2. Tasks
        m2 = re.findall(r"^\s*-\s*\[?(.*?)\]?$", text, re.MULTILINE)
        core_tasks = [t for t in m2 if t.strip() and not t.startswith("예:")]

        # Parse 3. Style
        m3 = re.search(r"3\.\s*AI\s*비서.*?:\s*\[?(.*?)\]?$", text, re.MULTILINE)
        if m3 and m3.group(1).strip() and not m3.group(1).startswith("예:"):
            persona_style = m3.group(1).strip()

    print(f"  • 대표님 성함 : {user_name}")
    print(f"  • 회사 상호   : {company_name}")
    print(f"  • 비서 성향   : {persona_style}")

    # Generate AGENTS.md
    agents_path = vault_dir / "AGENTS.md"
    agents_content = generate_agents_md(user_name, company_name, core_tasks, persona_style)
    agents_path.write_text(agents_content, encoding="utf-8")
    print(f"\n[OK] 맞춤형 AGENTS.md 생성 완료: {agents_path}")

    # Update CEO Dashboard title
    dash_path = vault_dir / "CEO_대시보드.md"
    if dash_path.exists():
        dash_text = dash_path.read_text(encoding="utf-8")
        dash_text = re.sub(r"# 🧭 CEO 조종석.*", f"# 🧭 {company_name} CEO 조종석 ({user_name} 대표)", dash_text)
        dash_path.write_text(dash_text, encoding="utf-8")
        print(f"[OK] CEO_대시보드.md 개인화 완료: {dash_path}")

    print("=" * 60)
    print(" ✨ 온보딩 맞춤화가 성공적으로 완료되었습니다!")
    print("=" * 60)


if __name__ == "__main__":
    run_wizard()
