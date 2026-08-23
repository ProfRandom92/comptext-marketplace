---
name: run-benchmark
description: Use when the user asks to run or rerun a Raw vs CompText benchmark, validate token reduction, or check quality regressions.
---

# Run benchmark

For the built-in offline fixture run exactly:

`node "${CODEX_HOME:-$HOME/.codex}/plugins/cache/comptext-marketplace/comptext-benchmark/0.1.5/scripts/smoke-receipt.mjs" /root/comptext/apps/comptext-benchmark-lab`

Treat its single JSON line as the primary evidence receipt. Do not run `find`, list run files, inspect bundled script source, or read full `result.json` unless that command fails or the user asks for raw evidence.

For live runs, reuse the Benchmark Lab, freeze one manifest, keep non-experimental variables identical across arms, and load `../../references/benchmark-policy.md`. MCP is optional.

Never claim an efficiency win when the receipt reports a quality regression. Return status, digests, runner/model, arm state, quality, efficiency, verdict, and artifact paths.