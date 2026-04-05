---
title: "LLM Evaluation"
created: 2026-04-05
updated: 2026-04-05
tags: [LLM, evaluation, benchmark, methodology]
summary: "Methods for assessing LLM capabilities. Benchmarks are common but can be misleading — OOD generalization is a key gap."
sources: [source-2026-04-05-gpt4-logical-reasoning]
---

# LLM Evaluation

## Overview
Evaluating large language models is an open problem. Common approaches:

### Benchmarks
Standardized datasets with ground truth answers:
- MMLU, HELM, BIG-Bench — general capability
- LogiQA, ReClor — logical reasoning
- HumanEval — code generation
- MATH — mathematical reasoning

### Limitations
1. **Benchmark saturation** — models can overfit to specific datasets
2. **OOD generalization** — strong on-distribution, weak off-distribution
3. **Metric mismatch** — BLEU/accuracy don't capture actual performance
4. **Contamination** — training data may include benchmark data

## The Right framing
From the GPT-4 logical reasoning paper:
> "Benchmark performance ≠ true reasoning ability"

A model that scores 90% on LogiQA but 40% on a similar OOD dataset hasn't truly "learned" logical reasoning.

## In the Wiki
- First evaluation: [[sources/source-2026-04-05-gpt4-logical-reasoning]]

## Related Concepts
- [[concepts/logical-reasoning]]
- [[concepts/out-of-distribution-generalization]]
- [[concepts/benchmark-overfitting]]

## Related Entities
- [[entities/gpt-4]]
- [[entities/chatgpt]]
