---
name: compile-context
description: Use when the user asks to build, validate, or minimize operational context from explicit required fields, constraints, dependencies, blockers, or recovery paths.
---

# Compile operational context

Build context before loading more source material. Create two bounded JSON files: a source summary with `source_digest` and available `field_paths`, and a contract with the explicit required fields and operational rules.

Run:
`node "${CODEX_HOME:-$HOME/.codex}/plugins/cache/comptext-marketplace/comptext-context/0.1.0/scripts/build-context.mjs" <source-summary.json> <contract.json>`

Treat the single JSON line as the primary context receipt. Do not include raw prompts, source text, secrets, command output, or unrelated repository content in either input.

Preserve semantic `required_order`; sort only set-like fields. If `validation.valid` is false, report the missing required fields instead of pretending the context is sufficient.

Return `context_id`, strategy, required/satisfied/missing fields, constraints, blockers, recovery paths, validation, and non-claims.