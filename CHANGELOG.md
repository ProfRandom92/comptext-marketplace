# Changelog

## Initial public release

### Added

- CompText Context 0.1.0 — deterministic operational-context compilation.
- CompText Evidence 0.1.0 — verification-freshness gate for completion claims.
- CompText Guard 0.1.0 — local pre-tool policy for secret reads and remote/release writes.
- CompText Benchmark 0.1.5 — reproducible Raw vs CompText benchmark receipts.
- Compact light/dark marketplace assets for all four plugins.
- Fresh Git-backed installation path through `ProfRandom92/comptext-marketplace`.
- Apache License 2.0 for the standalone marketplace repository.

### Verification

- Four-plugin fresh install from a clean `CODEX_HOME`.
- Runtime smoke checks for Context, Evidence, Guard, and Benchmark.
- Guard regression coverage for chained Git writes and interpreter-based secret reads.
- Byte-for-byte public runtime sync against the verified local source.
