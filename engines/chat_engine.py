"""Real chat results, explicit failures, and bounded provider requests."""
import json
import socket
import threading
import time
import urllib.error
import urllib.request

from engines.nim_engine import NVIDIA_KEY, NVIDIA_URL, PRIMARY_MODEL, BACKUP_MODEL
from memory.jarvis_memory import memory

_memory_lock = threading.RLock()
SYSTEM = (
    "Sen Jarvis, Türkçe konuşan yardımcı bir asistansın. Kullanıcının istediği "
    "metni, kodu veya senaryoyu doğrudan ve kısa üret. Bu sohbetin gerçek modeli "
    "NVIDIA üzerinden çağrılıyor. Harici araç çalıştırma yeteneğin yok; web gezme, "
    "dosya değiştirme, e-posta gönderme, video üretme veya yayınlama yaptığını "
    "iddia etme. Claude, Gemini ve Codex'in bu yanıta katıldığını söyleme. "
    "İşlem istenirse yapabildiğin taslağı üret ve gereken bağlantıyı açıkla. "
    "Verilmeyen gelir, izlenme, test sonucu ve gerçekleri uydurma."
)


class ProviderError(Exception):
    pass


def request_answer(messages):
    if not NVIDIA_KEY:
        raise ProviderError("NVIDIA API anahtarı yapılandırılmamış.")
    for index, model in enumerate(dict.fromkeys([PRIMARY_MODEL, BACKUP_MODEL])):
        payload = {"model": model, "messages": messages, "max_tokens": 900,
                   "temperature": 0.3, "stream": False}
        req = urllib.request.Request(
            NVIDIA_URL, data=json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + NVIDIA_KEY,
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.load(response)
            answer = data["choices"][0]["message"]["content"]
            if not isinstance(answer, str) or not answer.strip():
                raise ProviderError("Model boş yanıt verdi. Tekrar deneyebilirsin.")
            return {"text": answer.strip(), "model": model,
                    "usage": data.get("usage"), "fallback_used": bool(index)}
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise ProviderError("NVIDIA kimlik doğrulaması başarısız; API anahtarını kontrol et.") from None
            if exc.code == 429:
                raise ProviderError("NVIDIA kullanım sınırına ulaşıldı. Daha sonra tekrar dene.") from None
            if index == 0 and (exc.code in (400, 404) or exc.code >= 500):
                continue
            raise ProviderError(f"NVIDIA isteği başarısız (HTTP {exc.code}).") from None
        except (TimeoutError, socket.timeout, urllib.error.URLError):
            if index == 0:
                continue
            raise ProviderError("NVIDIA bağlantısı zaman aşımına uğradı veya ağa erişilemedi.") from None
        except (ValueError, KeyError, IndexError, TypeError):
            raise ProviderError("NVIDIA yanıtı beklenen biçimde değil.") from None
    raise ProviderError("Kullanılabilir model yanıt vermedi.")


def process_prompt(prompt, mode="COUNCIL"):
    start = time.monotonic()
    if not isinstance(prompt, str) or not prompt.strip():
        return {"status": "ERROR", "master_response": "Lütfen bir mesaj yaz.", "specialists": {}}
    prompt = prompt.strip()
    if len(prompt) > 12000:
        return {"status": "ERROR", "master_response": "Mesaj çok uzun; 12.000 karakterin altında gönder.", "specialists": {}}
    if prompt.casefold().rstrip("?.!") in ("bağlantı durumu", "sistem durumu", "hangi ai bağlı"):
        return {"status": "LOCAL", "master_response":
                "Sohbet NVIDIA API bağlantısını kullanır; her isteğin sonucu ayrıca gösterilir. "
                "Claude/Gemini/Codex konsensüsü, otomatik yayınlama ve e-posta işlemleri bu sohbet akışına bağlı değil.",
                "specialists": {}, "execution_time": 0}
    if prompt.casefold().startswith(("hafızanda neler var", "hafızanda ne var", "hafızanı göster")):
        with _memory_lock:
            stats = memory.get_memory_stats()
        return {"status": "LOCAL", "master_response": json.dumps(stats, ensure_ascii=False, indent=2),
                "specialists": {}, "execution_time": 0}
    with _memory_lock:
        # Previous demo reports must not be treated as factual model history.
        history = [turn for turn in memory.history if turn.get("source") == "nvidia_api"][-4:]
        messages = [{"role": "system", "content": SYSTEM}]
        for turn in history:
            messages.extend([{"role": "user", "content": turn["user"][:4000]},
                             {"role": "assistant", "content": turn["assistant"][:5000]}])
    messages.append({"role": "user", "content": prompt})
    try:
        result = request_answer(messages)
    except ProviderError as exc:
        return {"status": "ERROR", "master_response": str(exc), "specialists": {},
                "execution_time": round(time.monotonic() - start, 2)}
    elapsed = round(time.monotonic() - start, 2)
    with _memory_lock:
        memory.add_interaction(prompt, result["text"], elapsed)
        memory.history[-1]["source"] = "nvidia_api"
        memory.history[-1]["model"] = result["model"]
        memory._save_history()
    return {"status": "COMPLETED", "type": "MODEL_RESPONSE", "master_response": result["text"],
            "specialists": {"nim": f"Gerçek yanıt: {result['model']}"},
            "provider": "NVIDIA", "model": result["model"], "usage": result["usage"],
            "fallback_used": result["fallback_used"], "execution_time": elapsed}


def process_prompt_stream(prompt, mode="COUNCIL"):
    yield 'data: {"type":"STATUS","message":"Model yanıtı bekleniyor"}\n\n'
    yield "data: " + json.dumps(process_prompt(prompt, mode), ensure_ascii=False) + "\n\n"
    yield "data: [DONE]\n\n"
