# CompText Agent Marketplace

Private-first marketplace for focused CompText workflows across Codex and supported ChatGPT plugin surfaces.

## Plugins

- `comptext-benchmark` — reproducible Raw vs CompText benchmarks with quality-first receipts.
- `comptext-evidence` — deterministic verification-freshness gate for completion claims.
- `comptext-context` — compile minimal operational context from explicit requirements.
- `comptext-guard` — local pre-tool policy for secret reads and remote/release writes.

The plugins stay deliberately narrow. Shared computation and contracts live outside model context and are loaded only when needed.

## Git-backed install

```bash
codex plugin marketplace add ProfRandom92/comptext-marketplace
codex plugin add comptext-benchmark@comptext-marketplace
codex plugin add comptext-evidence@comptext-marketplace
codex plugin add comptext-context@comptext-marketplace
codex plugin add comptext-guard@comptext-marketplace
```

For isolated tests, set `CODEX_HOME` before installation. Script-backed skills resolve `${CODEX_HOME:-$HOME/.codex}` rather than assuming the default home.

## Verified release gate

Current development gate on the tablet runtime:

- Codex CLI `0.149.0`.
- all four plugins pass the current OpenAI local plugin validator.
- Plugin Eval: all four score `95/100 (A)`.
- shared contract selftest: `14/14` checks.
- Benchmark Lab: `19/19` tests.
- JSON, diff-whitespace, secret-shaped path/content, and symlink checks pass.
- clean local `CODEX_HOME` install discovers and enables all four plugins.

`comptext-benchmark` retains the deterministic fixture result Raw `1000` → CompText `420` input/effective-context tokens, a 58% reduction with no fixture quality regression. The fixture is a smoke test, not a general performance claim.

`comptext-context` preserves semantic order while canonicalizing set-like fields. `comptext-evidence` keeps freshness separate from semantic correctness. `comptext-guard` ships through the documented `hooks/hooks.json` convention; hook trust remains a host/user approval boundary.

## Design principles

`Compute before Context` → `Route before Load` → `Evidence before Trust` → `Verify before Memory` → `Measure before Claim`.

The marketplace is the distribution layer. Core research, large historical experiments, UI, providers, and optional MCP runtimes remain separate from the hot plugin path.
