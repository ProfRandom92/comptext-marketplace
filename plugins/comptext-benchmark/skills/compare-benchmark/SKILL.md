---
name: compare-benchmark
description: Use when the user asks for a Raw vs CompText verdict, quality regression check, efficiency delta, or evidence-based benchmark comparison.
---

# Compare benchmark

- Prefer `proof-summary.json`; regenerate it from `result.json` with bundled `scripts/proof-summary.mjs` if absent or stale.
- Confirm the receipt is bound to the expected manifest/result digest before relying on it.
- Keep quality and efficiency separate and surface every regression flag.
- Read the full `result.json` only when the receipt is insufficient; read events only for event-level evidence.
- Lead with verdict, then quality deltas, efficiency deltas, regressions, and artifact/evidence references.
- Never hide failed arms or incompatible manifests by averaging.
- Load `../../references/benchmark-policy.md` only for ambiguity or live-run policy questions.