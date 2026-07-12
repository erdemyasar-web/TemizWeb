#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import argparse
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "filters" / "src"
DIST = ROOT / "filters" / "dist" / "temizweb-main.txt"

UPSTREAM_URLS = [
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/nsfw.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/nsfw.txt",
]


def fetch_text(url: str, attempts: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = Request(
                url,
                headers={"User-Agent": "TemizWeb-Builder/1.1"},
            )
            with urlopen(request, timeout=120) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(attempt * 3)
    raise RuntimeError(f"Could not download {url}: {last_error}")


def fetch_upstream() -> tuple[str, str]:
    errors: list[str] = []
    for url in UPSTREAM_URLS:
        try:
            return fetch_text(url), url
        except RuntimeError as exc:
            errors.append(str(exc))
    raise RuntimeError("\n".join(errors))


def clean_upstream(text: str) -> list[str]:
    rules: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("!", "[")):
            continue
        if line.startswith(("||", "@@")):
            rules.append(line)
    if len(rules) < 1000:
        raise RuntimeError(
            f"HaGeZi download appears incomplete: only {len(rules)} rules"
        )
    return rules


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Build only TemizWeb source rules without HaGeZi",
    )
    args = parser.parse_args()

    source_files = sorted(SRC.glob("*.txt"))
    if not source_files:
        raise SystemExit(f"No source files found in {SRC}")

    build_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts: list[str] = []
    for path in source_files:
        text = path.read_text(encoding="utf-8")
        parts.append(text.replace("BUILD_DATE", build_date).rstrip())

    output_lines = "\n\n".join(parts).splitlines()

    if not args.offline:
        upstream_text, source_url = fetch_upstream()
        upstream_rules = clean_upstream(upstream_text)
        output_lines.extend(
            [
                "",
                "! -----------------------------------------------------------------------------",
                "! Upstream: HaGeZi NSFW DNS Blocklist",
                f"! Source: {source_url}",
                "! License: GPL-3.0",
                f"! Imported rules: {len(upstream_rules)}",
                "! -----------------------------------------------------------------------------",
                *upstream_rules,
            ]
        )

    seen: set[str] = set()
    final: list[str] = []
    for raw in output_lines:
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
