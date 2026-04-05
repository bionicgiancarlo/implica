# Gabriele's Wiki

A personal knowledge base, maintained by Giancarlo (LLM).

## What is this?

This is a persistent, compounding wiki — a structured collection of markdown files that sits between raw sources and answers. When sources are ingested, the wiki is updated. When you ask questions, the wiki is queried. Knowledge compounds rather than being rediscovered.

Learn more: [[WIKI.md]]

## Structure

- `raw/` — Immutable source documents (articles, papers, data)
- `wiki/` — LLM-generated pages (entities, concepts, syntheses, comparisons)
- `schema.md` — This wiki's conventions and workflows
- `index.md` — Catalog of all wiki pages
- `log.md` — Chronological record of operations

## Quick Start

**Ingest a source:**
> "Ingest the article at `raw/sources/my-article.md`"

**Ask a question:**
> "What do we know about X?"

**Health check:**
> "Lint the wiki"

## Recent Activity

See [[log.md]] for the full timeline.

---

*Wiki initialized: 2026-04-05*
┌─────────────────────────────────────────────────────────────────────────────┐
#                              THE LLM WIKI SYSTEM                              #
##                              Gabriele's Knowledge Base                        #
#################################################################################

                              ┌──────────────────────┐
                              │     YOU (Gabriele)    │
                              │ ─────────────────────  │
                              │  • Drop sources       │
                              │  • Ask questions      │
                              │  • Direct analysis    │
                              │  • Review wiki        │
                              └──────────┬───────────┘
                                         │
                                         │  (Telegram / Chat)
                                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
#                              GIANCARLO (LLM AGENT)                           #
##                                    brain 🧠                                   #
└────────────────────────────────────────────────────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
   │   INGEST WORKFLOW    │   │   QUERY WORKFLOW    │   │    LINT WORKFLOW    │
   │                     │   │                     │   │                     │
   │ 1. Read raw source  │   │ 1. Read index.md    │   │ 1. Find orphans     │
   │ 2. Create summary   │   │ 2. Search wiki pages │   │ 2. Find contradictions│
   │ 3. Update entities   │   │ 3. Synthesize answer│   │ 3. Find stale claims│
   │ 4. Update concepts   │   │ 4. File as new page │   │ 4. Suggest fixes    │
   │ 5. Update index      │   │    if valuable      │   │                     │
   │ 6. Log to log.md    │   │                     │   │                     │
   └──────────┬──────────┘   └──────────┬──────────┘   └──────────┬──────────┘
              │                          │                          │
              └──────────────────────────┼──────────────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
#                                   THE WIKI                                    #
##                              persistent knowledge                             #
##                              compounding over time                             #
#################################################################################

   ┌──────────────────────────────────────────────────────────────────────────┐
   #                              RAW SOURCES                                   #
   #  ────────────────────────────────────────────────────────────────────────  #
   #  immutable source documents (read-only, never modified)                    #
   #                                                                              #
   #    📄 articles/         📄 papers/           📄 notes/                       #
   #    📄 tweets/          📄 videos.txt        📄 podcasts/                   #
   #                                                                              #
   #  Location: /implica/raw/sources/                                            #
   └──────────────────────────────────────────────────────────────────────────┘
                                         │
                                         │ (Giancarlo reads)
                                         ▼
   ┌──────────────────────────────────────────────────────────────────────────┐
   #                              WIKI PAGES                                    #
   #  ────────────────────────────────────────────────────────────────────────  #
   #  LLM-generated markdown files (owned entirely by Giancarlo)               #
   #                                                                              #
   #   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   #
   #   │  ENTITIES   │  │  CONCEPTS   │  │  SOURCES    │  │  SYNTHESES  │   #
   #   │             │  │             │  │             │  │             │   #
   #   │ gpt-4.md    │  │ logical-    │  │ source-     │  │ llm-        │   #
   #   │ chatgpt.md  │  │ reasoning.md│  │ 2026-04-05-│  │ comparison.md│  #
   #   │ openai.md  │  │ attention.md│  │ gpt4.md    │  │             │   #
   #   │             │  │             │  │             │  │             │   #
   #   │ SPECIFIC    │  │ ABSTRACT    │  │ PER-SOURCE  │  │ CROSS-      │   #
   #   │ THINGS     │  │ IDEAS       │  │ SUMMARIES   │  │ SOURCE      │   #
   #   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   #
   #                                                                              #
   #   ┌─────────────┐  ┌─────────────┐                                        #
   #   │ COMPARISONS │  │ OVERVIEWS   │                                        #
   #   │             │  │             │                                        #
   #   │ gpt4-vs-    │  │ llm-        │                                        #
   #   │ claude.md   │  │ landscape-  │                                        #
   #   │             │  │ overview.md │                                        #
   #   └─────────────┘  └─────────────┘                                        #
   #                                                                              #
   #  Location: /implica/wiki/{entities,concepts,sources,syntheses,etc.}         #
   └──────────────────────────────────────────────────────────────────────────┘
                                         │
                                         │ (powers queries)
                                         ▼
   ┌──────────────────────────────────────────────────────────────────────────┐
   #                              NAVIGATION LAYER                              #
   #  ────────────────────────────────────────────────────────────────────────  #
   #   📋 index.md          📝 log.md           📖 README.md                     #
   #   Content catalog     Append-only        Entry point                      #
   #   Updated on ingest   All operations     Overview of wiki                 #
   #                                                                              #
   #  Location: /implica/{index.md,log.md,README.md}                             #
   └──────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────────────────┐
   #                               GIT REPO                                     #
   #  ────────────────────────────────────────────────────────────────────────  #
   #   Every change versioned. Every ingest = commit. Full history.            #
   #                                                                              #
   #   git commit -m "Ingest: new paper"   ← after each source                  #
   #   git log --graph --oneline          ← timeline of wiki evolution          #
   #                                                                              #
   #   Remote: github.com/bionicgiancarlo/implica                              #
   └──────────────────────────────────────────────────────────────────────────┘

---

## HOW IT WORKS (3 Operations)

### INGEST ────────────────────────────
  You: "Ingest the paper at raw/sources/my-paper.pdf"
         │
         ▼
  Giancarlo reads the paper
         │
         ▼
  Giancarlo creates:
    ✓ Summary page (wiki/sources/)
    ✓ Entity pages for things mentioned
    ✓ Concept pages for topics covered
    ✓ Updates index.md
    ✓ Appends to log.md
    ✓ Cross-references everything
         │
         ▼
  Git commit: "Ingest: paper title"
         │
         ▼
  Wiki now has the knowledge — compounding


### QUERY ─────────────────────────────
  You: "What do we know about OOD generalization?"
         │
         ▼
  Giancarlo reads index.md
         │
         ▼
  Giancarlo finds: [[concepts/out-of-distribution-generalization]]
         │
         ▼
  Giancarlo reads the concept page + linked entities
         │
         ▼
  Giancarlo synthesizes an answer with citations
         │
         ▼
  You: "Great analysis" — if valuable, Giancarlo files it as a new wiki page


### LINT ──────────────────────────────
  You: "Lint the wiki"
         │
         ▼
  Giancarlo checks:
    • Orphan pages (no inbound links)
    • Contradictions between pages
    • Stale claims superseded by new sources
    • Missing cross-references
    • Concepts mentioned but not yet as pages
         │
         ▼
  Giancarlo reports findings + fixes what it can
         │
         ▼
  Git commit: "Lint: fixed X, found Y"


---

## WHY THIS WORKS

  Human: curates sources, asks questions, thinks about meaning
  LLM:    reads, summarizes, cross-references, files, updates, maintains

  Humans abandon wikis because maintenance > value as it grows
  LLMs don't get bored, don't forget, can touch 15 files at once
  → Maintenance cost ≈ zero → wiki stays alive and compounds

---

*Generated: 2026-04-05 | Built with Giancarlo 🧠*
