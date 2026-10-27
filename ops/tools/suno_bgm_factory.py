#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[P5] JE Suno AI Viral Lifestyle BGM Factory (suno_bgm_factory.py)
-----------------------------------------------------------------
- 비개발자 JE를 위한 릴스/쇼츠/블로그 영상용 감성 BGM 프롬프트 자동 조율기
- 5인 전문가 자문 설계: 85~95 BPM 따뜻한 어쿠스틱/로파이, 저작권 100% 안전 Instrumental
- Zero-Dependency 순수 Python 구현 (ops/out/je_suno_presets.json 영구 보존)
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Windows 콘솔 UTF-8 방어
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PRESETS_FILE = os.path.join(BASE_DIR, "ops", "out", "je_suno_presets.json")

BGM_PRESETS = [
    {
        "id": "bgm_01",
        "title": "햇살 가득 아침 살림 (Morning Sunlight)",
        "mood": "따뜻하고 상쾌한 아침 주방 정리 & 커피 브이로그",
        "bpm": "92 BPM",
        "genre": "Acoustic Folk / Clean Pop",
        "instruments": "Nylon Acoustic Guitar, Soft Rhodes Piano, Gentle Shaker, Warm Upright Bass",
        "style_prompt": "Warm acoustic morning guitar, gentle nylon picking, cozy soft upright bass, bright airy kitchen ambiance, 92 BPM, lo-fi organic textures, uplifting hopeful, instrumental, no vocals",
        "recommended_for": "하부장 정리 비포애프터, 아침 루틴, 주방 살림 릴스",
        "duration": "30s ~ 60s"
    },
    {
        "id": "bgm_02",
        "title": "모던 키친 로파이 (Modern Kitchen Lo-Fi)",
        "mood": "차분하고 정돈된 세련된 인테리어 앤 살림 꿀템 추천",
        "bpm": "85 BPM",
        "genre": "Lo-Fi Hip Hop / Chillhop",
        "instruments": "Fender Rhodes Chords, Vinyl Crackle, Mellow Drum Groove, Deep Sub Bass",
        "style_prompt": "Chill lo-fi hip hop, cozy warm electric piano chords, subtle vinyl noise, relaxed smooth beats, 85 BPM, modern minimalist aesthetic, aesthetic vlog background, instrumental, no vocals",
        "recommended_for": "슬라이딩 선반 레일 당기는 쾌감 샷, 틈새 수납 비교 영상",
        "duration": "30s ~ 60s"
    },
    {
        "id": "bgm_03",
        "title": "초집중 미니멀 정리 ASMR (Minimal Calm)",
        "mood": "잡음 없이 말소리와 도마 소리가 선명하게 돋보이는 앰비언트",
        "bpm": "88 BPM",
        "genre": "Ambient / Calm Marimba",
        "instruments": "Soft Marimba, Gentle Celesta, Warm Pad, Subtle Ambient Foley",
        "style_prompt": "Gentle marimba raindrops, soft atmospheric warm synth pad, minimal spacious rhythm, peaceful clean kitchen ASMR companion, 88 BPM, soothing tidy home, instrumental, no vocals",
        "recommended_for": "양념통 라벨링, 오일병 정리, 팬트리 비포애프터",
        "duration": "30s ~ 60s"
    },
    {
        "id": "bgm_04",
        "title": "감성 리빙 브이로그 힐링 (Cozy Lifestyle)",
        "mood": "주말 오후의 여유롭고 기분 좋은 감성 살림 음악",
        "bpm": "90 BPM",
        "genre": "Indie Folk / Warm Acoustic",
        "instruments": "Fingerstyle Acoustic Guitar, Light Percussion, Warm Accordion, Soft Piano",
        "style_prompt": "Heartwarming indie acoustic folk, delicate fingerstyle guitar, light tambourine, sunny afternoon comfort, cozy lifestyle vlog, 90 BPM, organic cinematic feel, instrumental, no vocals",
        "recommended_for": "오늘의집 감성 홈스타일링, 주말 살림 결산 릴스",
        "duration": "30s ~ 60s"
    }
]

def load_or_create_presets():
    data = {
        "creator": "JE",
        "updated_at": datetime.now().isoformat(),
        "engine": "Suno AI v3.5 / v4 Ready",
        "total_presets": len(BGM_PRESETS),
        "presets": BGM_PRESETS
    }
    os.makedirs(os.path.dirname(PRESETS_FILE), exist_ok=True)
    with open(PRESETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

def main():
    parser = argparse.ArgumentParser(description="JE Suno AI BGM Factory")
    parser.add_argument("--list", action="store_true", help="프리셋 목록 출력")
    args = parser.parse_args()

    data = load_or_create_presets()
    print(f"[P5 OK] JE Suno BGM Factory Initialized ({data['total_presets']} Presets)")
    for p in data["presets"]:
        print(f" - [{p['bpm']}] {p['title']}: {p['genre']}")
    print(f"Saved: {PRESETS_FILE}")

if __name__ == "__main__":
    main()
