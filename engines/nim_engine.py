#!/usr/bin/env python3
"""
JARVIS NIM Engine — Ultra-Fast (max 2.0s) Non-Blocking Inference
"""

import json
import urllib.request
import urllib.error
import os

NVIDIA_KEY = os.getenv("NVIDIA_API_KEY") or "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"
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
PRIMARY_MODEL = "nvidia/nemotron-3.5-bolt-e4b"

def query_nim(prompt, system_prompt=None, model=None, max_tokens=1024, temp=0.3, timeout=2.0):
    target_model = model or PRIMARY_MODEL
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": target_model,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Accept": "application/json"
    }

    try:
        req = urllib.request.Request(NVIDIA_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[NIM Fallback: {str(e)}]"

if __name__ == "__main__":
    print(query_nim("Selam JARVIS."))
