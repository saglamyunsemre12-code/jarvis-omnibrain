#!/usr/bin/env python3
"""
JARVIS Voice Engine — macOS Native Speech Output
Speaks using high-clarity voice profiles (Daniel for EN, Yelda for TR).
"""

import subprocess
import threading

def speak_async(text, lang="tr"):
    def _speak():
        voice = "Yelda" if lang == "tr" else "Daniel"
        try:
            # Clean text from markdown formatting for cleaner speech
            clean_text = text.replace("**", "").replace("#", "").replace("`", "").strip()
            # If text is too long, only speak the first 2 sentences for high snappiness
            sentences = clean_text.split(".")
            short_speech = ". ".join(sentences[:2]) if len(sentences) > 2 else clean_text
            subprocess.run(["say", "-v", voice, short_speech], timeout=10)
        except Exception:
            try:
                # Fallback to default voice if voice not found
                subprocess.run(["say", text[:100]], timeout=10)
            except Exception:
                pass

    t = threading.Thread(target=_speak, daemon=True)
    t.start()

if __name__ == "__main__":
    speak_async("JARVIS ses motoru aktif. Tüm sistemler hazır, Emre Bey.")
