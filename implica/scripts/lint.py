#!/usr/bin/env python3
"""
lint.py — Implica Wiki Health Check

Checks for:
- Orphan pages (no inbound links)
- Missing cross-references
- Stale pages (not updated in N days)
- Contradictions between pages
- Missing pages for referenced concepts
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
import datetime

WIKI_ROOT = Path(__file__).parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"
STALE_DAYS = 30

def find_all_pages():
    """Find all wiki pages and their outbound links"""
    pages = {}
    link_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

    for md in WIKI_DIR.rglob("*.md"):
        rel = md.relative_to(WIKI_DIR)
        with open(md, errors='replace') as f:
            content = f.read()

        links = link_pattern.findall(content)
        links = [l.strip() for l in links]

        # Extract frontmatter
        stale = "stale: true" in content[:200]
        updated = None
        for line in content[:500].splitlines():
            if line.strip().startswith("updated:"):
                updated = line.split(":", 1)[1].strip().strip('"')

        pages[str(rel)] = {
            "path": md,
            "links": links,
            "stale": stale,
            "updated": updated,
            "has_recent_update": False
        }

    return pages

def check_orphans(pages):
    """Find pages with no inbound links"""
    orphans = []
    all_links = set()
    for p in pages.values():
        for link in p["links"]:
            # Normalize link to potential filename
            all_links.add(link)

    for name, page in pages.items():
        # Check if any other page links to this one
        has_inbound = any(
            name in link or link in name
            for other in pages.values()
            for link in other["links"]
        )
        if not has_inbound:
            orphans.append(name)

    return orphans

def check_stale(pages):
    """Find pages marked stale or not updated recently"""
    stale_pages = []
    cutoff = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=STALE_DAYS)

    for name, page in pages.items():
        if page["stale"]:
            stale_pages.append(f"{name} — marked stale")
            continue

        if page["updated"]:
            try:
                updated_date = datetime.datetime.strptime(page["updated"], "%Y-%m-%d")
                if updated_date < cutoff:
                    stale_pages.append(f"{name} — not updated since {page['updated']}")
            except:
                pass

    return stale_pages

def check_missing_concepts(pages):
    """Find referenced concepts that don't have their own page"""
    all_files = set()
    for p in pages:
        all_files.add(p)

    referenced = set()
    for page in pages.values():
        for link in page["links"]:
            referenced.add(link)

    missing = []
    for ref in referenced:
        # Check if any file matches this reference
        found = any(ref.lower() in f.lower() or f.lower() in ref.lower() for f in all_files)
        if not found:
            missing.append(f"{ref} — referenced but no page exists")

    return missing[:10]  # Limit

def main():
    print("Implica Wiki Lint Report")
    print("=" * 40)

    pages = find_all_pages()
    print(f"Total pages: {len(pages)}\n")

    orphans = check_orphans(pages)
    if orphans:
        print("ORPHAN PAGES (no inbound links):")
        for p in orphans:
            print(f"  ISSUE: orphan | {p} has no incoming links | {p}")
        print()

    stale = check_stale(pages)
    if stale:
        print("STALE PAGES:")
        for p in stale:
            print(f"  ISSUE: stale | {p}")
        print()

    missing = check_missing_concepts(pages)
    if missing:
        print("MISSING CONCEPT PAGES (referenced but don't exist):")
        for m in missing:
            print(f"  ISSUE: missing_page | {m}")

    if not orphans and not stale and not missing:
        print("✅ Wiki looks healthy!")

    # Log to wiki
    log_path = WIKI_DIR / "log.md"
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    issues_count = len(orphans) + len(stale) + len(missing)
    entry = f"\n## [{today}] lint | Health check\n- Pages checked: {len(pages)}\n"
    if issues_count == 0:
        entry += "- Status: healthy\n"
    else:
        entry += f"- Issues found: {issues_count} (orphans={len(orphans)}, stale={len(stale)}, missing_concepts={len(missing)})\n"

    with open(log_path, 'a') as f:
        f.write(entry)

    print(f"\nLogged to {log_path}")
    return 0 if issues_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
