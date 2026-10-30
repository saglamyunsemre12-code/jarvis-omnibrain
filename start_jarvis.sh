#!/usr/bin/env bash
# JARVIS Omni-Brain Launch Script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8888

# Check if port is already running, if so kill old
PID=$(lsof -ti :$PORT)
if [ -n "$PID" ]; then
  kill -9 $PID 2>/dev/null
fi

echo "============================================================"
echo "⚡ BAŞLATILIYOR: JARVIS OMNI-BRAIN (NEXUS V1.0)"
echo "   Mixture-of-Agents Council: Codex + Claude + Gemini + NIM"
echo "   Yerel HUD Arayüzü: http://127.0.0.1:$PORT"
echo "============================================================"

python3 "$DIR/server.py"
