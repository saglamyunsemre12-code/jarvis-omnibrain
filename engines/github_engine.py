#!/usr/bin/env python3
"""
JARVIS GitHub Engine — Seamless GitHub CLI & Repository Management
Directly interacts with account: saglamyunsemre12-code
"""

import subprocess
import json

def get_github_status():
    try:
        auth_out = subprocess.check_output(["gh", "auth", "status"], stderr=subprocess.STDOUT, text=True)
        user_out = subprocess.check_output(["gh", "api", "user"], text=True)
        user_data = json.loads(user_out)
        return {
            "status": "AUTHENTICATED",
            "username": user_data.get("login"),
            "name": user_data.get("name"),
            "public_repos": user_data.get("public_repos"),
            "html_url": user_data.get("html_url")
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def list_user_repos(limit=10):
    try:
        out = subprocess.check_output(["gh", "repo", "list", "--limit", str(limit), "--json", "name,description,url,updatedAt,isPrivate"], text=True)
        return json.loads(out)
    except Exception as e:
        return [{"name": "Error", "description": str(e)}]

def create_repo(name, description="", private=True):
    try:
        visibility = "--private" if private else "--public"
        cmd = ["gh", "repo", "create", name, visibility, "--description", description, "--confirm"]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return {"status": "SUCCESS", "output": out.strip()}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    print(get_github_status())
    print("Repos:", list_user_repos(5))
