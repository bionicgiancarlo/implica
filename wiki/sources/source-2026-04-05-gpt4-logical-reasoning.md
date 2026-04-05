---
title: "Source: GPT-4 Logical Reasoning Evaluation"
created: 2026-04-05
updated: 2026-04-05
tags: [LLM, GPT-4, ChatGPT, logical-reasoning, benchmark, NLP]
summary: "Paper evaluating ChatGPT and GPT-4 on logical reasoning benchmarks — GPT-4 wins but both struggle on OOD data."
sources: [source-2026-04-05-gpt4-logical-reasoning]
---

# GPT-4 Logical Reasoning Evaluation

## Paper Info
- **arXiv:** [2304.03439](https://arxiv.org/abs/2304.03439)
- **Authors:** Hanmeng Liu et al.
- **Published:** April 2023

## Summary

The paper evaluates ChatGPT and GPT-4 on multiple logical reasoning benchmarks (LogiQA, ReClor, AR-LSAT). Key result: GPT-4 outperforms ChatGPT on most tasks, but both models significantly degrade on out-of-distribution (OOD) datasets. The authors release a new benchmark suite called **LogiEval**.

## Key Findings

| Finding | Detail |
|---------|--------|
| Established benchmarks | Both do well on LogiQA, ReClor |
| Out-of-distribution | Both degrade significantly on OOD data |
| GPT-4 vs ChatGPT | GPT-4 performs better on most tasks |
| ChatGPT vs RoBERTa | ChatGPT > fine-tuned RoBERTa on most |
| NLI tasks | Both struggle most with natural language inference |

## Takeaways

1. **Benchmark performance ≠ true reasoning ability** — performance drops on novel distributions
2. **GPT-4 is better but not fundamentally different** at logical reasoning
3. **OOD generalization is a key weakness** of current LLMs
4. **Logical reasoning remains an open problem** for LLMs

## Related Concepts
- [[concepts/logical-reasoning]]
- [[concepts/LLM-evaluation]]
- [[concepts/out-of-distribution-generalization]]

## Related Entities
- [[entities/gpt-4]]
- [[entities/chatgpt]]

---

*Ingested: 2026-04-05*
