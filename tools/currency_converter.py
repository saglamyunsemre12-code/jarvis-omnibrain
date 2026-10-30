#!/usr/bin/env python3
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
