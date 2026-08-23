---
name: inspect-benchmark
description: Use when the user asks for benchmark status, failures, evidence, active/completed arms, or whether a rerun is required.
---

# Inspect benchmark

- Resolve the exact run ID first and prefer immutable Benchmark Lab artifacts over process guesses.
- For `smoke-orion-001`, prefer `proof-summary.json`; regenerate it from `result.json` with bundled `scripts/proof-summary.mjs` if absent or stale.
- Read `events.jsonl` only when event-level failure evidence is required.
- For other runs, verify their actual data directory before reading it.
- Report status, runner, manifest digest, arm state, failures, evidence refs, metrics-so-far, and rerun decision.
- Never expose credentials, environment secrets, or unrelated raw logs.
- Load `../../references/benchmark-policy.md` only when policy interpretation is needed.