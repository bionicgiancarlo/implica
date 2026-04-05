# Implica — Personal Research Wiki

A **persistent, compounding knowledge base** powered by LLMs.

The wiki sits between you and your raw sources. When you add a source, the LLM reads it, extracts key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting contradictions, strengthening cross-references. **The knowledge is compiled once and kept current, not re-derived on every query.**

---

## Quick Start

### Adding a source

```bash
./scripts/ingest.py path/to/paper.pdf --type paper
```

Or drop a file in `raw/` and run:

```bash
./scripts/ingest.py raw/2026-04-05-my-paper.pdf --type paper
```

### Querying

```bash
./scripts/query.py "what does the literature say about X?"
```

Or use qmd directly:

```bash
qmd query "your question"
```

### Health check

```bash
./scripts/lint.py
```

---

## Structure

```
raw/                    # Source documents (immutable)
  sources.md            # Index of all sources

wiki/                   # LLM-generated wiki pages
  entities/            # Pages about specific things
  topics/              # Pages about broad themes
  syntheses/            # Multi-source synthesis pages
  comparisons/         # Side-by-side comparisons
  source-summaries/    # One-page summary per source
  index.md             # Auto-generated catalog
  log.md               # Append-only history

scripts/               # CLI tools
  ingest.py           # Ingest a new source
  query.py            # Query the wiki
  lint.py             # Health check
  maintain.py         # Update index, cross-refs

config/
  qmd.yaml            # Search engine config

.mcp/
  server.py           # MCP server for Giancarlo
```

---

## Core Principles

1. **Raw sources are immutable** — never edited after ingestion
2. **Wiki pages are LLM-generated** — humans don't write knowledge pages directly
3. **Schema is law** — all LLMs follow SCHEMA.md conventions
4. **Ingest once, query forever** — the compounding advantage
5. **Works standalone** — Giancarlo via MCP is optional

---

## Design

Inspired by the [LLM Wiki pattern](https://github.com/bionicgiancarlo/implica/blob/main/SPEC.md). Built on markdown files with git for version history. Local search via [qmd](https://github.com/tobi/qmd).

---

## Wiki Conventions

See [SCHEMA.md](./SCHEMA.md) for the full specification.
