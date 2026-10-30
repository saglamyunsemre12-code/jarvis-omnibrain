#!/usr/bin/env python3
"""
JARVIS Viral Retention & Hook Engine
Synthesizes kelsoy.ai YouTube Agent Skills (yt-retention, yt-package, yt-shorts)
and Alex Hormozi / MrBeast viral retention algorithms.
"""

import re
import json

def analyze_retention(script_text):
    """
    Analyzes script structure, calculates retention score, pacing, and generates 3 A/B hook improvements.
    """
    words = script_text.split()
    word_count = len(words)
    estimated_duration_sec = round(word_count / 2.5, 1) # ~150 words per minute speaking rate

    # Extract first sentence as Hook
    sentences = [s.strip() for s in re.split(r'[.!?]', script_text) if s.strip()]
    hook = sentences[0] if sentences else script_text
    hook_words = hook.split()
    hook_length = len(hook_words)

    # 1. Hook Score Calculation
    hook_score = 70
    feedback = []

    if hook_length <= 12:
        hook_score += 15
        feedback.append("Kanca uzunluğu mükemmel (12 kelimenin altında, ilk 3 saniyede tamamlanıyor).")
    elif hook_length > 18:
        hook_score -= 20
        feedback.append("Kanca çok uzun. İzleyici ilk 3 saniyede kaydırabilir; kısaltın.")

    # High retention trigger words
    trigger_words = ["neden", "asla", "sır", "gizli", "hata", "nasıl", "para", "zaman", "taktik", "forbes", "kural"]
    matched_triggers = [w for w in trigger_words if w in hook.lower()]
    if matched_triggers:
        hook_score += min(15, len(matched_triggers) * 5)
        feedback.append(f"Merak uyandıran tetikleyici kelimeler tespit edildi: {', '.join(matched_triggers)}.")
    else:
        feedback.append("Kancada güçlü bir zıtlık veya merak tetikleyicisi eksik.")

    hook_score = max(30, min(98, hook_score))

    # 2. Pacing Index
    pacing_rating = "İyi" if 25 <= estimated_duration_sec <= 45 else ("Çok Kısa" if estimated_duration_sec < 20 else "Biraz Uzun")

    # 3. Generate 3 A/B Hook Variations
    ab_hooks = [
        f"Neden çoğu kişi {hook[:35]}... yaparken büyük bir hata yapıyor?",
        f"Bunu bilmeden asla başlama: {hook[:40]}...",
        f"Herkesin doğru sandığı ama aslında tamamen yanlış olan o gerçek:"
    ]

    return {
        "overall_retention_score": hook_score,
        "estimated_duration_sec": estimated_duration_sec,
        "word_count": word_count,
        "pacing_rating": pacing_rating,
        "detected_hook": hook,
        "audit_feedback": feedback,
        "recommended_ab_hooks": ab_hooks
    }

if __name__ == "__main__":
    sample = "Ultra lüks bir otelde bir fincan kahvenin tepsisi 1 santim bile kaysa Forbes denetmenleri neden notunuzu kırar? Çünkü lüks dünyasında hata yoktur."
    res = analyze_retention(sample)
    print(json.dumps(res, ensure_ascii=False, indent=2))
