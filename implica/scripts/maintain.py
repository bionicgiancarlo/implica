#!/usr/bin/env python3
"""
maintain.py — Implica Wiki Maintenance

Updates:
- wiki/index.md (regenerate from all pages)
- Stale flags
- Cross-reference consistency
"""

import sys
from pathlib import Path
import re
import datetime

WIKI_ROOT = Path(__file__).parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"
INDEX = WIKI_DIR / "index.md"
LOG = WIKI_DIR / "log.md"

def regen_index():
    """Regenerate wiki/index.md from all existing pages"""
    pages_by_type = {
        "entities": [],
        "topics": [],
        "syntheses": [],
        "comparisons": [],
        "source-summaries": [],
    }

    link_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

    for md in WIKI_DIR.rglob("*.md"):
        if md.name == "index.md" or md.name == "log.md":
            continue

        rel = str(md.relative_to(WIKI_DIR))
        with open(md, errors='replace') as f:
            content = f.read()

        # Extract frontmatter
        title = rel
        ptype = "unknown"
        sources_count = 0
        updated = "unknown"

        in_fm = False
        for line in content.splitlines():
            if line.strip() == "---":
                in_fm = not in_fm
                continue
            if in_fm:
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("type:"):
                    ptype = line.split(":", 1)[1].strip()
                elif line.startswith("updated:"):
                    updated = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("sources:"):
                    # Count items in list
                    sources_count = line.count("[") + line.count("]")
                    if sources_count > 0:
                        sources_count = 1  # Simplified

        # Count inbound links from other pages
        inbound = 0
        for other in WIKI_DIR.rglob("*.md"):
            if other == md or other.name in ["index.md", "log.md"]:
                continue
            with open(other, errors='replace') as f:
                other_content = f.read()
            if title in other_content or rel in other_content:
                inbound += 1

        # Determine category
        category = None
        for cat in pages_by_type:
            if rel.startswith(cat):
                category = cat
                break

        if category:
            pages_by_type[category].append({
                "title": title,
                "rel": rel,
                "ptype": ptype,
                "updated": updated,
                "sources": sources_count,
                "inbound": inbound
            })

    # Build index content
    lines = [
        "---",
        "title: Implica Wiki Index",
        "---",
        "",
        "# Index",
        "",
        f"_Auto-generated {datetime.datetime.utcnow().strftime('%Y-%m-%d')}_",
        ""
    ]

    section_titles = {
        "entities": "## Entities",
        "topics": "## Topics",
        "syntheses": "## Syntheses",
        "comparisons": "## Comparisons",
        "source-summaries": "## Source Summaries",
    }

    for cat, title in section_titles.items():
        lines.append(title)
        pages = pages_by_type[cat]
        if not pages:
            lines.append("_(none yet)_")
        else:
            if cat == "source-summaries":
                lines.append("| Page | Source | Date |")
                lines.append("|------|--------|------|")
                for p in sorted(pages, key=lambda x: x["updated"], reverse=True):
                    pg_link = f"[[{p['rel']}|{p['title']}]]"
                    lines.append(f"| {pg_link} | {p['ptype']} | {p['updated']} |")
            else:
                lines.append("| Page | Summary | Sources | Inbound | Updated |")
                lines.append("|------|---------|---------|---------|--------|")
                for p in sorted(pages, key=lambda x: x["title"]):
                    pg_link = f"[[{p['rel']}|{p['title']}]]"
                    src_count = p["sources"] or "—"
                    lines.append(f"| {pg_link} | _(expand)_ | {src_count} | {p['inbound']} | {p['updated']} |")
        lines.append("")

    INDEX.write_text("\n".join(lines))
    print(f"Regenerated index with {sum(len(v) for v in pages_by_type.values())} pages")

def main():
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

    regen_index()

    # Append to log
    entry = f"\n## [{today}] maintain | Index regenerated\n"
    with open(LOG, 'a') as f:
        f.write(entry)

    print("Maintenance complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
