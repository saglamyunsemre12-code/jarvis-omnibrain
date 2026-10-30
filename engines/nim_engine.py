#!/usr/bin/env python3
"""
JARVIS NIM Engine — Powered by NVIDIA NIM Llama 3.2 11B
Ultra-fast, resilient, 2-retry inference engine.
"""

import json
import urllib.request
import urllib.error
import os
import time

NVIDIA_KEY = os.getenv("NVIDIA_API_KEY") or "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"
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def query_nim(prompt, system_prompt=None, model="meta/llama-3.2-11b-vision-instruct", max_tokens=1024, temp=0.25):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Accept": "application/json"
    }

    for attempt in range(2):
        try:
            req = urllib.request.Request(NVIDIA_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            return f"[NIM Engine Note: {str(e)}]"

if __name__ == "__main__":
    print(query_nim("JARVIS test ping. Respond in 5 words."))
