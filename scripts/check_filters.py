#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "filters" / "dist" / "temizweb-main.txt"
text = TARGET.read_text(encoding="utf-8")
errors = []
for required in ("! Title:", "! License:", "! Version:", "! Expires:"):
    if required not in text:
        errors.append(f"Missing header: {required}")

active = []
for n, raw in enumerate(text.splitlines(), 1):
    line = raw.strip()
    if not line or line.startswith(("!", "[")):
        continue
    active.append(line)
    if "##" not in line and not line.startswith(("||", "@@", "/")):
        errors.append(f"Unknown syntax at line {n}: {line}")

if len(active) != len(set(active)):
    errors.append("Duplicate active rules remain")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"OK: {len(active)} active rules")
