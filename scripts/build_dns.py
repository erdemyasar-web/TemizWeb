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
    "hagezi_nsfw": [
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/nsfw.txt",
    ],
    "blocklistproject_porn": [
        "https://blocklistproject.github.io/Lists/alt-version/porn-nl.txt",
        "https://raw.githubusercontent.com/blocklistproject/Lists/main/alt-version/porn-nl.txt",
    ],
}

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.I,
)


def fetch_first(label: str, urls: list[str]) -> str:
    errors: list[str] = []
    for url in urls:
        try:
            print(f"Fetching {label}: {url}")
            req = Request(url, headers={"User-Agent": "TemizWeb-DNS-Builder/1.1"})
            with urlopen(req, timeout=120) as response:
                text = response.read().decode("utf-8", errors="replace")
            if text.strip():
                return text
            errors.append(f"empty response: {url}")
        except Exception as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError(f"All sources failed for {label}: " + " | ".join(errors))


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

    return line if DOMAIN_RE.fullmatch(line) else None


def read_domains(path: Path) -> set[str]:
    result: set[str] = set()
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
        "# TemizWeb DNS hosts list\n"
        + "\n".join(f"0.0.0.0 {domain}" for domain in ordered)
        + "\n",
        encoding="utf-8",
    )
    (DIST / f"{name}-adguard.txt").write_text(
        "! Title: TemizWeb DNS\n"
        + "\n".join(f"||{domain}^" for domain in ordered)
        + "\n",
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
        successful_sources = 0
        for label, urls in UPSTREAMS.items():
            try:
                text = fetch_first(label, urls)
            except RuntimeError as exc:
                print(f"WARNING: {exc}")
                continue

            imported = 0
            for raw in text.splitlines():
                domain = normalize_domain(raw)
                if domain:
                    adult.add(domain)
                    imported += 1
            print(f"Imported {imported} entries from {label}")
            successful_sources += 1

        if successful_sources == 0:
            raise SystemExit("No upstream adult list could be downloaded.")

    vpn = read_domains(SRC / "20-vpn-proxy-domains.txt")
    bypass = read_domains(SRC / "30-public-dns-bypass-domains.txt")

    balanced = adult - allow
    adult_vpn = (adult | vpn) - allow
    strict = (adult | vpn | bypass) - allow

    if not args.offline and len(balanced) < 1000:
        raise SystemExit(
            f"Adult list unexpectedly small ({len(balanced)} domains); refusing to publish."
        )

    write_outputs("temizweb-balanced", balanced)
    write_outputs("temizweb-adult-vpn", adult_vpn)
    write_outputs("temizweb-strict", strict)


if __name__ == "__main__":
    main()
