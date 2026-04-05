---
title: "Logical Reasoning"
created: 2026-04-05
updated: 2026-04-05
tags: [reasoning, NLP, cognition]
summary: "The ability to draw valid inferences from premises. Current LLMs like GPT-4 perform well on established benchmarks but degrade on OOD data."
sources: [source-2026-04-05-gpt4-logical-reasoning]
---

# Logical Reasoning

## Definition
Logical reasoning is the process of deriving conclusions from premises based on logical rules. It encompasses:
- Deductive reasoning (top-down, rule-based)
- Inductive reasoning (bottom-up, pattern-based)
- Abductive reasoning (best explanation)

## In NLP/AI
Logical reasoning is a key test of true language understanding. Benchmarks include:
- **LogiQA** — multi-choice reading comprehension with logical inference
- **ReClor** — logical reasoning in reading comprehension
- **AR-LSAT** — law school admission test-style reasoning
- **NLI datasets** — natural language inference (entailment, contradiction, neutral)

## Key Finding from Sources
> "Logical reasoning remains challenging for ChatGPT and GPT-4, especially on out-of-distribution and natural language inference datasets." — Liu et al., 2023

## The OOD Problem
Current LLMs excel on benchmarks they've seen during training but degrade on novel distributions. This suggests:
1. Performance ≠ genuine logical reasoning ability
2. Models may be pattern-matching rather than reasoning
3. Generalization to novel logical forms is unsolved

## In the Wiki
- Evaluated in [[sources/source-2026-04-05-gpt4-logical-reasoning]]
- Related entities: [[entities/gpt-4]], [[entities/chatgpt]]

## Related Concepts
- [[concepts/LLM-evaluation]]
- [[concepts/out-of-distribution-generalization]]
- [[concepts/benchmark-overfitting]]
