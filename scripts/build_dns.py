#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen
import argparse
import ipaddress
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "dns" / "src"
DIST = ROOT / "dns" / "dist"

UPSTREAMS = {
    "hagezi_nsfw": "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/nsfw.txt",
    "blocklistproject_porn": "https://blocklistproject.github.io/Lists/porn-nl.txt",
}

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.I,
)

def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "TemizWeb-DNS-Builder/1.0"})
    with urlopen(req, timeout=120) as response:
        return response.read().decode("utf-8", errors="replace")

def normalize_domain(raw: str) -> str | None:
    line = raw.strip().lower()
    if not line or line.startswith(("#", "!", "[")):
        return None
    if " " in line:
        parts = line.split()
        if len(parts) >= 2:
            try:
                ipaddress.ip_address(parts[0])
                line = parts[1]
            except ValueError:
                return None
    line = line.removeprefix("||").removesuffix("^").rstrip(".")
    if line.startswith("*."):
        line = line[2:]
    if DOMAIN_RE.fullmatch(line):
        return line
    return None

def read_domains(path: Path) -> set[str]:
    result = set()
    if not path.exists():
        return result
    for raw in path.read_text(encoding="utf-8").splitlines():
        domain = normalize_domain(raw)
        if domain:
            result.add(domain)
    return result

def write_outputs(name: str, domains: set[str]) -> None:
    ordered = sorted(domains)
    (DIST / f"{name}-domains.txt").write_text(
        "# TemizWeb DNS domain list\n" + "\n".join(ordered) + "\n",
        encoding="utf-8",
    )
    (DIST / f"{name}-hosts.txt").write_text(
        "# TemizWeb DNS hosts list\n" +
        "\n".join(f"0.0.0.0 {d}" for d in ordered) + "\n",
        encoding="utf-8",
    )
    (DIST / f"{name}-adguard.txt").write_text(
        "! Title: TemizWeb DNS\n" +
        "\n".join(f"||{d}^" for d in ordered) + "\n",
        encoding="utf-8",
    )
    print(f"{name}: {len(ordered)} domains")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    DIST.mkdir(parents=True, exist_ok=True)
    allow = read_domains(SRC / "allowlist.txt")
    adult = read_domains(SRC / "10-turkish-adult-supplement.txt")

    if not args.offline:
        for label, url in UPSTREAMS.items():
            print(f"Fetching {label}")
            for raw in fetch(url).splitlines():
                domain = normalize_domain(raw)
                if domain:
                    adult.add(domain)

    vpn = read_domains(SRC / "20-vpn-proxy-domains.txt")
    bypass = read_domains(SRC / "30-public-dns-bypass-domains.txt")

    balanced = adult - allow
    strict = (adult | vpn | bypass) - allow
    adult_vpn = (adult | vpn) - allow

    write_outputs("temizweb-balanced", balanced)
    write_outputs("temizweb-adult-vpn", adult_vpn)
    write_outputs("temizweb-strict", strict)

if __name__ == "__main__":
    main()
