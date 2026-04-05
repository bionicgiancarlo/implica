# SCHEMA.md — Implica Wiki Conventions

> Every LLM (including Giancarlo via MCP) must follow these conventions when reading or writing wiki pages. This is the contract.

---

## Page Types

| Type | Purpose | Example |
|------|---------|---------|
| `entity` | A specific thing | `Prefrontal-Cortex.md`, `Transformer-Architecture.md` |
| `topic` | A broad theme or domain | `Consciousness.md`, `Protein-Folding.md` |
| `synthesis` | Multi-source synthesis around a question | `Memory-Consolidation-Hypothesis.md` |
| `comparison` | Side-by-side comparison | `CRISPR-vs-Base-Editing.md` |
| `source-summary` | One-page summary of a raw source | `2026-01-15-attention-is-all-you-need.md` |

---

## Frontmatter

Every wiki page MUST start with this frontmatter block:

```markdown
---
title: "Page Title"
type: entity | topic | synthesis | comparison | source-summary
tags: [tag1, tag2]
sources: [link to raw sources, if applicable]
created: YYYY-MM-DD
updated: YYYY-MM-DD
stale: false
---
```

- `stale: true` means the page may have outdated information and should be reviewed
- `sources` is optional but strongly encouraged for synthesis and entity pages
- `tags` help with discovery and dataview queries

---

## File Naming

- **Entities**: `Camel-Case-Description.md`
- **Topics**: `Camel-Case-Topic.md`
- **Syntheses**: `Descriptive-Title.md`
- **Comparisons**: `Thing-A-vs-Thing-B.md`
- **Source summaries**: `{date}-{short-slug}.md` (date of the source, not ingestion)

Cross-references use `[[filename|Display Text]]` or `[[filename]]` format.

---

## Cross-References

Link to related pages using Obsidian-style wiki links:

```markdown
This relates to [[Prefrontal-Cortex]] and [[Memory-Consolidation]].

See also: [[Transformer-Architecture|Transformers]] for the architecture.
```

Wiki links are preferred over raw URLs for internal pages. External links use standard markdown.

---

## Source Naming (raw/)

Raw sources use the format: `{YYYY-MM-DD}-{short-slug}.{ext}`

Examples:
- `2026-01-15-attention-is-all-you-need.pdf`
- `2026-03-02-neural-ode-review.md`
- `2026-04-01-gabriele-lecture-notes.md`

The `raw/sources.md` index tracks all sources with metadata.

---

## On Ingest

When ingesting a new source, the LLM MUST:

1. Create a `wiki/source-summaries/{date}-{slug}.md` page summarizing the source
2. Update `wiki/index.md` with the new page
3. Append an entry to `wiki/log.md`
4. Update or create relevant `entities/` and `topics/` pages that the source touches
5. Add cross-references where relevant
6. Update `raw/sources.md` with source metadata

Ingest should touch multiple wiki pages, not just create one summary.

---

## On Query Response

When answering a query from the wiki (not raw sources):

1. Search relevant pages via qmd or index
2. Read the top pages
3. Synthesize an answer
4. If the answer is valuable enough to keep, offer to save it as a synthesis page
5. Always cite sources: `[[page-name]]` or `[source](url)`

---

## Lint Rules

A healthy wiki should have:
- No orphan pages (every page should have at least one inbound link)
- No `stale: true` pages that are actually still current
- No contradictions between pages (flag if detected)
- All major concepts from source summaries referenced in entity/topic pages
- Cross-references where connections exist

Lint output format:
```
ISSUE: {type} | {description} | {file(s) affected}
```

---

## Index Format (wiki/index.md)

```markdown
# Index

## Entities
| Page | Summary | Sources |
|------|---------|---------|
| [[Entity-Name]] | One-line summary | 2 |

## Topics
| Page | Summary | Updated |
|------|---------|---------|
| [[Topic-Name]] | One-line summary | 2026-01-15 |

## Syntheses
| Page | Question | Sources | Updated |
|------|----------|---------|---------|
| [[Synthesis-Name]] | What it addresses | 3 | 2026-01-20 |

## Comparisons
| Page | Things Compared | Updated |
|------|-----------------|---------|
| [[A-vs-B]] | X vs Y | 2026-02-01 |

## Source Summaries
| Page | Source | Date |
|------|--------|------|
| [[2026-01-15-attention]] | Attention Is All You Need | 2026-01-15 |
```

---

## Log Format (wiki/log.md)

Append-only. Each entry:

```markdown
## [YYYY-MM-DD] operation | Description
- Details
```

Operations: `ingest`, `query`, `lint`, `update`, `note`

Example:
```markdown
## [2026-04-05] ingest | Attention Is All You Need paper
- Created [[2026-04-05-attention-is-all-you-need]]
- Updated [[Transformer-Architecture]]
- Updated [[Attention-Mechanism]]
- Linked from [[NLP-Overview]]
```

---

## Page Content Conventions

- Use `##` for headings within pages
- Keep pages focused — one concept/entity per page when possible
- If a page gets too large, split it and cross-reference
- Use bullet lists for properties/attributes
- Use tables for comparisons
- Bold key terms on first introduction
- No trailing whitespace

---

## Conventions for Synthesis Pages

Synthesis pages should:
1. State the question or hypothesis clearly at the top
2. Present evidence from multiple sources
3. Note areas of disagreement or uncertainty
4. End with open questions or next steps
5. Be updated when new relevant sources are ingested

---

## Giancarlo Integration

Giancarlo connects via the MCP server (`.mcp/server.py`). The schema is self-contained — any LLM can maintain the wiki following these conventions without needing the MCP connection.
