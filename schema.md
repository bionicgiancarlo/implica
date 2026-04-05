# Wiki Schema

This is the schema for the Gabriele's LLM Wiki. It tells me (Giancarlo) how to structure, maintain, and work with this wiki.

---

## Directory Structure

```
wiki/
├── WIKI.md          # The idea file (what this wiki is)
├── schema.md        # This file - conventions and workflows
├── index.md         # Content catalog - updated on every ingest
├── log.md           # Chronological record - append only
├── README.md        # Entry point - overview of the wiki
├── raw/             # Immutable source documents
│   ├── sources/     # Articles, papers, documents
│   └── assets/      # Images, data files from sources
└── wiki/            # LLM-generated markdown files
    ├── entities/    # Pages about specific things (people, places, products)
    ├── concepts/    # Pages about abstract topics and ideas
    ├── sources/     # Summary pages for each ingested source
    ├── syntheses/   # High-level synthesis of multiple sources
    ├── comparisons/ # Side-by-side comparisons
    └── overviews/   # Broad topic overviews
```

---

## File Naming Conventions

- **Pages:** lowercase-with-hyphens.md (e.g., `attention-mechanism.md`, `transformer-architecture.md`)
- **Sources:** source-YYYY-MM-DD-short-title.md (e.g., `source-2026-04-05-llm-wiki-pattern.md`)
- **Images:** descriptive-name.ext (e.g., `transformer-attention-head.png`)

---

## Page Template

Every wiki page should have this frontmatter:

```markdown
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
sources: [source-2026-04-05-example]  # Only if content came from sources
summary: One-line description for index.md
---

# Page Title

## Overview
...

## Key Points
...

## Details
...

## Related
- [[entity/other-page]] or [[concept/other-concept]]
```

---

## Workflows

### Ingesting a Source

1. Drop the source file into `wiki/raw/sources/`
2. Tell me: "Ingest the source at `wiki/raw/sources/filename`"
3. I will:
   - Read the source
   - Create a summary page at `wiki/wiki/sources/source-YYYY-MM-DD-title.md`
   - Update `index.md` with the new page
   - Update relevant entity and concept pages
   - Add entry to `log.md`
   - Cross-reference with existing pages

### Answering a Query

1. You ask a question
2. I:
   - Read `index.md` to find relevant pages
   - Read those pages
   - Synthesize an answer with citations
   - If the answer is valuable/persistent, offer to file it as a new wiki page

### Lint (Health Check)

Periodically, tell me: "Lint the wiki"
I will check for:
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages with no inbound links
- Concepts mentioned but lacking pages
- Missing cross-references
- Data gaps

---

## Index Format

`index.md` structure:

```markdown
# Wiki Index

## Pages (N total)

### Entities
| Page | Summary | Updated |
|------|---------|---------|
| [[entities/name]] | One-line summary | YYYY-MM-DD |

### Concepts
| Page | Summary | Updated |
|------|---------|---------|
| [[concepts/name]] | One-line summary | YYYY-MM-DD |

### Sources
| Page | Summary | Sources | Updated |
|------|---------|---------|---------|
| [[sources/title]] | One-line summary | 1 | YYYY-MM-MM |

## Recently Updated
- [[page]] - YYYY-MM-DD
```

---

## Log Format

`log.md` format — entries start with `## [date] type | description`:

```markdown
## [2026-04-05] ingest | Source title
- Added summary page
- Updated entities: entity1, entity2
- Updated concepts: concept1
- Cross-referenced with: existing-page

## [2026-04-05] query | Question summary
- Answered: brief answer
- Filed as: [[wiki/page]]

## [2026-04-05] lint | Health check
- Found: 2 orphan pages, 1 contradiction
- Fixed: ...
```

---

## Cross-Reference Style

Use wiki-links for internal pages:
- `[[entities/elon-musk]]` - links to entity page
- `[[concepts/attention-mechanism]]` - links to concept page
- `[[sources/2026-04-05-paper]]` - links to source summary

Use full URLs for external links: `[Title](https://example.com)`

---

## Quality Standards

1. **Every page needs a summary** — one line for the index
2. **Every page needs tags** — at least one
3. **Sources must be cited** — link back to source summary pages
4. **Cross-link aggressively** — if you mention a concept, link to its page
5. **Update on ingest** — don't leave old pages stale
6. **Log everything** — every operation gets a log entry

---

## Git Workflow

The wiki is a git repo. Commit changes regularly:
- `git add -A && git commit -m "Ingest: source title"` after each ingest
- `git add -A && git commit -m "Lint: fixes and updates"` after lint passes

This gives you version history for free.

---

*Last updated: 2026-04-05*
