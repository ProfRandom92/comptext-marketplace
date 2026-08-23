# Benchmark policy

Use this reference only for live runs, schema ambiguity, or regression decisions.

- Freeze one manifest before execution.
- Hold taskset, evaluator, seed/repeats, and model settings constant across comparison arms except the declared experimental variable.
- Keep quality and efficiency separate.
- A token reduction is not a win if task success, semantic fidelity, constraint survival, or negation survival regresses materially.
- Preserve contradictions and hallucination/overclaim signals when available.
- Failed arms and missing evidence stay visible; never average them away.
- Derived receipts may summarize immutable artifacts but must carry a digest binding to the source result.
- Never infer benchmark numbers that were not measured.