#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "filters" / "src"
DIST = ROOT / "filters" / "dist" / "temizweb-main.txt"
UPSTREAM = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/nsfw.txt"


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": "TemizWeb-Builder/1.0"})
    with urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_upstream(text: str) -> list[str]:
    rules: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("!", "[")):
            continue
        if line.startswith(("||", "@@")):
            rules.append(line)
    return rules


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Do not fetch HaGeZi")
    args = parser.parse_args()

    build_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    own_parts: list[str] = []
    for path in sorted(SRC.glob("*.txt")):
        text = path.read_text(encoding="utf-8").replace("BUILD_DATE", build_date)
        own_parts.append(text.rstrip())

    output = "\n\n".join(own_parts).rstrip() + "\n"
    if not args.offline:
        upstream = clean_upstream(fetch_text(UPSTREAM))
        output += (
            "\n! -----------------------------------------------------------------------------\n"
            "! Upstream: HaGeZi NSFW DNS Blocklist (GPL-3.0)\n"
            f"! Source: {UPSTREAM}\n"
            f"! Imported rules: {len(upstream)}\n"
            "! -----------------------------------------------------------------------------\n"
            + "\n".join(upstream)
            + "\n"
        )

    # Exact deduplication while preserving comments and order.
    seen: set[str] = set()
    final: list[str] = []
    for raw in output.splitlines():
        line = raw.rstrip()
        if line and not line.startswith("!"):
            if line in seen:
                continue
            seen.add(line)
        final.append(line)

    DIST.parent.mkdir(parents=True, exist_ok=True)
    DIST.write_text("\n".join(final).rstrip() + "\n", encoding="utf-8")
    print(f"Built {DIST}: {len(seen)} active rules")


if __name__ == "__main__":
    main()
