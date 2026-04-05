# LLM Wiki — Standalone Research Knowledge Base

> A self-contained personal wiki system powered by LLMs, designed to be queried directly by a human and optionally connected to an AI agent (Giancarlo) via MCP.

---

## Overview

The system is a directory of markdown files organized as a wiki, with:
- A **query engine** (qmd) for direct, instant search without an LLM
- An **ingestion CLI** for processing new sources
- A **maintenance CLI** for linting and health checks
- A **schema** defining conventions so any LLM (or Giancarlo via MCP) can maintain it consistently

Gabriele uses it directly. Giancarlo connects via MCP when needed.

---

## Directory Structure

```
llm-wiki/
├── README.md              # How to use the system
├── SCHEMA.md               # Wiki conventions (source format, page naming, cross-ref rules)
├── config/
│   └── qmd.yaml            # qmd search engine config
├── raw/                    # Immutable source documents
│   ├── sources.md          # Index of all sources with metadata
│   └── [source files]      # PDFs, markdown, articles (by date + short slug)
├── wiki/                   # LLM-generated pages
│   ├── index.md            # Catalog of all wiki pages (auto-generated)
│   ├── log.md              # Chronological append-only log
│   ├── entities/           # Pages about specific things (people, proteins, concepts)
│   ├── topics/             # Pages about broad topics/themes
│   ├── syntheses/          # Pages that synthesize multiple sources
│   └── comparisons/        # Side-by-side comparisons, tables
├── scripts/                # Standalone CLI tools
│   ├── ingest.py           # Ingest a new source
│   ├── query.py            # Query the wiki (wraps qmd)
│   ├── lint.py             # Health check the wiki
│   └── maintain.py         # Update index, cross-refs, stale page flags
└── .mcp/                   # MCP server config (for Giancarlo connection)
    └── server.py           # MCP server exposing wiki operations
```

---

## Core Concepts

### Raw Sources
Immutable source documents. Never edited after ingestion. Organized by date + short slug.
Naming: `YYYY-MM-DD_short-slug.ext`

### Wiki Pages
LRU-generated markdown files. Fully owned by the system. Types:
- **entity** — a specific thing (X protein, Y algorithm, Z paper)
- **topic** — a broad theme or area
- **synthesis** — a page that pulls together multiple sources around a question
- **comparison** — structured comparison of alternatives
- **source-summary** — a page summarizing one raw source

### Schema (SCHEMA.md)
Defines:
- Page frontmatter format (title, type, tags, sources, date, stale?)
- File naming conventions
- Cross-reference format (`[[page-name]]` or `[[filename|Display Text]]`)
- What to do on ingest (update index, update log, update related entities)
- Lint rules (orphan detection, contradiction detection, stale claim flagging)
- Query response format conventions

### Log (log.md)
Append-only. Format: `## [YYYY-MM-DD] operation | Description`
Operations: `ingest`, `query`, `lint`, `update`, `note`

### Index (wiki/index.md)
Auto-generated catalog. One line per page: `| [[page-name]] | one-line summary | type | sources |`

---

## CLI Commands

### `ingest <source> [--type paper|article|note]`
1. Copy source to `raw/` with proper naming
2. Read and extract key information
3. Update `raw/sources.md` with metadata
4. Create/update relevant wiki pages (entity, topic, source-summary)
5. Update `wiki/index.md`
6. Append to `wiki/log.md`

### `query <question>`
Wraps qmd. Returns ranked page list with snippets. Gabriele reads results, decides what to explore.

### `lint`
Health check:
- Find orphan pages (no inbound links)
- Flag pages with outdated claims
- Find missing cross-references between related pages
- Identify concepts mentioned but without dedicated pages
- Suggest new sources to fill gaps

### `maintain`
Run maintenance tasks:
- Regenerate `wiki/index.md`
- Update cross-references on modified pages
- Flag stale pages (not updated in N days)

---

## Search Engine (qmd)

qmd is a local search engine for markdown with BM25 + embedding hybrid search and LLM re-ranking.

Config: `config/qmd.yaml`

Features:
- CLI: `qmd query "your question"` → ranked results
- MCP server: can be used by Giancarlo as a tool
- Web UI option for browsing

Why qmd: fast, local, no external API, good for real-time search

---

## MCP Server (`.mcp/server.py`)

Exposes wiki operations to Giancarlo:

```
mcp__wiki__ingest(source_path)       → triggers ingest CLI
mcp__wiki__query(question)           → runs qmd, returns results
mcp__wiki__lint()                    → runs lint, returns issues
mcp__wiki__read(page_name)           → reads a wiki page
mcp__wiki__search(query)             → thin wrapper around qmd
mcp__wiki__status()                  → returns wiki stats
```

The MCP server is standalone — Giancarlo connects to it as an MCP client.

---

## Giancarlo Integration (Skill)

A Giancarlo skill (`llm-wiki` or similar) that:
1. Knows the wiki path and schema
2. Has the MCP server tools available
3. Knows to run `ingest` when Gabriele shares a source
4. Knows to query via qmd/MCP before synthesizing
5. Follows SCHEMA.md conventions when editing wiki pages

---

## Workflow

### Gabriele Direct Use
1. Drop source in `raw/`, run `ingest`
2. Browse wiki pages in Obsidian or VS Code
3. Query with `qmd query "..."` or via Obsidian search
4. Run `lint` periodically

### Giancarlo-Assisted Use
1. Gabriele shares a paper/URL with Giancarlo
2. Giancarlo runs `ingest` via MCP
3. Giancarlo can `query` or `search` the wiki before synthesizing
4. Giancarlo can run `lint` to surface issues
5. Gabriele browses results directly

### Shared Use
Gabriele browses the wiki directly. Giancarlo maintains it. Both can search.

---

## Implementation Order

1. **Phase 1: Core wiki structure**
   - Create directory layout
   - Write SCHEMA.md
   - Set up `raw/sources.md` and `wiki/index.md`, `wiki/log.md`
   - Test manual page creation following schema

2. **Phase 2: Ingest CLI**
   - `scripts/ingest.py` — reads a source, extracts key info, updates wiki
   - Connect to LLM API for extraction (or use Giancarlo directly as the LLM)
   - Update index and log

3. **Phase 3: qmd integration**
   - Install qmd
   - Configure it to index `wiki/` directory
   - Test CLI query

4. **Phase 4: Lint + Maintain CLIs**
   - `scripts/lint.py` — health checks
   - `scripts/maintain.py` — index regeneration, cross-ref updates

5. **Phase 5: MCP server**
   - `.mcp/server.py` exposing all operations
   - Test with Giancarlo skill

6. **Phase 6: Giancarlo skill**
   - `skills/llm-wiki/SKILL.md` — describes wiki conventions and tools
   - Wire up MCP tools

---

## Key Design Decisions

- **No database** — everything is markdown files. Git tracks history.
- **qmd for search** — embeddings stay local, no external API dependency
- **Human writes pages only for schema/design decisions** — all knowledge pages are LLM-generated
- **Schema is law** — any LLM (Giancarlo or future agent) must follow SCHEMA.md
- **MCP is optional** — system works fully standalone without Giancarlo
- **Ingest is the hard part** — needs a good LLM prompt/template for extraction

---

## Reference

Original spec: see `llm-wiki-spec.md` in workspace root (the source document Gabriele provided)
