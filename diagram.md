# LLM Wiki System Architecture

```mermaid
flowchart TB
    subgraph USER["👤 YOU (Gabriele)"]
        direction TB
        U1["Drop sources into raw/sources/"]
        U2["Ask questions via Telegram"]
        U3["Direct Giancarlo's analysis"]
        U4["Browse the wiki in GitHub"]
    end

    subgraph AGENT["🧠 GIANCARLO (LLM Agent)"]
        direction TB
        A1["Ingest Workflow"]
        A2["Query Workflow"]
        A3["Lint Workflow"]
    end

    subgraph WIKI["📚 THE WIKI (Persistent Knowledge)"]
        direction LR
        
        subgraph RAW["RAW SOURCES (Immutable)"]
            RS1["papers/"]
            RS2["articles/"]
            RS3["notes/"]
        end

        subgraph PAGES["WIKI PAGES (LLM-generated)"]
            direction TB
            WP1["🟦 entities/"]
            WP2["🟩 concepts/"]
            WP3["🟪 sources/"]
            WP4["🟫 syntheses/"]
            WP5["⬛ comparisons/"]
            WP6["⬜ overviews/"]
        end

        subgraph NAV["NAVIGATION"]
            IDX["📋 index.md"]
            LOG["📝 log.md"]
            README["📖 README.md"]
        end
    end

    subgraph GIT["🔀 GIT REPO"]
        G1["github.com/bionicgiancarlo/implica"]
        G2["Every change = commit"]
        G3["Full version history"]
    end

    USER -->|"Telegram"| AGENT
    U1 -->|"drop file"| RAW
    
    AGENT -->|"reads"| RAW
    AGENT -->|"writes/updates"| PAGES
    AGENT -->|"updates on every ingest"| NAV
    AGENT -->|"commits every operation"| GIT
    
    PAGES -->|"powers queries"| NAV
    NAV -->|"navigates"| PAGES
```

## Operations

### INGEST
```
You drop source → Giancarlo reads → Creates summary + entities + concepts → Updates index → Logs operation → Git commit
```

### QUERY
```
You ask → Giancarlo reads index → Finds relevant pages → Synthesizes answer with citations → Files valuable answers as new wiki pages
```

### LINT
```
You say "Lint" → Giancarlo checks: orphans, contradictions, stale claims, missing links → Reports + fixes
```

## Why This Works

| Human | LLM |
|-------|-----|
| Curation & questions | Reading, summarizing, cross-referencing |
| Meaning & direction | Filing, updating, maintaining |
| Asks good questions | Does all the bookkeeping |
| Thinks about implications | Keeps wiki consistent & current |

**Key insight:** Humans abandon wikis because maintenance burden > value as it grows. LLMs don't get bored or forget. Maintenance cost ≈ zero → wiki compounds forever.

---

*Built with Giancarlo 🧠 | 2026-04-05*
