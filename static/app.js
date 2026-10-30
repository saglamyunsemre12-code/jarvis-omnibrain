// J.A.R.V.I.S. MARK VII // STARK INDUSTRIES HOLOGRAPHIC CLIENT ENGINE
// Complete 3D Canvas Hologram + Audio Visualizer + Speech Synthesis + Multi-AI Council

// UI & Audio State
let isAudioEnabled = true;
let currentSpecialistsData = {};
let currentMasterResponse = "";
let currentSpeakingUtterance = null;

const STATE_IDLE = "IDLE";
const STATE_PROCESSING = "PROCESSING";
const STATE_SPEAKING = "SPEAKING";
let jarvisState = STATE_IDLE;

// Web Audio API Synthesized Chimes
class StarkAudioSynthesizer {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }
  playSendChime() {
    if (!isAudioEnabled) return;
    this.init();
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(440, this.ctx.currentTime); // A4
    osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.15); // A5
    gain.gain.setValueAtTime(0.04, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.25);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.25);
  }
  playReceiveChime() {
    if (!isAudioEnabled) return;
    this.init();
    const osc1 = this.ctx.createOscillator();
    const osc2 = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc1.type = "sine";
    osc2.type = "triangle";
    osc1.frequency.setValueAtTime(523.25, this.ctx.currentTime); // C5
    osc1.frequency.setValueAtTime(783.99, this.ctx.currentTime + 0.12); // G5
    osc2.frequency.setValueAtTime(1046.50, this.ctx.currentTime + 0.12); // C6
    gain.gain.setValueAtTime(0.05, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.4);
    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(this.ctx.destination);
    osc1.start();
    osc2.start();
    osc1.stop(this.ctx.currentTime + 0.4);
    osc2.stop(this.ctx.currentTime + 0.4);
  }
}

const audioSynth = new StarkAudioSynthesizer();

// DOM Elements
const canvas = document.getElementById("jarvisCanvas");
const ctx = canvas.getContext("2d");
const oscCanvas = document.getElementById("oscCanvas");
const oscCtx = oscCanvas.getContext("2d");
const promptInput = document.getElementById("promptInput");
const btnSend = document.getElementById("btnSend");
const btnMic = document.getElementById("btnMic");
const responseHud = document.getElementById("responseHud");
const hudContent = document.getElementById("hudContent");
const btnCloseHud = document.getElementById("btnCloseHud");
const btnCopyText = document.getElementById("btnCopyText");
const btnSpeakText = document.getElementById("btnSpeakText");
const execTimeBadge = document.getElementById("execTimeBadge");
const coreStatusText = document.getElementById("coreStatusText");
const hudClock = document.getElementById("hudClock");
const btnAudioToggle = document.getElementById("btnAudioToggle");
const specialistTabs = document.getElementById("specialistTabs");

// Clock update
function updateClock() {
  const now = new Date();
  const timeStr = now.toTimeString().split(" ")[0];
  if (hudClock) hudClock.innerText = `MALIBU LAB: ${timeStr} UTC+3`;
}
setInterval(updateClock, 1000);
updateClock();

// Memory Telemetry Badge Update
async function updateMemoryBadge() {
  try {
    const res = await fetch("/api/memory");
    if (res.ok) {
      const data = await res.json();
      const memTag = document.getElementById("hudMemoryTag");
      if (memTag) {
        memTag.innerHTML = `<span>🧠 BELLEK: ${data.total_turns} TUR (${data.learned_facts_count} BİLGİ)</span>`;
      }
    }
  } catch (e) {}
}
updateMemoryBadge();

// Audio Toggle
btnAudioToggle.addEventListener("click", () => {
  isAudioEnabled = !isAudioEnabled;
  btnAudioToggle.innerHTML = `
    <span class="audio-wave-icon">${isAudioEnabled ? "🔊" : "🔇"}</span>
    <span class="audio-label">JARVIS SESİ: ${isAudioEnabled ? "AKTİF" : "KAPALI"}</span>
  `;
  if (!isAudioEnabled && window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }
});

// Close Response Card
btnCloseHud.addEventListener("click", () => {
  responseHud.classList.add("hidden");
  jarvisState = STATE_IDLE;
  coreStatusText.innerText = "J.A.R.V.I.S. MARK VII // AT YOUR SERVICE, SIR";
  coreStatusText.style.color = "var(--cyan-primary)";
  if (window.speechSynthesis) window.speechSynthesis.cancel();
});

// Copy Text
btnCopyText.addEventListener("click", () => {
  if (currentMasterResponse) {
    navigator.clipboard.writeText(currentMasterResponse);
    btnCopyText.innerText = "✓ Kopyalandı";
    setTimeout(() => { btnCopyText.innerText = "📋 Kopyala"; }, 2000);
  }
});

// Speak Current Response
btnSpeakText.addEventListener("click", () => {
  if (currentMasterResponse) {
    speakText(currentMasterResponse);
  }
});

// Specialist Tab Switcher
document.querySelectorAll(".spec-tab").forEach(tabBtn => {
  tabBtn.addEventListener("click", () => {
    document.querySelectorAll(".spec-tab").forEach(b => b.classList.remove("active"));
    tabBtn.classList.add("active");
    const tab = tabBtn.dataset.tab;
    renderTabContent(tab);
  });
});

function renderTabContent(tabKey) {
  if (tabKey === "master") {
    hudContent.innerHTML = formatMarkdown(currentMasterResponse);
    return;
  }

  // Find matching key in specialists dictionary
  let specData = currentSpecialistsData[tabKey];
  if (!specData) {
    const foundKey = Object.keys(currentSpecialistsData).find(k => k.toLowerCase().includes(tabKey.toLowerCase()));
    if (foundKey) specData = currentSpecialistsData[foundKey];
  }

  if (specData) {
    const formatted = typeof specData === "string" ? specData : JSON.stringify(specData, null, 2);
    hudContent.innerHTML = `
      <div style="border-bottom: 1px solid rgba(0,240,255,0.2); padding-bottom: 8px; margin-bottom: 14px;">
        <h3 style="color: var(--cyan-primary);">${tabKey.toUpperCase()} // YAPAY ZEKÂ ANALİZİ VE ÇIKTISI</h3>
      </div>
      <div>${formatMarkdown(formatted)}</div>
    `;
  } else {
    hudContent.innerHTML = `
      <div style="padding: 20px; text-align: center; color: var(--text-dim); font-family: var(--font-mono);">
        [${tabKey.toUpperCase()} bu görev için doğrudan çıktı üretmedi veya master konsensüse dahil edildi.]
      </div>
    `;
  }
}

// Quick Action Chips
document.querySelectorAll(".hud-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    promptInput.value = chip.dataset.prompt;
    handleSend();
  });
});

// Speech Synthesis (JARVIS Natural Voice)
function speakText(rawText) {
  if (!isAudioEnabled || !('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();

  // Extract clean sentences without markdown or code
  const clean = rawText
    .replace(/```[\s\S]*?```/g, "Kod bloğu oluşturuldu.")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/[#*>-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  // Pick first 2-3 sentences for crisp speech
  const sentences = clean.split(/(?<=[.?!])\s+/).slice(0, 3).join(" ");
  if (!sentences) return;

  const utterance = new SpeechSynthesisUtterance(sentences);
  utterance.lang = "tr-TR";
  utterance.pitch = 0.95;
  utterance.rate = 1.05;

  // Try finding high quality Turkish or British voice
  const voices = window.speechSynthesis.getVoices();
  const trVoice = voices.find(v => v.lang.startsWith("tr") || v.lang.includes("TR"));
  if (trVoice) {
    utterance.voice = trVoice;
  }

  utterance.onstart = () => {
    jarvisState = STATE_SPEAKING;
  };

  utterance.onend = () => {
    jarvisState = STATE_IDLE;
  };

  utterance.onerror = () => {
    jarvisState = STATE_IDLE;
  };

  currentSpeakingUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

// Send Command to Server
async function handleSend() {
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  audioSynth.playSendChime();
  promptInput.value = "";
  
  jarvisState = STATE_PROCESSING;
  coreStatusText.innerText = "J.A.R.V.I.S. NÖRAL MATRİS İŞLEMDE...";
  coreStatusText.style.color = "var(--gold-stark)";

  // Open HUD with processing state
  responseHud.classList.remove("hidden");
  execTimeBadge.innerText = "HESAPLANIYOR...";
  hudContent.innerHTML = `
    <div style="padding: 30px; text-align: center; color: var(--cyan-primary);">
      <div style="font-family: var(--font-hud); font-size: 1.1rem; letter-spacing: 0.15em; margin-bottom: 12px;">
        ◈ J.A.R.V.I.S. MATRİSİ ANALİZ EDİYOR ◈
      </div>
      <div style="font-family: var(--font-mono); color: var(--text-dim); font-size: 0.85rem; margin-bottom: 16px;">
        "${escapeHtml(prompt)}"
      </div>
      <div style="display: inline-block; width: 240px; height: 3px; background: rgba(0,240,255,0.2); border-radius: 2px; overflow: hidden;">
        <div style="width: 100%; height: 100%; background: var(--cyan-primary); animation: progressAnim 1.2s infinite ease-in-out;"></div>
      </div>
    </div>
  `;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, mode: "COUNCIL" })
    });

    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
    const data = await res.json();

    audioSynth.playReceiveChime();
    execTimeBadge.innerText = `${data.execution_time || 0.05}s`;
    currentMasterResponse = data.master_response || data.result || "İşlem tamamlandı.";
    currentSpecialistsData = data.specialists || {};

    // Reset tabs
    document.querySelectorAll(".spec-tab").forEach(b => b.classList.remove("active"));
    document.querySelector(".spec-tab[data-tab='master']").classList.add("active");
    renderTabContent("master");

    coreStatusText.innerText = "GÖREV TAMAMLANDI // KONSENSÜS SAĞLANDI";
    coreStatusText.style.color = "var(--cyan-primary)";

    // Speak response
    speakText(currentMasterResponse);
    updateMemoryBadge();

  } catch (err) {
    console.error("JARVIS API Error:", err);
    hudContent.innerHTML = `
      <div style="padding: 20px; color: var(--gold-stark); font-family: var(--font-mono);">
        <strong>[HATA RAPORU]:</strong> ${escapeHtml(err.message)}<br><br>
        Sistem bağlantısı yedek kanallara yönlendirildi. Lütfen komutunuzu tekrarlayınız.
      </div>
    `;
    coreStatusText.innerText = "UYARI: PROTOKOL GECİKMESİ";
    coreStatusText.style.color = "var(--gold-stark)";
    jarvisState = STATE_IDLE;
  }
}

btnSend.addEventListener("click", handleSend);
promptInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});

// Web Speech API Microphone Recognition
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
      coreStatusText.innerText = "SİZİ DİNLİYORUM EFENDİM...";
      coreStatusText.style.color = "var(--gold-stark)";
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
    coreStatusText.innerText = "J.A.R.V.I.S. MARK VII // AT YOUR SERVICE, SIR";
    coreStatusText.style.color = "var(--cyan-primary)";
  };

  recognition.onend = () => {
    btnMic.classList.remove("listening");
  };
} else {
  btnMic.style.display = "none";
}

// -------------------------------------------------------------
// 3D HOLOGRAPHIC CANVAS ENGINE (IRON MAN FILM REPLICA)
// -------------------------------------------------------------
let rotAngleY = 0;
let ringAngle1 = 0;
let ringAngle2 = 0;
let pulseTimer = 0;

// 3D Sphere Points Generation
const sphereRadius = 130;
const latLines = 12;
const lonLines = 16;
const spherePoints = [];

for (let i = 0; i <= latLines; i++) {
  const theta = (i * Math.PI) / latLines;
  const sinTheta = Math.sin(theta);
  const cosTheta = Math.cos(theta);

  for (let j = 0; j < lonLines; j++) {
    const phi = (j * 2 * Math.PI) / lonLines;
    const sinPhi = Math.sin(phi);
    const cosPhi = Math.cos(phi);

    const x = sphereRadius * sinTheta * cosPhi;
    const y = sphereRadius * cosTheta;
    const z = sphereRadius * sinTheta * sinPhi;
    spherePoints.push({ x, y, z, lat: i, lon: j });
  }
}

// Floating Core Sparks
const sparks = [];
for (let s = 0; s < 36; s++) {
  sparks.push({
    r: 60 + Math.random() * 110,
    angle: Math.random() * Math.PI * 2,
    speed: (0.01 + Math.random() * 0.02) * (Math.random() > 0.5 ? 1 : -1),
    yOff: (Math.random() - 0.5) * 60,
    size: 1 + Math.random() * 2
  });
}

function renderJarvisCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;

  // Speed modifiers by state
  let rotSpeed = 0.008;
  let waveAmp = 6;
  if (jarvisState === STATE_PROCESSING) {
    rotSpeed = 0.035;
    waveAmp = 18;
  } else if (jarvisState === STATE_SPEAKING) {
    rotSpeed = 0.018;
    waveAmp = 32;
  }

  rotAngleY += rotSpeed;
  ringAngle1 += rotSpeed * 0.8;
  ringAngle2 -= rotSpeed * 1.2;
  pulseTimer += 0.04;

  const tiltX = 0.38; // 22 degree tilt for perspective

  // 1. Draw Outer Concentric Degree Dial (Radius ~260)
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(ringAngle1 * 0.3);
  ctx.strokeStyle = "rgba(0, 240, 255, 0.22)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(0, 0, 255, 0, Math.PI * 2);
  ctx.stroke();

  // Degree ticks & text
  const totalTicks = 72;
  for (let t = 0; t < totalTicks; t++) {
    const angle = (t * 2 * Math.PI) / totalTicks;
    const isMajor = t % 9 === 0;
    const isMed = t % 3 === 0;
    const len = isMajor ? 12 : (isMed ? 7 : 4);
    const r1 = 255;
    const r2 = 255 - len;

    ctx.strokeStyle = isMajor ? "rgba(0, 240, 255, 0.75)" : "rgba(0, 240, 255, 0.25)";
    ctx.beginPath();
    ctx.moveTo(Math.cos(angle) * r1, Math.sin(angle) * r1);
    ctx.lineTo(Math.cos(angle) * r2, Math.sin(angle) * r2);
    ctx.stroke();

    if (isMajor) {
      const deg = Math.round((t * 360) / totalTicks);
      const label = `${deg.toString().padStart(3, '0')}°`;
      ctx.fillStyle = "rgba(0, 240, 255, 0.6)";
      ctx.font = "8px 'Share Tech Mono', monospace";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      const lr = 236;
      ctx.fillText(label, Math.cos(angle) * lr, Math.sin(angle) * lr);
    }
  }
  ctx.restore();

  // 2. Segmented Dashed Arc Ring (Radius ~220)
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(ringAngle2);
  ctx.strokeStyle = "rgba(0, 240, 255, 0.35)";
  ctx.lineWidth = 2;
  ctx.setLineDash([18, 12, 6, 12]);
  ctx.beginPath();
  ctx.arc(0, 0, 218, 0, Math.PI * 2);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();

  // 3. Radial Audio Frequency Waveform (64 bars around Radius 185)
  ctx.save();
  ctx.translate(cx, cy);
  const numBars = 54;
  for (let b = 0; b < numBars; b++) {
    const bAngle = (b * 2 * Math.PI) / numBars;
    const harmonic = Math.sin(b * 0.4 + pulseTimer * 2) * Math.cos(b * 0.2 - pulseTimer);
    const barHeight = 4 + Math.abs(harmonic) * waveAmp;

    const baseR = 175;
    const endR = baseR + barHeight;

    const x1 = Math.cos(bAngle) * baseR;
    const y1 = Math.sin(bAngle) * baseR;
    const x2 = Math.cos(bAngle) * endR;
    const y2 = Math.sin(bAngle) * endR;

    ctx.strokeStyle = jarvisState === STATE_PROCESSING ? "rgba(245, 158, 11, 0.75)" : "rgba(0, 240, 255, 0.65)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }
  ctx.restore();

  // 4. 3D Rotating Wireframe Hologram Sphere
  const cosY = Math.cos(rotAngleY);
  const sinY = Math.sin(rotAngleY);
  const cosX = Math.cos(tiltX);
  const sinX = Math.sin(tiltX);

  const projectedPoints = spherePoints.map(p => {
    // Rotate Y
    const x1 = p.x * cosY + p.z * sinY;
    const y1 = p.y;
    const z1 = -p.x * sinY + p.z * cosY;

    // Rotate X
    const x2 = x1;
    const y2 = y1 * cosX - z1 * sinX;
    const z2 = y1 * sinX + z1 * cosX;

    const depth = (z2 + sphereRadius) / (sphereRadius * 2); // 0 to 1
    return {
      sx: cx + x2,
      sy: cy + y2,
      depth,
      lat: p.lat,
      lon: p.lon
    };
  });

  // Draw Longitude Lines
  ctx.lineWidth = 1;
  for (let j = 0; j < lonLines; j++) {
    const lonPts = projectedPoints.filter(p => p.lon === j);
    ctx.beginPath();
    for (let k = 0; k < lonPts.length; k++) {
      const pt = lonPts[k];
      if (k === 0) ctx.moveTo(pt.sx, pt.sy);
      else ctx.lineTo(pt.sx, pt.sy);
    }
    const avgDepth = lonPts.reduce((acc, p) => acc + p.depth, 0) / lonPts.length;
    const alpha = 0.08 + avgDepth * 0.35;
    ctx.strokeStyle = `rgba(0, 240, 255, ${alpha})`;
    ctx.stroke();
  }

  // Draw Latitude Circles
  for (let i = 1; i < latLines; i++) {
    const latPts = projectedPoints.filter(p => p.lat === i);
    ctx.beginPath();
    for (let k = 0; k < latPts.length; k++) {
      const pt = latPts[k];
      if (k === 0) ctx.moveTo(pt.sx, pt.sy);
      else ctx.lineTo(pt.sx, pt.sy);
    }
    ctx.closePath();
    const avgDepth = latPts.reduce((acc, p) => acc + p.depth, 0) / latPts.length;
    const alpha = 0.08 + avgDepth * 0.35;
    ctx.strokeStyle = `rgba(0, 240, 255, ${alpha})`;
    ctx.stroke();
  }

  // 5. Floating Orbital Sparks
  sparks.forEach(s => {
    s.angle += s.speed;
    const sx = cx + Math.cos(s.angle) * s.r;
    const sy = cy + Math.sin(s.angle) * s.r * 0.4 + s.yOff;
    ctx.fillStyle = "rgba(0, 240, 255, 0.75)";
    ctx.beginPath();
    ctx.arc(sx, sy, s.size, 0, Math.PI * 2);
    ctx.fill();
  });

  // 6. Central Arc Reactor Core Glow
  const pulseCore = Math.sin(pulseTimer) * 4;
  const coreGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 55 + pulseCore);
  coreGrad.addColorStop(0, "rgba(255, 255, 255, 0.95)");
  coreGrad.addColorStop(0.25, "rgba(0, 240, 255, 0.75)");
  coreGrad.addColorStop(0.65, "rgba(0, 160, 255, 0.2)");
  coreGrad.addColorStop(1, "rgba(0, 240, 255, 0)");

  ctx.fillStyle = coreGrad;
  ctx.beginPath();
  ctx.arc(cx, cy, 55 + pulseCore, 0, Math.PI * 2);
  ctx.fill();

  // Innermost Reactor Dot
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(cx, cy, 6, 0, Math.PI * 2);
  ctx.fill();

  requestAnimationFrame(renderJarvisCanvas);
}

// -------------------------------------------------------------
// MINI OSCILLOSCOPE ENGINE (BOTTOM RIGHT HUD)
// -------------------------------------------------------------
let oscTime = 0;
function renderOscilloscope() {
  oscCtx.clearRect(0, 0, oscCanvas.width, oscCanvas.height);
  oscTime += 0.06;

  oscCtx.strokeStyle = "rgba(0, 240, 255, 0.8)";
  oscCtx.lineWidth = 1.5;
  oscCtx.beginPath();

  const w = oscCanvas.width;
  const h = oscCanvas.height;
  const mid = h / 2;
  const amp = jarvisState === STATE_SPEAKING ? 14 : (jarvisState === STATE_PROCESSING ? 10 : 4);

  for (let x = 0; x < w; x++) {
    const y = mid + Math.sin(x * 0.08 + oscTime) * Math.cos(x * 0.03 - oscTime) * amp;
    if (x === 0) oscCtx.moveTo(x, y);
    else oscCtx.lineTo(x, y);
  }
  oscCtx.stroke();

  requestAnimationFrame(renderOscilloscope);
}

// Start visual loops
requestAnimationFrame(renderJarvisCanvas);
requestAnimationFrame(renderOscilloscope);

// Helpers
function escapeHtml(text) {
  if (!text) return "";
  return text.toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function formatMarkdown(text) {
  if (!text) return "";
  let html = escapeHtml(text);
  // Code block
  html = html.replace(/```([\s\S]*?)```/g, '<pre>$1</pre>');
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  // Blockquotes
  html = html.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Inline Code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Lists
  html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
  html = html.replace(/^- (.*$)/gim, '<li>$1</li>');
  // Linebreaks
  html = html.replace(/\n\n/g, '<br><br>');
  return html;
}
