#!/usr/bin/env python3
"""Automated runbook scaffolder conforming to CONTRIBUTING.MD standards."""

import os
import re
import sys
from pathlib import Path

CATEGORY_KEYWORDS = {
    "server-management": ["ssh", "server", "tailscale", "luks", "wol", "nfs", "rclone", "irmc", "firewall", "ufw"],
    "software-management": ["docker", "flatpak", "appimage", "java", "compose", "container", "navidrome", "linkding", "homer"],
    "backup-operations": ["backup", "restore", "borg", "vorta", "archive", "snapshot", "rclone"],
    "system-optimizations": ["zram", "swappiness", "pipewire", "usb", "vfs", "performance", "optimization"],
    "system-administration": ["systemd", "service", "monitoring", "journal", "cron", "admin"],
    "hardware-diagnostics": ["post", "nvidia", "dkms", "gpu", "kernel", "hardware", "bios", "fault"],
    "huawei-configs": ["huawei", "battery", "matebook"],
    "ios-management": ["ios", "iphone", "sidestore", "ipa"],
}


def detect_category(summary: str) -> str:
    lowered = summary.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return category
    return "system-administration"


def next_index(category_dir: Path) -> str:
    indices = []
    for entry in category_dir.glob("*.md"):
        match = re.match(r"^(\d{2})_", entry.name)
        if match:
            indices.append(int(match.group(1)))
    return f"{(max(indices) + 1) if indices else 1:02d}"


def build_slug(summary: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", summary.strip()).strip("_").upper()
    return cleaned[:48] or "NEW_RUNBOOK"


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: ./generate_guide.py "<Brief Problem Summary>"', file=sys.stderr)
        return 1

    summary = " ".join(sys.argv[1:]).strip()
    repo_root = Path(__file__).resolve().parent
    category = detect_category(summary)
    category_dir = repo_root / category
    category_dir.mkdir(parents=True, exist_ok=True)

    idx = next_index(category_dir)
    slug = build_slug(summary)
    filename = f"{idx}_{slug}.md"
    target = category_dir / filename

    ticks = "```"
    content = (
        f"# {idx}: {summary}\n\n"
        f"Operational runbook for {summary.lower()} on `<client-host>` / `<server-host>`.\n\n"
        f"---\n\n"
        f"## 1. Prerequisites & Preparation\n\n"
        f"1. Verify system state on `<client-host>`:\n"
        f"   {ticks}bash\n"
        f"   # Add prerequisite commands\n"
        f"   {ticks}\n\n"
        f"---\n\n"
        f"## 2. Configuration\n\n"
        f"1. Apply the configuration:\n"
        f"   {ticks}bash\n"
        f"   # Add configuration commands\n"
        f"   {ticks}\n\n"
        f"---\n\n"
        f"## 3. Diagnostics & Validation\n\n"
        f"1. Verify the expected behavior:\n"
        f"   {ticks}bash\n"
        f"   # Add validation command\n"
        f"   {ticks}\n"
        f"   Expected Output:\n"
        f"   {ticks}text\n"
        f"   # Add literal expected output\n"
        f"   {ticks}\n\n"
        f"---\n\n"
        f"## 4. Best Practices (Do's and Don'ts)\n\n"
        f"* **Do** verify changes before rebooting or disconnecting.\n"
        f"* **Don't** commit host-specific IPs, usernames, or credentials.\n"
    )

    target.write_text(content, encoding="utf-8")
    print(f"Created {target.relative_to(repo_root)}")
    print(f"Remember to register it in README.md under {category}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
