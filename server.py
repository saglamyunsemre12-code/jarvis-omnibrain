#!/usr/bin/env python3
"""
JARVIS Omni-Brain HTTP Server — Ultra-Fast, Multi-Engine Meta-API
Exposes endpoints for Council (MoA), GitHub, Higgsfield, ElevenLabs, Remotion, and macOS Control.
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engines.chat_engine import process_prompt, process_prompt_stream
from engines.system_engine import get_system_metrics, get_safari_tabs, set_volume, open_url_in_safari
from engines.n8n_engine import get_n8n_status
from engines.voice_engine import speak_async
from engines.github_engine import get_github_status, list_user_repos, create_repo
from engines.higgsfield_engine import generate_higgsfield_prompt, generate_remotion_component
from engines.elevenlabs_engine import generate_voice_script
from engines.skills_indexer import get_all_indexed_skills
from engines.hermes_tool_forge import forge_tool, list_forged_tools, execute_forged_tool
from engines.crawler_engine import fetch_and_clean_markdown
from engines.retention_scorer import analyze_retention

PORT = int(os.environ.get("PORT", 8888))
HOST = "0.0.0.0"
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

class JarvisHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, code=200):
        try:
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/chat/stream":
            query_params = urllib.parse.parse_qs(parsed.query)
            prompt = query_params.get("prompt", [""])[0].strip()
            mode = query_params.get("mode", ["COUNCIL"])[0]

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            try:
                for chunk in process_prompt_stream(prompt, mode=mode):
                    self.wfile.write(chunk.encode("utf-8"))
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass

        elif parsed.path == "/api/chat":
            query_params = urllib.parse.parse_qs(parsed.query)
            prompt = query_params.get("prompt", [""])[0].strip()
            mode = query_params.get("mode", ["COUNCIL"])[0]
            if not prompt:
                self._send_json({"error": "Prompt cannot be empty"}, code=400)
                return
            result = process_prompt(prompt, mode=mode)
            self._send_json(result)

        elif parsed.path == "/api/swarm/rundown":
            self._send_json({"status": "NOT_CONNECTED", "master_response":
                            "Canlı işletme verileri bağlı değil; gelir, yayın ve destek sonucu gösterilemiyor."})

        elif parsed.path == "/api/status":
            status_data = {"status": "ONLINE", "port": PORT,
                           "chat_provider": "NVIDIA",
                           "provider_health": "checked_per_request",
                           "multi_model_consensus": False,
                           "automatic_publishing": False}
            self._send_json(status_data)

        elif parsed.path == "/api/memory":
            from memory.jarvis_memory import memory
            self._send_json(memory.get_memory_stats())

        elif parsed.path == "/api/skills":
            self._send_json(get_all_indexed_skills())

        elif parsed.path == "/api/forge/tools":
            self._send_json({"tools": list_forged_tools()})

        elif parsed.path == "/api/github/repos":
            self._send_json({"repos": list_user_repos(10)})

        elif parsed.path == "/api/tabs":
            self._send_json({"tabs": get_safari_tabs()})

        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8")
        
        try:
            req_data = json.loads(post_body) if post_body else {}
        except Exception:
            req_data = {}

        if parsed.path == "/api/chat":
            prompt = req_data.get("prompt", "").strip()
            mode = req_data.get("mode", "COUNCIL")
            
            if not prompt:
                self._send_json({"error": "Prompt cannot be empty"}, code=400)
                return

            try:
                result = process_prompt(prompt, mode=mode)
                self._send_json(result, code=502 if result.get("status") == "ERROR" else 200)
            except Exception:
                self._send_json({"status": "ERROR", "master_response": "Sunucu isteği tamamlayamadı."}, code=500)

        elif parsed.path == "/api/memory/clear":
            from memory.jarvis_memory import memory
            res = memory.clear_history()
            self._send_json({"result": res, "status": "CLEARED"})

        elif parsed.path == "/api/higgsfield/generate":
            concept = req_data.get("concept", "Luxury hotel suite view")
            style = req_data.get("style", "cinematic_luxury")
            pkg = generate_higgsfield_prompt(concept, style=style)
            self._send_json(pkg)

        elif parsed.path == "/api/elevenlabs/script":
            text = req_data.get("text", "Lüks servis asla tesadüf değildir.")
            profile = req_data.get("voice_profile", "adam_deep")
            script = generate_voice_script(text, voice_profile=profile)
            self._send_json(script)

        elif parsed.path == "/api/remotion/code":
            title = req_data.get("title", "FORBES 5-STAR")
            subtitle = req_data.get("subtitle", "SIFIR HATA STANDARTLARI")
            code = generate_remotion_component(title, subtitle)
            self._send_json({"code": code})

        elif parsed.path == "/api/forge/tool":
            t_name = req_data.get("name", "custom_tool")
            t_code = req_data.get("code", "# Custom Tool Code\n")
            sample_in = req_data.get("sample_input", "test")
            res = forge_tool(t_name, t_code, sample_in)
            self._send_json(res)

        elif parsed.path == "/api/forge/execute":
            t_name = req_data.get("name", "")
            arg = req_data.get("argument", "")
            res = execute_forged_tool(t_name, arg)
            self._send_json(res)

        elif parsed.path == "/api/research/url":
            target_url = req_data.get("url", "https://example.com")
            res = fetch_and_clean_markdown(target_url)
            self._send_json(res)

        elif parsed.path == "/api/viral/score":
            script_text = req_data.get("script", "")
            res = analyze_retention(script_text)
            self._send_json(res)

        elif parsed.path == "/api/speak":
            text = req_data.get("text", "")
            speak_async(text)
            self._send_json({"status": "SPEAKING"})

        elif parsed.path == "/api/volume":
            vol = req_data.get("volume", 50)
            res = set_volume(vol)
            self._send_json({"result": res})

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

class ThreadingJarvisServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def run_server():
    server = ThreadingJarvisServer((HOST, PORT), JarvisHandler)
    print("=" * 60)
    print(f"⚡ JARVIS OMNI-BRAIN SERVER ONLINE: http://{HOST}:{PORT}")
    print(f"[*] Sınırsız Nöral Ağ & Bütünleşmiş Araçlar: AKTİF")
    print(f"[*] GitHub, Higgsfield, ElevenLabs, Remotion, n8n: BAĞLI")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nJARVIS Server shutting down gracefully.")
        server.server_close()

if __name__ == "__main__":
    run_server()
