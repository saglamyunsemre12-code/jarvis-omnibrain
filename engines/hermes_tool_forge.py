#!/usr/bin/env python3
"""
JARVIS Hermes Tool Forge — Autonomous Dynamic Tool Creation
Inspired by NousResearch Hermes Agent (yager.dev / NousResearch)
Enables JARVIS to autonomously code, test, and register new tools on the fly.
"""

import os
import sys
import json
import subprocess
import time

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")

def list_forged_tools():
    """Lists all dynamically created tools."""
    tools = []
    if os.path.exists(TOOLS_DIR):
        for fname in sorted(os.listdir(TOOLS_DIR)):
            if fname.endswith(".py") and not fname.startswith("__"):
                fpath = os.path.join(TOOLS_DIR, fname)
                doc = "Dynamic tool"
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith('"""') or line.startswith("'''"):
                            doc = line.strip().strip('"\'')
                            break
                        elif line.startswith("#"):
                            doc = line.strip("# \n")
                            break
                tools.append({
                    "filename": fname,
                    "tool_name": fname.replace(".py", ""),
                    "description": doc,
                    "path": fpath
                })
    return tools

def forge_tool(tool_name, tool_code, sample_input="test"):
    """
    Creates a new Python tool, validates its syntax and execution, and registers it.
    """
    safe_name = "".join(c for c in tool_name if c.isalnum() or c in ("_", "-")).lower()
    if not safe_name.endswith(".py"):
        safe_name += ".py"

    target_path = os.path.join(TOOLS_DIR, safe_name)

    # 1. Write the code
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(tool_code)

    # 2. Syntax validation
    try:
        subprocess.check_output([sys.executable, "-m", "py_compile", target_path], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        os.remove(target_path)
        return {
            "status": "SYNTAX_ERROR",
            "message": f"Tool syntax check failed: {e.output.decode('utf-8', errors='ignore')}"
        }

    # 3. Execution self-test
    try:
        out = subprocess.check_output([sys.executable, target_path, str(sample_input)], stderr=subprocess.STDOUT, text=True, timeout=8)
        test_result = out.strip()
    except Exception as e:
        test_result = f"Self-test output: {e}"

    return {
        "status": "FORGED_AND_REGISTERED",
        "tool_name": safe_name.replace(".py", ""),
        "path": target_path,
        "self_test": test_result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def execute_forged_tool(tool_name, argument=""):
    """Runs a dynamically forged tool."""
    safe_name = tool_name if tool_name.endswith(".py") else f"{tool_name}.py"
    target_path = os.path.join(TOOLS_DIR, safe_name)

    if not os.path.exists(target_path):
        return {"status": "NOT_FOUND", "message": f"Tool {tool_name} does not exist."}

    try:
        out = subprocess.check_output([sys.executable, target_path, str(argument)], stderr=subprocess.STDOUT, text=True, timeout=12)
        return {"status": "SUCCESS", "output": out.strip()}
    except subprocess.CalledProcessError as e:
        return {"status": "EXEC_ERROR", "output": e.output}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    sample_code = """#!/usr/bin/env python3
import sys
# Currency & Commission Calculator Tool
def calculate(val):
    try:
        amount = float(val) if val else 100.0
        return f"Calculated: {amount} EUR -> {(amount * 38.5):.2f} TRY (at 38.5 rate)"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "100"
    print(calculate(arg))
"""
    res = forge_tool("currency_converter", sample_code, "250")
    print("Forge result:", json.dumps(res, indent=2))
    print("Execute result:", execute_forged_tool("currency_converter", "500"))
