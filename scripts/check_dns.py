#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dns" / "dist"
DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9-]+$", re.I)

errors = []
for path in sorted(DIST.glob("*-domains.txt")):
    domains = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        domains.append(line)
        if not DOMAIN_RE.fullmatch(line):
            errors.append(f"{path.name}:{n}: invalid domain: {line}")
    if len(domains) != len(set(domains)):
        errors.append(f"{path.name}: duplicates remain")
    if domains != sorted(domains):
        errors.append(f"{path.name}: not sorted")
    print(f"{path.name}: {len(domains)} domains")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("DNS outputs OK")
