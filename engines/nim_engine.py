#!/usr/bin/env python3
"""
JARVIS NIM Engine — Ultra-Fast Streaming Inference Engine
Powered by NVIDIA NIM (Nemotron 3.5 Bolt & Llama 3.2)
Supports:
- Multi-turn conversational messages (history)
- Real-time HTTP streaming to prevent socket timeouts
- Automatic token accumulation and fallback
"""

import json
import urllib.request
import urllib.error
import os
import time

NVIDIA_KEY = os.getenv("NVIDIA_API_KEY") or "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"
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
PRIMARY_MODEL = "nvidia/nemotron-3.5-bolt-e4b"
BACKUP_MODEL = "meta/llama-3.2-11b-vision-instruct"

def query_nim(prompt, system_prompt=None, history_messages=None, model=None, max_tokens=600, temp=0.3, timeout=8):
    """
    Executes a streaming query against NVIDIA NIM.
    Streams line-by-line so connections never stall.
    """
    target_model = model or PRIMARY_MODEL
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Append multi-turn history if provided
    if history_messages and isinstance(history_messages, list):
        messages.extend(history_messages)

    # Current user prompt
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": target_model,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens,
        "stream": True
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Accept": "text/event-stream"
    }

    try:
        req = urllib.request.Request(NVIDIA_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            full_text = ""
            for line in resp:
                line_str = line.decode("utf-8", errors="ignore").strip()
                if line_str.startswith("data: "):
                    data_part = line_str[6:].strip()
                    if data_part == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_part)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        full_text += delta
                    except Exception:
                        continue
            
            if full_text.strip():
                return full_text.strip()
    except Exception as e:
        # Fallback to non-streaming or backup model if streaming failed
        pass

    # Non-streaming backup attempt
    try:
        payload["stream"] = False
        payload["model"] = BACKUP_MODEL
        req2 = urllib.request.Request(NVIDIA_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req2, timeout=timeout) as resp2:
            data2 = json.loads(resp2.read().decode("utf-8"))
            return data2["choices"][0]["message"]["content"]
    except Exception as e2:
        return None

if __name__ == "__main__":
    t0 = time.time()
    res = query_nim("Güneş pillerinin verimliliği hakkında en yenilikçi 2 yaklaşımı açıkla.")
    print(f"Time: {time.time()-t0:.2f}s")
    print(res)
