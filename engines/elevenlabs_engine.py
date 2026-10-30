#!/usr/bin/env python3
"""
JARVIS ElevenLabs Engine — Professional Voice Studio & SSML Synthesis
Generates voice profiles, emotion markers, and pacing scripts for high-conversion reels and narration.
"""

import json

VOICE_PROFILES = {
    "adam_deep": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "name": "Adam (Deep & Authoritative)",
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.45,
        "use_speaker_boost": True
    },
    "rachel_calm": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "name": "Rachel (Calm & Luxury)",
        "stability": 0.65,
        "similarity_boost": 0.8,
        "style": 0.2,
        "use_speaker_boost": True
    },
    "george_storyteller": {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",
        "name": "George (Dynamic Storyteller)",
        "stability": 0.45,
        "similarity_boost": 0.85,
        "style": 0.55,
        "use_speaker_boost": True
    }
}

def generate_voice_script(raw_text, voice_profile="adam_deep", language="tr"):
    """
    Formats spoken text with pauses, emphasis, and emotion cues for ElevenLabs TTS engines.
    """
    profile = VOICE_PROFILES.get(voice_profile, VOICE_PROFILES["adam_deep"])
    
    # Process text for vocal pacing
    paced_text = raw_text.replace(". ", " ... ").replace("? ", " ...? ").replace("! ", " ! ")
    
    payload = {
        "text": paced_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": profile["stability"],
            "similarity_boost": profile["similarity_boost"],
            "style": profile["style"],
            "use_speaker_boost": profile["use_speaker_boost"]
        },
        "profile_meta": {
            "voice_name": profile["name"],
            "target_language": language
        }
    }
    return payload

if __name__ == "__main__":
    s = generate_voice_script("Forbes standartlarında bir otelde hiçbir şey tesadüf değildir.")
    print("ElevenLabs Payload:\n", json.dumps(s, ensure_ascii=False, indent=2))
