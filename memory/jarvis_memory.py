#!/usr/bin/env python3
"""
JARVIS Tiered Memory Architecture (Inspired by MemGPT & Letta)
Includes:
1. Core Memory (Human Persona & User Profile)
2. Recall Memory (Episodic Multi-Turn Conversational History)
3. Archival Memory (Persistent Learned Facts & Long-term Knowledge)
"""

import os
import json
import time
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(DATA_DIR, "conversation_history.json")
FACTS_FILE = os.path.join(DATA_DIR, "learned_facts.json")

# Default Core Persona & Human Profiles
DEFAULT_PERSONA = (
    "Sen Tony Stark'ın efsanevi yapay zekası J.A.R.V.I.S.'sin. "
    "Asil, son derece zeki, kibar (efendim / sir) ve sonuç odaklısın. "
    "Asla boş laflar, tebrikler veya 'yapmaya hazırım' gibi oyalamalar yazma. "
    "Kullanıcı bir şey istediğinde DOĞRUDAN eksiksiz kodu, senaryoyu, teknik analizi veya çözümü üret."
)

DEFAULT_HUMAN = {
    "name": "Yunus Emre Sağlam",
    "title": "AI & Otomasyon Mimarı / İçerik Üreticisi",
    "skills": ["n8n", "AI Video", "Higgsfield", "ElevenLabs", "Python", "React Remotion", "Modern Web"],
    "preferences": [
        "Sıfır hata prensibi",
        "Göz yormayan minimalist ve holografik arayüz",
        "Ezbere CV kullanımı yok; sadece doğrudan başvurularda kullanılır",
        "Doğrudan somut çıktı üretimi, boş yanıtlar yasaktır"
    ],
    "active_projects": ["JARVIS Omni-Brain", "Instagram Viral Video Otomasyonu", "n8n Cloud Hub"]
}

class JarvisMemory:
    def __init__(self):
        self.history = self._load_history()
        self.facts = self._load_facts()
        self.persona = DEFAULT_PERSONA
        self.human = DEFAULT_HUMAN

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history[-50:], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[-] History save error: {e}")

    def _load_facts(self):
        if os.path.exists(FACTS_FILE):
            try:
                with open(FACTS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        # Initial learned facts
        return {
            "creator": "Yunus Emre Sağlam",
            "voice_personality": "J.A.R.V.I.S. (Paul Bettany esintili, kibar ve asil)",
            "operating_system": "macOS Sonoma / Apple Silicon",
            "git_repo": "https://github.com/saglamyunsemre12-code/jarvis-omnibrain"
        }

    def _save_facts(self):
        try:
            with open(FACTS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.facts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[-] Facts save error: {e}")

    def add_interaction(self, user_prompt, assistant_response, execution_time=0.0):
        """
        Record a conversational turn into episodic memory.
        """
        turn = {
            "timestamp": int(time.time()),
            "time_str": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_prompt.strip(),
            "assistant": assistant_response.strip(),
            "execution_time": execution_time
        }
        self.history.append(turn)
        self._save_history()

        # Autonomous Fact Extraction (MemGPT self-learning)
        self._extract_and_learn_facts(user_prompt)

    def _extract_and_learn_facts(self, text):
        """
        Scans user statements for key persistent memory facts:
        e.g. "adım X", "şirketim Y", "bunu unutma: Z", "projeyi kaydet: W"
        """
        lower = text.lower()
        if "benim adım" in lower or "ismim" in lower:
            match = re.search(r'(?:benim adım|ismim)\s+([a-zA-ZğüşıöçĞÜŞİÖÇ\s]+)', text, re.I)
            if match:
                self.facts["user_stated_name"] = match.group(1).strip()
                self._save_facts()

        if "bunu unutma" in lower or "hafızana kaydet" in lower or "hatırla" in lower:
            clean = re.sub(r'(bunu unutma|hafızana kaydet|hatırla|aklinda tut)[:,\s]*', '', text, flags=re.I).strip()
            if clean:
                fact_id = f"fact_{int(time.time())}"
                self.facts[fact_id] = clean
                self._save_facts()

    def get_recent_history(self, limit=6):
        """
        Returns the last N dialogue turns formatted as messages for LLM context.
        """
        recent = self.history[-limit:]
        messages = []
        for t in recent:
            messages.append({"role": "user", "content": t["user"]})
            messages.append({"role": "assistant", "content": t["assistant"]})
        return messages

    def get_last_assistant_output(self):
        """
        Retrieves the most recent output generated by JARVIS.
        """
        if self.history:
            return self.history[-1]["assistant"]
        return None

    def get_context_prompt(self):
        """
        Assembles the Core Working Memory block for LLM prompts.
        """
        facts_summary = "\n".join([f"• {k}: {v}" for k, v in self.facts.items()])
        pref_summary = "\n".join([f"• {p}" for p in self.human["preferences"]])
        proj_summary = ", ".join(self.human["active_projects"])

        return f"""[J.A.R.V.I.S. CORE WORKING MEMORY (MEMGPT)]
KULLANICI: {self.human['name']} ({self.human['title']})
AKTİF PROJELER: {proj_summary}

KULLANICI TERCİHLERİ VE KURALLAR:
{pref_summary}

ÖĞRENİLEN KALICI BİLGİLER:
{facts_summary}
"""

    def get_memory_stats(self):
        return {
            "total_turns": len(self.history),
            "learned_facts_count": len(self.facts),
            "last_interaction": self.history[-1]["time_str"] if self.history else "Henüz etkileşim yok",
            "facts": self.facts
        }

    def clear_history(self):
        self.history = []
        self._save_history()
        return "Konuşma geçmişi temizlendi. Çekirdek profil ve öğrenilen bilgiler korundu."

# Singleton instance
memory = JarvisMemory()

if __name__ == "__main__":
    print(memory.get_context_prompt())
    print("Memory stats:", memory.get_memory_stats())
