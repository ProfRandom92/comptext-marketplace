# Contributing to CompText Marketplace

Contributions are welcome when they keep the plugins small, testable, and evidence-driven.

## Before opening a pull request

- Keep each plugin focused on one responsibility.
- Add or update a regression test for behavior changes.
- Keep large assets, research notes, and generated artifacts out of the runtime path.
- Preserve failure evidence instead of converting it into a successful claim.
- Treat benchmark numbers as results for exact fixtures and execution conditions, not universal claims.
- Do not include credentials, private prompts, production secrets, or unrelated source data in fixtures.

## Pull requests

A useful pull request should explain:

1. the problem being solved;
2. the smallest behavior change required;
3. how the change was verified;
4. whether it changes context cost, security policy, evidence semantics, or benchmark interpretation.

Prefer focused changes over cross-plugin coupling. Context, evidence, guard policy, and benchmarking should remain independently understandable.

## License of contributions

Unless explicitly stated otherwise, contributions intentionally submitted to this repository are licensed under the **Apache License 2.0**, consistent with the repository license.
