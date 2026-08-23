---
name: verify-freshness
description: Use when the user explicitly asks whether verification evidence is fresh enough to support an AI completion claim after workspace mutations.
---

# Verify evidence freshness

For bundled fixtures, run exactly:
`node "${CODEX_HOME:-$HOME/.codex}/plugins/cache/comptext-marketplace/comptext-evidence/0.1.0/scripts/freshness-gate.mjs" "${CODEX_HOME:-$HOME/.codex}/plugins/cache/comptext-marketplace/comptext-evidence/0.1.0/fixtures/<fixture>.jsonl"`
Use only `stale-after-mutation`, `fresh-after-verification`, or `failed-mutation-does-not-stale`; do not inspect bundled source unless the command fails.

- For user traces, require bounded content-free JSONL containing only sequence, event type, and success state.
- A successful mutation makes prior verification stale; a failed mutation does not.
- Only successful verification after the latest successful mutation clears pending state; assertion never clears it.
- Do not persist prompts, source text, raw commands/output, credentials, or environment values in traces.
- Return trace digest, mutation/verification sequence, pending state, completion verdict, and reason.
- For Riqor comparisons, report compatibility or divergence; never claim this implementation is Riqor.
