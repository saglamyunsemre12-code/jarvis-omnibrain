// JARVIS OMNI-BRAIN CLIENT CONTROLLER (V2.0 - MATRIX EXPANSION)
let activeMode = "COUNCIL";
let isAudioEnabled = true;

// Web Audio API Sound Generator
class SoundFX {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }
  playChime() {
    if (!isAudioEnabled) return;
    this.init();
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(587.33, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.15);
    gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.3);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.3);
  }
  playSuccess() {
    if (!isAudioEnabled) return;
    this.init();
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "triangle";
    osc.frequency.setValueAtTime(523.25, this.ctx.currentTime);
    osc.frequency.setValueAtTime(659.25, this.ctx.currentTime + 0.1);
    osc.frequency.setValueAtTime(783.99, this.ctx.currentTime + 0.2);
    osc.frequency.setValueAtTime(1046.50, this.ctx.currentTime + 0.3);
    gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.5);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.5);
  }
}

const sfx = new SoundFX();

// DOM Elements
const promptInput = document.getElementById("promptInput");
const btnSend = document.getElementById("btnSend");
const btnMic = document.getElementById("btnMic");
const responseContainer = document.getElementById("responseContainer");
const councilBreakdown = document.getElementById("councilBreakdown");
const reactorLabel = document.getElementById("reactorLabel");
const reactorWrapper = document.getElementById("reactorWrapper");
const valExecTime = document.getElementById("valExecTime");
const valConsensus = document.getElementById("valConsensus");
const diagBattery = document.getElementById("diagBattery");
const diagSkillsCount = document.getElementById("diagSkillsCount");
const btnAudioToggle = document.getElementById("btnAudioToggle");

// Mode Buttons
document.querySelectorAll(".mode-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    activeMode = btn.dataset.mode;
    sfx.playChime();
    reactorLabel.innerText = `MOD: ${btn.innerText}`;
  });
});

// Audio Toggle
btnAudioToggle.addEventListener("click", () => {
  isAudioEnabled = !isAudioEnabled;
  btnAudioToggle.innerText = isAudioEnabled ? "🔊" : "🔇";
  btnAudioToggle.style.borderColor = isAudioEnabled ? "var(--cyan-core)" : "var(--border-hud)";
});

// Quick Commands
document.querySelectorAll(".cmd-pill").forEach(pill => {
  pill.addEventListener("click", () => {
    promptInput.value = pill.dataset.prompt;
    handleSend();
  });
});

// Load Diagnostics & Status
async function loadStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    if (data.system && data.system.battery) {
      const match = data.system.battery.match(/\d+%/);
      diagBattery.innerText = match ? match[0] : "AC Güçte";
    }
  } catch (err) {
    diagBattery.innerText = "Yerel Bağlantı";
  }

  try {
    const res = await fetch("/api/skills");
    const data = await res.json();
    if (data.total_skills_count) {
      diagSkillsCount.innerText = `${data.total_skills_count} Aktif Beceri/Plugin`;
    }
  } catch (err) {
    // Keep default
  }
}
loadStatus();

// Studio Quick Trigger: GitHub
document.getElementById("btnTriggerGitHub").addEventListener("click", async () => {
  sfx.playChime();
  reactorLabel.innerText = "GITHUB REPOLARI SORGULANIYOR...";
  responseContainer.innerHTML = `<div style="padding: 20px; text-align: center; color: var(--cyan-core);">[GITHUB BAĞLANTISI AKTİF] @saglamyunsemre12-code verileri çekiliyor...</div>`;
  try {
    const res = await fetch("/api/github/repos");
    const data = await res.json();
    sfx.playSuccess();
    let repoListHtml = data.repos && data.repos.length 
      ? data.repos.map(r => `<li><strong>${r.name}</strong> - ${r.description || 'Açıklama yok'} <a href="${r.url}" target="_blank" style="color:var(--cyan-core);">[Görüntüle]</a></li>`).join("")
      : "<li>Henüz oluşturulmuş repo bulunmuyor veya özel repo listesi boş.</li>";

    responseContainer.innerHTML = `
      <div style="padding: 16px;">
        <h2 style="color: var(--cyan-core); margin-bottom: 12px;">🐙 GitHub Hesabı: @saglamyunsemre12-code</h2>
        <p style="color: var(--text-muted); margin-bottom: 16px;">Doğrudan GitHub CLI üzerinden bağlandı. Yeni repo oluşturmaya ve kod itmeye hazır.</p>
        <ul style="margin-left: 20px; line-height: 1.8;">${repoListHtml}</ul>
      </div>
    `;
    councilBreakdown.innerHTML = `<div class="breakdown-section"><strong>GitHub CLI:</strong> Doğrulandı. Token ve repo izinleri tam.</div>`;
    reactorLabel.innerText = "GITHUB SENKRONİZE";
  } catch (err) {
    responseContainer.innerHTML = `<div style="color:red; padding:20px;">Hata: ${err.message}</div>`;
  }
});

// Studio Quick Trigger: Higgsfield
document.getElementById("btnTriggerHiggsfield").addEventListener("click", async () => {
  sfx.playChime();
  reactorLabel.innerText = "HIGGSFIELD SİNEMATİK PROMPT HAZIRLANIYOR...";
  try {
    const res = await fetch("/api/higgsfield/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept: "Ultra modern AI intelligence server room with glowing holographic core in 9:16 vertical format", style: "cyberpunk_tech" })
    });
    const data = await res.json();
    sfx.playSuccess();
    responseContainer.innerHTML = `
      <div style="padding: 16px;">
        <h2 style="color: var(--gold-core); margin-bottom: 8px;">🎬 Higgsfield AI Video Prompt Paketi</h2>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Safari Tab 5 (Higgsfield AI - Cinema Studio / Genjutsu) ile doğrudan uyumlu parametreler:</p>
        <div style="background: #090e18; border: 1px solid var(--border-hud); padding: 12px; border-radius: 6px; margin-bottom: 12px;">
          <strong style="color: var(--cyan-core);">Higgsfield Prompt:</strong><br>
          <p style="margin-top: 6px; color: #fff;">${data.higgsfield_prompt}</p>
        </div>
        <div style="background: #090e18; border: 1px solid var(--border-hud); padding: 12px; border-radius: 6px;">
          <strong style="color: #ef4444;">Negative Prompt:</strong><br>
          <p style="margin-top: 6px; color: #94a3b8;">${data.negative_prompt}</p>
        </div>
      </div>
    `;
    councilBreakdown.innerHTML = `<div class="breakdown-section"><strong>Higgsfield Studio:</strong> 9:16 Aspect Ratio, ARRI 35 lens preset ve 40 step render hazır.</div>`;
    reactorLabel.innerText = "HIGGSFIELD PROMPT HAZIR";
  } catch (err) {
    responseContainer.innerHTML = `<div style="color:red; padding:20px;">Hata: ${err.message}</div>`;
  }
});

// Studio Quick Trigger: ElevenLabs
document.getElementById("btnTriggerElevenLabs").addEventListener("click", async () => {
  sfx.playChime();
  reactorLabel.innerText = "ELEVENLABS SESLENDİRME METNİ OLUŞTURULUYOR...";
  try {
    const res = await fetch("/api/elevenlabs/script", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: "Sıradan sistemler hata yapar. Jarvis ise sıfır hata toleransıyla çalışır. Geleceğin zekası parmaklarının ucunda.", voice_profile: "adam_deep" })
    });
    const data = await res.json();
    sfx.playSuccess();
    responseContainer.innerHTML = `
      <div style="padding: 16px;">
        <h2 style="color: var(--emerald-core); margin-bottom: 8px;">🎙️ ElevenLabs Profesyonel Seslendirme Paketi</h2>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Safari Tab 8 (ElevenLabs Text-to-Speech) ses profili ve zamanlama:</p>
        <div style="background: #090e18; border: 1px solid var(--border-hud); padding: 12px; border-radius: 6px; margin-bottom: 12px;">
          <strong style="color: var(--cyan-core);">Seçilen Ses:</strong> ${data.profile_meta.voice_name}<br>
          <strong style="color: var(--emerald-core);">Model:</strong> ${data.model_id} (Multilingual v2)<br>
          <strong style="color: var(--gold-core);">Zamanlanmış Metin (SSML Vurguları):</strong><br>
          <p style="margin-top: 6px; font-size: 1.05rem; color: #fff;">"${data.text}"</p>
        </div>
      </div>
    `;
    councilBreakdown.innerHTML = `<div class="breakdown-section"><strong>ElevenLabs Engine:</strong> Stability: 0.5, Similarity: 0.75, Speaker Boost: On.</div>`;
    reactorLabel.innerText = "ELEVENLABS SESİ HAZIR";
  } catch (err) {
    responseContainer.innerHTML = `<div style="color:red; padding:20px;">Hata: ${err.message}</div>`;
  }
});

// Studio Quick Trigger: Remotion
document.getElementById("btnTriggerRemotion").addEventListener("click", async () => {
  sfx.playChime();
  reactorLabel.innerText = "REMOTION REACT KODU ÜRETİLİYOR...";
  try {
    const res = await fetch("/api/remotion/code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "JARVIS NEXUS", subtitle: "INFINITE NEURAL NETWORK" })
    });
    const data = await res.json();
    sfx.playSuccess();
    responseContainer.innerHTML = `
      <div style="padding: 16px;">
        <h2 style="color: #a855f7; margin-bottom: 8px;">⚛️ React Remotion Video Kurgu Bileşeni</h2>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Codex remotion-render becerisine uygun tam dinamik kod:</p>
        <pre>${escapeHtml(data.code)}</pre>
      </div>
    `;
    councilBreakdown.innerHTML = `<div class="breakdown-section"><strong>Remotion Engine:</strong> Spring animasyonu ve keyframe enterpolasyonu hazır.</div>`;
    reactorLabel.innerText = "REMOTION KODU HAZIR";
  } catch (err) {
    responseContainer.innerHTML = `<div style="color:red; padding:20px;">Hata: ${err.message}</div>`;
  }
});

// Studio Quick Trigger: Hermes Tool Forge
document.getElementById("btnTriggerForge").addEventListener("click", async () => {
  sfx.playChime();
  reactorLabel.innerText = "HERMES TOOL FORGE LİSTESİ YÜKLENİYOR...";
  try {
    const res = await fetch("/api/forge/tools");
    const data = await res.json();
    sfx.playSuccess();
    let toolsHtml = data.tools && data.tools.length 
      ? data.tools.map(t => `<li><strong>${t.tool_name}</strong> - <em>${t.description}</em> <span style="color:var(--emerald-core); font-size:0.75rem;">[AKTİF ÇALIŞTIRILABİLİR]</span></li>`).join("")
      : "<li>Henüz dinamik araç oluşturulmadı.</li>";

    responseContainer.innerHTML = `
      <div style="padding: 16px;">
        <h2 style="color: var(--emerald-core); margin-bottom: 8px;">🛠️ Hermes Dynamic Tool Forge (NousResearch Paradigm)</h2>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">JARVIS ihtiyaç duyduğu yeni araçları çalışma anında otonom olarak kodlar, test eder ve kaydeder:</p>
        <div style="background: #090e18; border: 1px solid var(--border-hud); padding: 12px; border-radius: 6px; margin-bottom: 14px;">
          <strong style="color: var(--cyan-core);">Kayıtlı Otonom Araçlar:</strong>
          <ul style="margin: 8px 0 0 16px; line-height: 1.8;">${toolsHtml}</ul>
        </div>
        <p style="font-size: 0.8rem; color: var(--text-muted);">Yeni bir araç üretmek için istem kutusuna örn: <em>"Bana döviz kuru hesaplayan bir Python aracı üret ve kaydet"</em> yazabilirsiniz.</p>
      </div>
    `;
    councilBreakdown.innerHTML = `<div class="breakdown-section"><strong>Hermes Tool Forge:</strong> Otonom Python araç motoru aktif ve hazır.</div>`;
    reactorLabel.innerText = "TOOL FORGE HAZIR";
  } catch (err) {
    responseContainer.innerHTML = `<div style="color:red; padding:20px;">Hata: ${err.message}</div>`;
  }
});

// Studio Quick Trigger: Viral Retention Analyzer
document.getElementById("btnTriggerViral").addEventListener("click", async () => {
  sfx.playChime();
  reactorLabel.innerText = "VİRAL RETENTION VE KANCA SKORLANIYOR...";
  try {
    const sampleScript = "Ultra lüks bir otelde bir fincan kahvenin tepsisi 1 santim bile kaysa Forbes denetmenleri neden notunuzu kırar? Çünkü lüks dünyasında hata yoktur.";
    const res = await fetch("/api/viral/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ script: sampleScript })
    });
    const data = await res.json();
    sfx.playSuccess();

    let abHtml = data.recommended_ab_hooks.map(h => `<li>"${h}"</li>`).join("");
    let feedbackHtml = data.audit_feedback.map(f => `<li>✓ ${f}</li>`).join("");

    responseContainer.innerHTML = `
      <div style="padding: 16px;">
        <h2 style="color: var(--gold-core); margin-bottom: 8px;">📈 Viral Kanca & Retention Analiz Raporu</h2>
        <div style="display: flex; gap: 16px; margin-bottom: 16px;">
          <div style="background:#090e18; border:1px solid var(--gold-core); padding:12px 18px; border-radius:8px;">
            <div style="font-size:0.75rem; color:var(--text-muted);">Retention Skoru:</div>
            <div style="font-family:var(--font-hud); font-size:1.8rem; color:var(--gold-core); font-weight:900;">${data.overall_retention_score}/100</div>
          </div>
          <div style="background:#090e18; border:1px solid var(--border-hud); padding:12px 18px; border-radius:8px;">
            <div style="font-size:0.75rem; color:var(--text-muted);">Tahmini Süre:</div>
            <div style="font-family:var(--font-hud); font-size:1.8rem; color:var(--cyan-core);">${data.estimated_duration_sec}s</div>
          </div>
          <div style="background:#090e18; border:1px solid var(--border-hud); padding:12px 18px; border-radius:8px;">
            <div style="font-size:0.75rem; color:var(--text-muted);">Tempo (Pacing):</div>
            <div style="font-family:var(--font-hud); font-size:1.3rem; color:var(--emerald-core); margin-top:4px;">${data.pacing_rating}</div>
          </div>
        </div>
        <div style="background: #090e18; border: 1px solid var(--border-hud); padding: 12px; border-radius: 6px; margin-bottom: 12px;">
          <strong style="color: var(--cyan-core);">Algoritma Denetim Bulguları:</strong>
          <ul style="margin: 6px 0 0 16px; font-size: 0.85rem; line-height: 1.6;">${feedbackHtml}</ul>
        </div>
        <div style="background: #090e18; border: 1px solid var(--border-hud); padding: 12px; border-radius: 6px;">
          <strong style="color: var(--gold-core);">Önerilen 3 A/B Kanca İyileştirmesi (Hormozi / kelsoy.ai):</strong>
          <ul style="margin: 6px 0 0 16px; font-size: 0.85rem; line-height: 1.6; color:#fff;">${abHtml}</ul>
        </div>
      </div>
    `;
    councilBreakdown.innerHTML = `<div class="breakdown-section"><strong>Viral Retention Analyzer:</strong> 3-Saniye kuralı, kelime temposu ve merak tetikleyicisi doğrulandı.</div>`;
    reactorLabel.innerText = "RETENTION SKORLANDI";
  } catch (err) {
    responseContainer.innerHTML = `<div style="color:red; padding:20px;">Hata: ${err.message}</div>`;
  }
});

// Send Chat Request with Real-Time SSE Streaming
async function handleSend() {
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  sfx.playChime();
  promptInput.value = "";
  
  reactorLabel.innerText = "NÖRAL KONSEY BAĞLANIYOR...";
  reactorWrapper.classList.add("thinking");
  valConsensus.innerText = "CANLI YAYIN";
  valConsensus.style.color = "var(--gold-core)";

  responseContainer.innerHTML = `
    <div style="padding: 24px; text-align: center; color: var(--cyan-core);">
      <div style="font-family: var(--font-hud); font-size: 1.1rem; margin-bottom: 8px;">[JARVIS NÖRAL AKIŞ]</div>
      <div id="liveStatusText" style="font-family: var(--font-code); font-size: 0.85rem; color: var(--emerald-core); margin-bottom: 8px;">Bağlantı kuruluyor...</div>
      <div style="font-family: var(--font-code); font-size: 0.75rem; color: var(--text-muted);">${escapeHtml(prompt)}</div>
    </div>
  `;

  const streamUrl = `/api/chat/stream?prompt=${encodeURIComponent(prompt)}&mode=${encodeURIComponent(activeMode)}`;
  const evtSource = new EventSource(streamUrl);

  evtSource.onmessage = (event) => {
    if (event.data === "[DONE]") {
      evtSource.close();
      reactorWrapper.classList.remove("thinking");
      reactorLabel.innerText = "JARVIS ÇEVRİMİÇİ";
      sfx.playSuccess();
      return;
    }

    try {
      const data = JSON.parse(event.data);

      if (data.type === "STATUS") {
        const liveStatus = document.getElementById("liveStatusText");
        if (liveStatus) liveStatus.innerText = data.message;
      } else if (data.type === "THINKING") {
        reactorLabel.innerText = `${data.agent.toUpperCase()}: ${data.status}`;
        councilBreakdown.innerHTML += `
          <div class="breakdown-section" style="animation: pulse 1s;">
            <strong style="color:var(--cyan-core);">[${data.agent} Aktif]:</strong> ${data.status}
          </div>
        `;
      } else if (data.type === "SYSTEM") {
        responseContainer.innerHTML = `
          <div style="padding: 16px;">
            <h3 style="color: var(--emerald-core); margin-bottom: 12px;">🖥️ macOS Sistem Komutu Sonucu</h3>
            <pre>${escapeHtml(data.result)}</pre>
          </div>
        `;
        valExecTime.innerText = `${data.execution_time || 0.01} sn`;
      } else if (data.master_response) {
        responseContainer.innerHTML = formatMarkdown(data.master_response);

        if (data.specialists) {
          councilBreakdown.innerHTML = `
            <div class="breakdown-section">
              <div class="breakdown-title" style="color: var(--cyan-core);">[CODEX MİMARİSİ]</div>
              <p>${escapeHtml(data.specialists.engineer_codex || "").slice(0, 280)}...</p>
            </div>
            <div class="breakdown-section">
              <div class="breakdown-title" style="color: var(--gold-core);">[CLAUDE STRATEJİSİ]</div>
              <p>${escapeHtml(data.specialists.strategist_claude || "").slice(0, 280)}...</p>
            </div>
            <div class="breakdown-section">
              <div class="breakdown-title" style="color: var(--emerald-core);">[GEMINI DOĞRULAMASI]</div>
              <p>${escapeHtml(data.specialists.analyst_gemini || "").slice(0, 280)}...</p>
            </div>
          `;
        }

        valExecTime.innerText = `${data.execution_time || 0.01} sn`;
        valConsensus.innerText = data.type === "CACHE_HIT" ? "ÖNBELLEK (0ms)" : "UZLAŞMA TAMAM";
        valConsensus.style.color = "var(--emerald-core)";
      }
    } catch (e) {
      console.error("Stream parse error:", e);
    }
  };

  evtSource.onerror = (err) => {
    evtSource.close();
    reactorWrapper.classList.remove("thinking");
    reactorLabel.innerText = "JARVIS ÇEVRİMİÇİ";
  };
}

btnSend.addEventListener("click", handleSend);
promptInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});

// Speech Recognition (Web Speech API)
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = 'tr-TR';
  recognition.continuous = false;
  recognition.interimResults = false;

  btnMic.addEventListener("click", () => {
    try {
      recognition.start();
      btnMic.classList.add("listening");
      reactorLabel.innerText = "DİNLENİYOR...";
    } catch (e) {
      recognition.stop();
      btnMic.classList.remove("listening");
    }
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    promptInput.value = transcript;
    btnMic.classList.remove("listening");
    handleSend();
  };

  recognition.onerror = () => {
    btnMic.classList.remove("listening");
    reactorLabel.innerText = "JARVIS CORE BEKLEMEDE";
  };

  recognition.onend = () => {
    btnMic.classList.remove("listening");
  };
} else {
  btnMic.style.display = "none";
}

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function formatMarkdown(text) {
  let html = escapeHtml(text);
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
  html = html.replace(/^- (.*$)/gim, '<li>$1</li>');
  html = html.replace(/```([\s\S]*?)```/g, '<pre>$1</pre>');
  html = html.replace(/\n\n/g, '<br><br>');
  return html;
}
