#!/usr/bin/env python3
"""
JARVIS System Engine — Direct macOS Control via AppleScript & CLI
Manages battery, volume, Safari tabs, speech, and OS diagnostics.
"""

import subprocess
import json

def get_battery_status():
    try:
        out = subprocess.check_output(["pmset", "-g", "batt"], text=True)
        return out.strip()
    except Exception as e:
        return f"Battery query error: {e}"

def get_system_metrics():
    battery = get_battery_status()
    try:
        uptime = subprocess.check_output(["uptime"], text=True).strip()
    except Exception:
        uptime = "N/A"
    return {
        "battery": battery,
        "uptime": uptime,
        "os": "macOS Sonoma / Darwin"
    }

def get_safari_tabs():
    scpt = '''
    tell application "Safari"
        set tabList to {}
        repeat with w in windows
            repeat with t in tabs of w
                set end of tabList to (name of t & " -> " & URL of t)
            end repeat
        end repeat
        return tabList
    end tell
    '''
    try:
        out = subprocess.check_output(["osascript", "-e", scpt], text=True)
        return [line.strip() for line in out.split(",") if line.strip()]
    except Exception as e:
        return [f"Safari not accessible: {e}"]

def set_volume(level):
    try:
        subprocess.run(["osascript", "-e", f"set volume output volume {int(level)}"], check=True)
        return f"Volume set to {level}%"
    except Exception as e:
        return f"Volume error: {e}"

def open_url_in_safari(url):
    try:
        subprocess.run(["open", url], check=True)
        return f"Opened {url} in default browser."
    except Exception as e:
        return f"Open error: {e}"

def execute_shell(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=15)
        return out.strip()
    except subprocess.CalledProcessError as e:
        return f"Exit {e.returncode}: {e.output}"
    except Exception as e:
        return f"Execution error: {e}"

if __name__ == "__main__":
    print("Metrics:", get_system_metrics())
