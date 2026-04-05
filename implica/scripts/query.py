#!/usr/bin/env python3
"""
query.py — Query the Implica wiki using qmd or basic grep

Usage:
  ./scripts/query.py "your question"
"""

import sys
import subprocess
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent
WIKI_DIR = WIKI_ROOT / "wiki"

def query_qmd(question):
    """Use qmd if available"""
    try:
        result = subprocess.run(
            ["qmd", "query", question, "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(WIKI_ROOT)
        )
        if result.returncode == 0:
            return result.stdout, None
        return None, result.stderr
    except FileNotFoundError:
        return None, "qmd not installed"

def query_grep(question, limit=20):
    """Fallback: grep-based search across markdown files"""
    import re
    terms = question.lower().split()
    results = []

    for md in WIKI_DIR.rglob("*.md"):
        if md.name in ["index.md", "log.md"]:
            continue
        with open(md, errors='replace') as f:
            content = f.read()

        # Simple relevance: count term matches
        content_lower = content.lower()
        score = sum(1 for term in terms if term in content_lower)

        if score > 0:
            # Get first matching line
            first_match = ""
            for line in content.splitlines():
                if any(term in line.lower() for term in terms):
                    first_match = line.strip()[:120]
                    break

            results.append({
                "file": str(md.relative_to(WIKI_ROOT)),
                "score": score,
                "preview": first_match
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit], None

def main():
    if len(sys.argv) < 2:
        print("Usage: query.py <question>")
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    # Try qmd first
    out, err = query_qmd(question)
    if out:
        print(out)
        return 0

    # Fallback to grep
    results, err = query_grep(question)
    if err:
        print(f"Search error: {err}", file=sys.stderr)

    if results:
        print(f"Search results for: {question}")
        print("=" * 60)
        for r in results:
            print(f"\n[{r['file']}] (score: {r['score']})")
            print(f"  {r['preview']}")
        print(f"\n({len(results)} results)")
    else:
        print(f"No results for: {question}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
