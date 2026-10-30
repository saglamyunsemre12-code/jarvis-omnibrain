#!/usr/bin/env python3
"""
JARVIS Skills & Plugins Indexer — Unified Meta-Catalog
Indexes all Codex skills, Antigravity plugins, MCP tools, and external services.
"""

import os
import json

def get_all_indexed_skills():
    codex_dir = os.path.expanduser("~/.codex/skills")
    codex_skills = []
    if os.path.exists(codex_dir):
        for name in sorted(os.listdir(codex_dir)):
            if not name.startswith("."):
                skill_path = os.path.join(codex_dir, name, "SKILL.md")
                desc = "Custom Codex & YouTube / Remotion Automation Skill"
                if os.path.exists(skill_path):
                    with open(skill_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            if "description:" in line.lower():
                                desc = line.split(":", 1)[1].strip().strip('"\'')
                                break
                codex_skills.append({
                    "id": name,
                    "name": name,
                    "source": "Codex / Personal",
                    "description": desc
                })

    antigravity_skills = [
        {"id": "modern-web-guidance", "name": "Modern Web Guidance", "source": "Antigravity", "description": "Cutting-edge HTML5/CSS/JS, OKLCH, and responsive Impeccable web guidelines."},
        {"id": "omniroute", "name": "OmniRoute AI Gateway", "source": "Antigravity", "description": "Auto-cascading multi-LLM fallback (Claude -> NVIDIA NIM -> Gemini)."},
        {"id": "headroom", "name": "Headroom Context Compressor", "source": "Antigravity", "description": "85-90% semantic compression of heavy logs and outputs."},
        {"id": "task-observer", "name": "Task Observer Memory", "source": "Antigravity", "description": "Persistent preference learning and self-correcting rules."},
        {"id": "claude-mem", "name": "Claude-Mem Cross-Session", "source": "Antigravity", "description": "User profile and long-term memory persistence across resets."},
        {"id": "google-antigravity-sdk", "name": "Antigravity Agent SDK", "source": "Antigravity", "description": "Autonomous multi-agent orchestration and design patterns."},
        {"id": "chrome-extensions", "name": "Chrome Extensions Manifest V3", "source": "Antigravity", "description": "Browser extension development and publishing."},
        {"id": "generative_ui", "name": "Generative UI Widgets", "source": "Antigravity", "description": "Rich interactive HTML widgets inline in the console."}
    ]

    mcp_connectors = [
        {"id": "mcp-github", "name": "GitHub Connector", "source": "MCP", "description": "Direct access to repositories, commits, and PRs via GitHub API."},
        {"id": "mcp-cloudrun", "name": "Google Cloud Run", "source": "MCP", "description": "Serverless container deployment and live service management."},
        {"id": "mcp-gemini-docs", "name": "Gemini API Official Docs", "source": "MCP", "description": "Up-to-date Gemini SDK and model documentation lookup."}
    ]

    external_ai_nodes = [
        {"id": "node-nvda", "name": "NVIDIA NIM", "status": "ONLINE", "type": "LLM Inference", "models": ["Llama-3.2-11B", "Nemotron-70B"]},
        {"id": "node-codex", "name": "OpenAI Codex", "status": "ONLINE", "type": "Code Architecture", "cli": "codex exec"},
        {"id": "node-claude", "name": "Anthropic Claude", "status": "ONLINE", "type": "Strategic Reasoning", "access": "OmniRoute + Browser"},
        {"id": "node-gemini", "name": "Google Gemini", "status": "ONLINE", "type": "Research & Grounding", "access": "Web + API"},
        {"id": "node-higgsfield", "name": "Higgsfield AI", "status": "ONLINE", "type": "Cinematic Video Suite", "access": "Safari Tab 5"},
        {"id": "node-elevenlabs", "name": "ElevenLabs", "status": "ONLINE", "type": "Voice & Speech Synthesis", "access": "Safari Tab 8"},
        {"id": "node-n8n", "name": "n8n Cloud Studio", "status": "ONLINE", "type": "Workflow Automation", "access": "emre-ai-studio.app.n8n.cloud"},
        {"id": "node-github", "name": "GitHub CLI & Repo Hub", "status": "ONLINE", "type": "Version Control", "user": "saglamyunsemre12-code"},
        {"id": "node-sheets", "name": "Google E-Tablolar", "status": "ONLINE", "type": "Content Calendar", "doc": "Instagram İçerik Takvimi"}
    ]

    return {
        "total_skills_count": len(codex_skills) + len(antigravity_skills) + len(mcp_connectors),
        "codex_skills": codex_skills,
        "antigravity_skills": antigravity_skills,
        "mcp_connectors": mcp_connectors,
        "external_nodes": external_ai_nodes
    }

if __name__ == "__main__":
    data = get_all_indexed_skills()
    print(f"Total skills indexed: {data['total_skills_count']}")
    print(f"Total AI nodes: {len(data['external_nodes'])}")
