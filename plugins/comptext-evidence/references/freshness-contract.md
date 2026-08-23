# Evidence freshness contract

The gate is intentionally narrower than semantic verification.

- `mutation(success=true)` marks verification pending.
- `mutation(success=false)` does not invalidate fresh evidence.
- `verification(success=true)` clears pending state for the current repository state.
- Failed or missing verification never clears pending state.
- A later successful mutation invalidates earlier verification for completion purposes.
- `completion_claim` is observational only; assertion cannot clear the gate.
- Trace records are content-free metadata and receive a SHA-256 digest.

This contract is compatible with the documented Riqor evidence-gate semantics but is an independent CompText reference implementation for deterministic benchmarking.
