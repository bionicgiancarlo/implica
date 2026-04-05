---
title: "Out-of-Distribution Generalization"
created: 2026-04-05
updated: 2026-04-05
tags: [generalization, robustness, ML, LLM]
summary: "The ability to perform well on inputs different from training data. The key weakness identified in GPT-4/ChatGPT evaluation."
sources: [source-2026-04-05-gpt4-logical-reasoning]
---

# Out-of-Distribution (OOD) Generalization

## Definition
OOD generalization refers to a model's ability to perform well on inputs that differ from what it was trained on — different distributions, novel problem formats, unseen reasoning patterns.

## Why It Matters
A model that generalizes OOD has learned the underlying task, not just memorized patterns. This is the difference between:
- **Pattern matching** — high accuracy on seen distributions, crashes on new ones
- **True reasoning** — handles novel problem forms robustly

## Key Finding from GPT-4 Evaluation
Both ChatGPT and GPT-4 showed:
- Strong performance on established benchmarks (LogiQA, ReClor)
- **Significant degradation** on OOD variants and AR-LSAT
- Especially poor on NLI (natural language inference) tasks

This suggests current LLMs are closer to sophisticated pattern matchers than genuine reasoners.

## Implications
1. Benchmark leaderboards may overestimate true capability
2. OOD robustness is a key unsolved problem
3. Evaluation methodology matters as much as model capability

## In the Wiki
- Central finding in [[sources/source-2026-04-05-gpt4-logical-reasoning]]

## Related Concepts
- [[concepts/benchmark-overfitting]]
- [[concepts/llm-evaluation]]
- [[concepts/logical-reasoning]]
