#!/usr/bin/env python3
"""
ingest.py — Implica Wiki Ingest CLI

Usage:
  ./scripts/ingest.py <source> [--type paper|article|note|url] [--name <slug>]

Examples:
  ./scripts/ingest.py raw/2026-04-05-my-paper.pdf --type paper
  ./scripts/ingest.py https://example.com/article --type url
  ./scripts/ingest.py raw/notes.md --type note
"""

import sys
import os
import re
import subprocess
import argparse
import datetime
from pathlib import Path

# ─── Config ─────────────────────────────────────────────────────────────────

WIKI_ROOT = Path(__file__).parent.parent
RAW_DIR = WIKI_ROOT / "raw"
WIKI_DIR = WIKI_ROOT / "wiki"
SOURCES_INDEX = RAW_DIR / "sources.md"
INDEX = WIKI_DIR / "index.md"
LOG = WIKI_DIR / "log.md"

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
if not MINIMAX_API_KEY:
    # Try to read from openclaw config
    import json
    config_path = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
    if config_path.exists():
        with open(config_path) as f:
            data = json.load(f)
            profiles = data.get("profiles", {})
            for v in profiles.values():
                if v.get("type") == "api_key":
                    MINIMAX_API_KEY = v.get("key", "")
                    break

# ─── Utils ────────────────────────────────────────────────────────────────────

def log(msg):
    print(f"[ingest] {msg}", file=sys.stderr)

def run(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if result.returncode != 0 and capture:
        log(f"warn: {cmd} returned {result.returncode}")
    return result.stdout if capture else ""

def date_now():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

def slugify(text):
    """Make a short slug from text"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:60]

def extract_text_from_pdf(path):
    """Extract text from PDF using Python's built-ins"""
    # Try strings command as fallback
    try:
        result = subprocess.run(
            ["strings", path],
            capture_output=True, text=True, timeout=30
        )
        # Filter for readable text chunks
        lines = [l.strip() for l in result.stdout.splitlines() if len(l.strip()) > 20]
        return "\n".join(lines[:500])  # Limit to first 500 substantial lines
    except Exception as e:
        return f"[Could not extract PDF text: {e}]"

def extract_text_from_markdown(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def extract_text(source):
    """Extract text from any supported file type"""
    source = Path(source)
    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    ext = source.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(source)
    elif ext in [".md", ".txt", ".text"]:
        return extract_text_from_markdown(source)
    else:
        # Try to read as text anyway
        return extract_text_from_markdown(source)

# ─── LLM Extraction ───────────────────────────────────────────────────────────

def call_llm(text, prompt_template):
    """Call Minimax API for extraction"""
    if not MINIMAX_API_KEY:
        return None, "No API key available"

    import urllib.request
    import json

    full_prompt = f"""{prompt_template}

TEXT TO ANALYZE:
{text[:8000]}  # Limit input size

Respond in JSON with the fields specified above."""

    payload = {
        "model": "MiniMax-M2.7",
        "messages": [{"role": "user", "content": full_prompt}],
        "max_tokens": 2048,
        "temperature": 0.3
    }

    try:
        req = urllib.request.Request(
            "https://api.minimax.io/anthropic/v1/messages",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {MINIMAX_API_KEY}",
                "Content-Type": "application/json",
                "Anthropic-Version": "2023-06-01"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data.get("content", [{}])[0].get("text", ""), None
    except Exception as e:
        return None, str(e)

# ─── Frontmatter building ─────────────────────────────────────────────────────

def build_frontmatter(title, page_type, tags, sources, date):
    tags_str = "[" + ", ".join(f'"{t}"' for t in tags) + "]" if tags else "[]"
    sources_str = "[" + ", ".join(f'"{s}"' for s in sources) + "]" if sources else "[]"
    return f'''---
title: "{title}"
type: {page_type}
tags: {tags_str}
sources: {sources_str}
created: {date}
updated: {date}
stale: false
---

'''

# ─── Ingest steps ─────────────────────────────────────────────────────────────

def ingest_file(source_path, source_type, name_override=None):
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    today = date_now()
    slug = name_override or slugify(source.stem)
    date_str = today  # TODO: extract date from PDF metadata if available

    log(f"Ingesting {source} (type={source_type}, slug={slug})")

    # Extract text
    text = extract_text(source)
    log(f"Extracted ~{len(text)} chars")

    # Build extraction prompt
    if source_type == "paper":
        extraction_prompt = """You are analyzing a research paper. Extract key information and return ONLY valid JSON with this structure (no markdown, no explanation):

{
  "title": "Paper title",
  "authors": ["Author 1", "Author 2"],
  "year": "YYYY",
  "tags": ["tag1", "tag2", "tag3"],
  "domain": "broad domain like 'machine learning' or 'neuroscience'",
  "key_claims": ["claim 1", "claim 2", "claim 3"],
  "methods": "brief description of methods used",
  "findings": ["finding 1", "finding 2"],
  "limitations": ["limitation 1"],
  "related_concepts": ["concept 1", "concept 2"],
  "summary": "2-3 paragraph summary of the paper",
  "entity_pages_to_update": ["Entity-Name", "Entity-Name"],
  "topic_pages_to_update": ["Topic-Name", "Topic-Name"]
}

Return only the JSON."""
    elif source_type == "article":
        extraction_prompt = """You are analyzing an article. Extract key information and return ONLY valid JSON with this structure (no markdown, no explanation):

{
  "title": "Article title",
  "source": "publication name or URL",
  "date": "YYYY-MM-DD or null",
  "tags": ["tag1", "tag2"],
  "key_points": ["point 1", "point 2", "point 3"],
  "summary": "2-3 paragraph summary",
  "related_concepts": ["concept 1", "concept 2"],
  "entity_pages_to_update": ["Entity-Name"],
  "topic_pages_to_update": ["Topic-Name"]
}

Return only the JSON."""
    else:
        extraction_prompt = """You are analyzing notes. Extract key information and return ONLY valid JSON:

{
  "title": "Title or topic of these notes",
  "tags": ["tag1", "tag2"],
  "key_points": ["point 1", "point 2"],
  "summary": "2-3 paragraph summary",
  "related_concepts": ["concept 1", "concept 2"],
  "entity_pages_to_update": [],
  "topic_pages_to_update": []
}

Return only the JSON."""

    extracted_str, err = call_llm(text, extraction_prompt)

    if err or not extracted_str:
        log(f"LLM extraction failed: {err} — using manual parsing")
        extracted = {
            "title": slug.replace("-", " ").title(),
            "tags": [source_type],
            "key_points": ["See source summary"],
            "summary": f"Source: {source.name}",
            "related_concepts": [],
            "entity_pages_to_update": [],
            "topic_pages_to_update": [],
        }
    else:
        try:
            import json as json_mod
            # Strip markdown code blocks if present
            if "```json" in extracted_str:
                extracted_str = extracted_str.split("```json")[1].split("```")[0]
            elif "```" in extracted_str:
                extracted_str = extracted_str.split("```")[1].split("```")[0]
            extracted = json_mod.loads(extracted_str.strip())
        except Exception as e:
            log(f"JSON parse error: {e}")
            extracted = {
                "title": slug.replace("-", " ").title(),
                "tags": [source_type],
                "key_points": ["See source summary"],
                "summary": extracted_str[:500] if extracted_str else f"Source: {source.name}",
                "related_concepts": [],
                "entity_pages_to_update": [],
                "topic_pages_to_update": [],
            }

    title = extracted.get("title", slug)
    tags = extracted.get("tags", [source_type])
    summary = extracted.get("summary", "")
    related = extracted.get("related_concepts", [])
    entities = extracted.get("entity_pages_to_update", [])
    topics = extracted.get("topic_pages_to_update", [])

    # Create source summary page
    summary_filename = f"{date_str}-{slug}.md"
    summary_path = WIKI_DIR / "source-summaries" / summary_filename
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    summary_content = build_frontmatter(title, "source-summary", tags, [f"raw/{source.name}"], date_str)
    summary_content += f"# {title}\n\n"
    summary_content += f"**Type:** {source_type}\n\n"
    summary_content += f"**Source:** `{source.absolute()}`\n\n"
    summary_content += "## Summary\n\n"
    summary_content += summary + "\n\n"
    if extracted.get("key_points"):
        summary_content += "## Key Points\n\n"
        for pt in extracted["key_points"]:
            summary_content += f"- {pt}\n"
        summary_content += "\n"
    if extracted.get("authors"):
        summary_content += f"**Authors:** {', '.join(extracted['authors'])}\n\n"
    if extracted.get("methods"):
        summary_content += f"## Methods\n\n{extracted['methods']}\n\n"
    if related:
        summary_content += "## Related Concepts\n\n"
        for c in related:
            summary_content += f"- {c}\n"
        summary_content += "\n"

    with open(summary_path, 'w') as f:
        f.write(summary_content)
    log(f"Created source summary: {summary_path.name}")

    # Update raw/sources.md
    _update_sources_index(source.name, source_type, title, date_str, slug)

    # Update wiki/index.md
    _update_index_add("source-summaries", summary_filename, title, summary[:80], source_type, 1)

    # Update entities
    for entity in entities:
        _upsert_entity(entity, f"Updated by {title}", today)

    # Update topics
    for topic in topics:
        _upsert_topic(topic, f"Updated by {title}", today)

    # Append to log
    _append_log(today, "ingest", title, [f"Created [[{summary_filename}]]"] + [f"Updated [[{e}]]" for e in entities])

    log("Ingest complete!")

def _update_sources_index(filename, ftype, title, date_str, slug):
    new_line = f"| [{filename}](raw/{filename}) | {ftype} | {date_str} | [[wiki/source-summaries/{date_str}-{slug}|source summary]] |\n"
    if SOURCES_INDEX.exists():
        with open(SOURCES_INDEX) as f:
            content = f.read()
    else:
        content = "# Raw Sources\n\n| Source | Type | Date | Slug |\n|--------|------|------|------|\n"
    # Remove placeholder if present
    content = content.replace("| _(none yet)_ | — | — | — |\n", "")
    # Add new line before closing
    if "| _(none yet)_ |" in content:
        content = content.replace("| _(none yet)_ |", f"| [{filename}](raw/{filename}) | {ftype} | {date_str} |")
    elif new_line.strip() not in content:
        content += new_line
    with open(SOURCES_INDEX, 'w') as f:
        f.write(content)

def _update_index_add(page_type, filename, title, summary, ptype, source_count):
    if not INDEX.exists():
        return
    with open(INDEX) as f:
        content = f.read()

    # Find the right section and add
    section_headers = {
        "source-summaries": "## Source Summaries",
        "entities": "## Entities",
        "topics": "## Topics",
        "syntheses": "## Syntheses",
        "comparisons": "## Comparisons",
    }
    section = section_headers.get(page_type, "## Source Summaries")

    new_line = f"| [[wiki/{page_type}/{filename}|{title}]] | {summary} | {ptype} | {source_count} |\n"

    if new_line.strip() in content:
        return  # Already present

    # Simple append before _Last maintained_ line
    marker = "_Last maintained:"
    if marker in content:
        content = content.replace(marker, new_line + marker)
    else:
        content += new_line

    with open(INDEX, 'w') as f:
        f.write(content)

def _upsert_entity(name, reason, date):
    """Create or update an entity page"""
    filename = name + ".md"
    path = WIKI_DIR / "entities" / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        # Append update note
        with open(path) as f:
            content = f.read()
        # Remove stale flag if present
        content = content.replace("stale: true", "stale: false")
        # Update date
        content = content.replace("updated: YYYY-MM-DD", f"updated: {date}")
        # Add note about recent update
        if "## Recent Updates" in content:
            content = content.replace("## Recent Updates\n", f"## Recent Updates\n\n- **{date}** — {reason}\n")
        else:
            content += f"\n## Recent Updates\n\n- **{date}** — {reason}\n"
        with open(path, 'w') as f:
            f.write(content)
    else:
        # Create new entity
        with open(path, 'w') as f:
            f.write(build_frontmatter(name, "entity", [], [], date))
            f.write(f"# {name}\n\n")
            f.write(f"**Note:** This entity was created/updated based on: {reason}\n\n")
            f.write("## Overview\n\n_(expand with sources)_\n\n")
            f.write("## Related\n\n- _(add links to related entities and topics)_\n")

    log(f"Upserted entity: {filename}")

def _upsert_topic(name, reason, date):
    """Create or update a topic page"""
    filename = name + ".md"
    path = WIKI_DIR / "topics" / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        with open(path) as f:
            content = f.read()
        content = content.replace("stale: true", "stale: false")
        content = content.replace("updated: YYYY-MM-DD", f"updated: {date}")
        if "## Recent Updates" in content:
            content = content.replace("## Recent Updates\n", f"## Recent Updates\n\n- **{date}** — {reason}\n")
        else:
            content += f"\n## Recent Updates\n\n- **{date}** — {reason}\n"
        with open(path, 'w') as f:
            f.write(content)
    else:
        with open(path, 'w') as f:
            f.write(build_frontmatter(name, "topic", [], [], date))
            f.write(f"# {name}\n\n")
            f.write(f"**Note:** This topic was created/updated based on: {reason}\n\n")
            f.write("## Overview\n\n_(expand with sources)_\n\n")
            f.write("## Key Concepts\n\n- _(add key concepts as they emerge)_\n")
            f.write("## Related Topics\n\n- _(add links to related topics)_\n")

    log(f"Upserted topic: {filename}")

def _append_log(date, operation, title, details):
    entry = f"\n## [{date}] {operation} | {title}\n"
    for d in details:
        entry += f"- {d}\n"
    with open(LOG, 'a') as f:
        f.write(entry)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Ingest a source into the Implica wiki")
    parser.add_argument("source", help="Path to source file or URL")
    parser.add_argument("--type", default="article", choices=["paper", "article", "note", "url"],
                        help="Type of source (default: article)")
    parser.add_argument("--name", help="Override the slug name")
    args = parser.parse_args()

    try:
        ingest_file(args.source, args.type, args.name)
    except Exception as e:
        log(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
