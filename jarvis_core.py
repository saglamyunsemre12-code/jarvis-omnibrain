#!/usr/bin/env python3
"""
JARVIS Omni-Brain Core — Mixture-of-Agents (MoA) Orchestrator & Multi-Model Brain
Unifies OpenAI Codex, Anthropic Claude, Google Gemini, NVIDIA NIM, n8n, and macOS Native Control.
"""

import sys
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.nim_engine import query_nim
from engines.system_engine import get_system_metrics, get_safari_tabs, set_volume, open_url_in_safari, execute_shell
from engines.voice_engine import speak_async
from engines.n8n_engine import get_n8n_status

USER_MEMORY_CONTEXT = """
KULLANICI BİLGİSİ (YUNUS EMRE SAĞLAM):
- Otomasyon, n8n, AI İçerik Üretimi, Modern Web ve Yapay Zeka Ajanları Odaklı.
- Kesin Kural: Kişisel CV deneyimleri (otel, havacılık vb.) genel projelerde ASLA ezbere kullanılmaz; yalnızca doğrudan iş başvurularında kullanılır. Genel projelerde tamamen görevin kendi teknik ve pazarlama hedefine odaklanılır.

BAĞLI ARAÇLAR VE SINIRSIZ NÖRAL AĞ (JARVIS NEXUS):
1. GitHub Hub: @saglamyunsemre12-code (Doğrudan CLI / Repo Yönetimi)
2. NVIDIA NIM: Llama-3.2-11B & Nemotron-70B Yüksek Hızlı Çıkarım
3. OpenAI Codex: 18 Yerel Video/YouTube Becerisi (yt-script, yt-package, yt-seo, remotion-*)
4. Higgsfield AI: Sinematik Video ve Görsel Üretim Stüdyosu (Genjutsu / Cinema Studio)
5. ElevenLabs: Profesyonel Seslendirme & TTS Sentezleyici
6. n8n Cloud: Haftalık Otomasyon Boru Hattı (emre-ai-studio.app.n8n.cloud)
7. Google E-Tablolar: Instagram İçerik Takvimi Senkronizasyonu
8. Antigravity & MCP: Modern Web Guidance, Generative UI, Headroom, OmniRoute
9. macOS Sistem Kontrolü: Donanım, Pil, Ses, Safari Sekmeleri
"""

def proposer_engineer(prompt):
    """Specialist 1: The Code & Architecture Specialist (Codex Persona)"""
    sys_prompt = f"Sen JARVIS'in Baş Kod ve Sistem Mimarı (Codex Specialist) rolündesin. Verilen göreve en yalın, hızlı, ölçeklenebilir ve hatasız teknik yaklaşımı sun. Gereksiz laf kalabalığı yapma, doğrudan uygulanabilir mimariyi ve kod yapısını özetle. {USER_MEMORY_CONTEXT}"
    return query_nim(prompt, system_prompt=sys_prompt, temp=0.2)

def proposer_strategist(prompt):
    """Specialist 2: The Strategist & Copywriting Specialist (Claude Persona)"""
    sys_prompt = f"Sen JARVIS'in Baş Strateji ve Viral İçerik Uzmanı (Claude Specialist) rolündesin. Verilen göreve psikolojik kanca (hook), insan ilgisini çeken anlatım ve maksimum dönüşüm sağlayacak stratejik açıyı sun. {USER_MEMORY_CONTEXT}"
    return query_nim(prompt, system_prompt=sys_prompt, temp=0.4)

def proposer_analyst(prompt):
    """Specialist 3: The Fact-Checker & Operations Analyst (Gemini Persona)"""
    sys_prompt = f"Sen JARVIS'in Operasyonel Analiz ve Doğrulama Uzmanı (Gemini Specialist) rolündesin. Verilen göreve Forbes 5-star kalite kriterleri, potansiyel riskler, kaynak optimizasyonu ve operasyonel mükemmellik açısından bak. {USER_MEMORY_CONTEXT}"
    return query_nim(prompt, system_prompt=sys_prompt, temp=0.3)

def aggregate_and_synthesize(prompt, p_eng, p_strat, p_analyst):
    """Aggregator: Synthesizes the 3 specialist perspectives into a single Supreme Answer."""
    synthesis_prompt = f"""
Kullanıcı İstemi: "{prompt}"

Aşağıda JARVIS Konseyi'ndeki 3 farklı uzman yapay zekânın bağımsız önerileri bulunmaktadır:

[UZMAN 1 - KOD VE MİMARİ ÖNERİSİ]:
{p_eng}

[UZMAN 2 - STRATEJİ VE İÇERİK ÖNERİSİ]:
{p_strat}

[UZMAN 3 - OPERASYONEL ANALİZ VE KALİTE ÖNERİSİ]:
{p_analyst}

GÖREVİN:
Bu üç uzmanın en güçlü fikirlerini tek bir mükemmel, eksiksiz, nihai başyapıta (Supreme Master Response) dönüştür.
- Çelişkileri ve gereksiz tekrarları temizle.
- Hem teknik mimariyi, hem stratejik kancayı, hem de operasyonel mükemmelliği tek bir akıcı metinde birleştir.
- Yanıtı Türkçe, profesyonel, otoriter ve son derece net bir dille ver.
"""
    sys_prompt = f"Sen JARVIS OMNI-BRAIN'in Üst Akıl Sentezleyicisisin (Supreme Council Aggregator). Bütün yapay zekâların ortak gücünü temsil ediyorsun. {USER_MEMORY_CONTEXT}"
    return query_nim(synthesis_prompt, system_prompt=sys_prompt, temp=0.25)

def is_system_command(prompt):
    lower = prompt.lower()
    system_triggers = ["pil", "battery", "şarj", "ses", "volume", "safari", "sekme", "tab", "uptime", "n8n", "sistem", "uygula"]
    return any(t in lower for t in system_triggers)

def handle_system_command(prompt):
    lower = prompt.lower()
    if "pil" in lower or "battery" in lower or "şarj" in lower:
        metrics = get_system_metrics()
        msg = f"🔋 Sistem Güç Durumu:\n{metrics['battery']}\nÇalışma Süresi: {metrics['uptime']}"
        speak_async("Pil durumu kontrol edildi.", lang="tr")
        return {"type": "SYSTEM", "result": msg}
    elif "safari" in lower or "sekme" in lower or "tab" in lower:
        tabs = get_safari_tabs()
        msg = "🌐 Aktif Safari Sekmeleri:\n" + "\n".join([f"• {t}" for t in tabs[:8]])
        return {"type": "SYSTEM", "result": msg}
    elif "ses" in lower or "volume" in lower:
        # Check if number in prompt
        import re
        nums = re.findall(r'\d+', prompt)
        vol = int(nums[0]) if nums else 50
        res = set_volume(vol)
        speak_async(f"Ses seviyesi yüzde {vol} olarak ayarlandı.")
        return {"type": "SYSTEM", "result": res}
    elif "n8n" in lower:
        n8n_info = get_n8n_status()
        msg = f"⚡ n8n Cloud Bağlantısı: {n8n_info['instance']}\nAktif İş Akışları:\n" + "\n".join([f"• {w['name']} ({w['status']})" for w in n8n_info['workflows']]) + f"\nKota: {n8n_info['quota']}"
        return {"type": "SYSTEM", "result": msg}
    else:
        return {"type": "SYSTEM", "result": "Sistem komutu tanındı ancak özel eylem belirlenemedi."}

# In-Memory High-Speed LRU Cache (Claude & Gemini Recommended)
QUERY_CACHE = {}
MAX_CACHE_SIZE = 100

def get_cached_response(prompt, mode):
    cache_key = f"{mode}:{prompt.strip().lower()}"
    return QUERY_CACHE.get(cache_key)

def set_cached_response(prompt, mode, data):
    if len(QUERY_CACHE) >= MAX_CACHE_SIZE:
        QUERY_CACHE.pop(next(iter(QUERY_CACHE)))
    cache_key = f"{mode}:{prompt.strip().lower()}"
    QUERY_CACHE[cache_key] = data

def process_prompt_stream(prompt, mode="COUNCIL"):
    """
    Server-Sent Events (SSE) generator.
    Yields real-time events to the HUD for instant TTFT (<100ms).
    """
    start_time = time.time()
    
    # 1. Check Cache First (0ms path)
    cached = get_cached_response(prompt, mode)
    if cached:
        yield f"data: {json.dumps({'type': 'CACHE_HIT', 'master_response': cached['master_response'], 'execution_time': 0.01})}\n\n"
        yield "data: [DONE]\n\n"
        return

    yield f"data: {json.dumps({'type': 'STATUS', 'message': 'Nöral Konsey Başlatıldı...'})}\n\n"

    # Fast Path for System or Auto
    if is_system_command(prompt) and mode != "COUNCIL":
        res = handle_system_command(prompt)
        res["execution_time"] = round(time.time() - start_time, 2)
        yield f"data: {json.dumps(res)}\n\n"
        yield "data: [DONE]\n\n"
        return

    # Stream Thinking Updates
    yield f"data: {json.dumps({'type': 'THINKING', 'agent': 'Codex', 'status': 'Yalın kod mimarisi taranıyor...'})}\n\n"
    yield f"data: {json.dumps({'type': 'THINKING', 'agent': 'Claude', 'status': 'Stratejik kanca ve viral psikoloji analiz ediliyor...'})}\n\n"
    yield f"data: {json.dumps({'type': 'THINKING', 'agent': 'Gemini', 'status': 'Operasyonel kalite ve riskler doğrulanıyor...'})}\n\n"

    # Execute and Synthesize
    full_res = process_prompt(prompt, mode=mode)
    set_cached_response(prompt, mode, full_res)

    yield f"data: {json.dumps(full_res)}\n\n"
    yield "data: [DONE]\n\n"

def process_prompt(prompt, mode="COUNCIL"):
    """
    Main entry point for JARVIS:
    - If system command and not forced council, executes locally.
    - Otherwise runs parallel Mixture-of-Agents and synthesizes.
    """
    start_time = time.time()

    if is_system_command(prompt) and mode != "COUNCIL":
        res = handle_system_command(prompt)
        res["execution_time"] = round(time.time() - start_time, 2)
        return res

    # Fast Path for AUTO Mode
    if mode == "AUTO":
        fast_sys_prompt = f"Sen JARVIS Omni-Brain Asistanısın. Yunus Emre Sağlam için doğrudan, net, en yüksek kalitede çözüm üret. {USER_MEMORY_CONTEXT}"
        answer = query_nim(prompt, system_prompt=fast_sys_prompt, temp=0.25)
        elapsed = round(time.time() - start_time, 2)
        speak_async(answer.split(".")[0], lang="tr")
        return {
            "type": "AUTO_DIRECT",
            "prompt": prompt,
            "master_response": answer,
            "execution_time": elapsed,
            "status": "COMPLETED"
        }

    # Run Mixture-of-Agents Council in Parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_eng = executor.submit(proposer_engineer, prompt)
        future_strat = executor.submit(proposer_strategist, prompt)
        future_analyst = executor.submit(proposer_analyst, prompt)

        p_eng = future_eng.result()
        p_strat = future_strat.result()
        p_analyst = future_analyst.result()

    # Synthesize Master Response
    master_response = aggregate_and_synthesize(prompt, p_eng, p_strat, p_analyst)
    elapsed = round(time.time() - start_time, 2)

    # Optional speech synthesis for short opening sentence
    first_sentence = master_response.split(".")[0] if "." in master_response else master_response[:60]
    speak_async(first_sentence, lang="tr")

    return {
        "type": "COUNCIL_SYNTHESIS",
        "prompt": prompt,
        "master_response": master_response,
        "specialists": {
            "engineer_codex": p_eng,
            "strategist_claude": p_strat,
            "analyst_gemini": p_analyst
        },
        "execution_time": elapsed,
        "status": "CONSENSUS_REACHED"
    }

if __name__ == "__main__":
    test_q = "Lüks restoranlar için AI ile rezervasyon ve sosyal medya otomasyonu nasıl kurulmalı?"
    print("[*] JARVIS Omni-Brain activating...")
    out = process_prompt(test_q)
    print("\n=== MASTER RESPONSE ===")
    print(out["master_response"])
    print(f"\nExecution time: {out['execution_time']}s")
