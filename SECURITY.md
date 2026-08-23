# Security Policy

CompText Marketplace is experimental developer tooling. CompText Guard is a bounded policy layer, not a sandbox or a complete security boundary.

## Reporting a security issue

Do not publish live credentials, private repository data, exploit secrets, or sensitive production artifacts in a public issue.

For a public report, use synthetic data and the smallest reproduction that demonstrates the problem. Clearly identify the affected plugin, version, expected policy, and observed behavior.

Security fixes should include a regression test whenever practical. A successful test should demonstrate the intended boundary without weakening unrelated protections.

## Scope

Security-relevant areas include:

- Guard policy bypasses;
- unintended secret or environment reads;
- unsafe remote-write or deploy behavior;
- evidence-freshness bypasses;
- digest/provenance mismatches;
- packaging paths that expose unintended files.
