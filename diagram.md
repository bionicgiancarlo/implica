# LLM Wiki System Architecture

```mermaid
flowchart TB
    subgraph USER["👤 YOU (Gabriele)"]
        U1["Drop sources into raw/sources/"]
        U2["Ask questions via Telegram"]
        U3["Browse the wiki on GitHub"]
    end

    subgraph AGENT["🧠 GIANCARLO (LLM Agent)"]
        A1["Ingest Workflow"]
        A2["Query Workflow"]
        A3["Lint Workflow"]
    end

    USER -->|"Telegram"| AGENT
    U1 -->|"drop file"| RAW

    subgraph WIKI["📚 THE WIKI"]
        RAW["📁 raw/sources/"] 
        PAGES["📄 wiki/{entities,concepts,sources,syntheses,comparisons,overviews}/"]
        NAV["📋 index.md + 📝 log.md"]
    end

    AGENT -->|"reads"| RAW
    AGENT -->|"writes|updates"| PAGES
    AGENT -->|"updates"| NAV
    AGENT -->|"commits"| REPO
    PAGES -->|"power queries"| NAV

    subgraph REPO["🔀 GitHub: bionicgiancarlo/implica"]
        R1["Version history"]
        R2["Every change = commit"]
    end
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
