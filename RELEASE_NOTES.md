# CompText Marketplace v0.1.0

Initial public release of the standalone CompText Marketplace.

## Included plugins

- **CompText Context 0.1.0** — deterministic operational-context compilation from explicit requirements.
- **CompText Evidence 0.1.0** — verification-freshness checks after successful workspace mutations.
- **CompText Guard 0.1.0** — bounded local pre-tool policy for secret reads and remote/release/deploy writes.
- **CompText Benchmark 0.1.5** — reproducible Raw vs CompText benchmark receipts with quality and efficiency reported separately.

## Install

```bash
codex plugin marketplace add ProfRandom92/comptext-marketplace
codex plugin add comptext-context@comptext-marketplace
codex plugin add comptext-evidence@comptext-marketplace
codex plugin add comptext-guard@comptext-marketplace
codex plugin add comptext-benchmark@comptext-marketplace
```

## Verification for this release candidate

- 49 public runtime files matched the verified local source byte-for-byte.
- Fresh Git-backed installation discovered and enabled all four plugins.
- CompText Guard regression suite: 4/4 passed.
- Marketplace plugin integration tests: 2/2 passed.
- Benchmark Lab: 19/19 passed.
- Plugin Eval: 95/100 (A) for all four plugins.
- Current plugin validator: 4/4 passed.
- Deterministic package rebuilds produced matching SHA-256 per plugin.

Package SHA-256 values:

```text
comptext-benchmark  aa71b42dc023b0b88f01373730490f0eb421ae3cda063cdbc7815cf06f164d79
comptext-evidence   653ade32a40004dd7f749d3bebc1f8fc26906ee8cbbd86bac17c5eb3829fc479
comptext-context    cabe9c9f623ca368f7a0c3438ab57eb96f4012328a77ebee3c329931161e6a42
comptext-guard      cebe3f6d0d7ecb3b44ad1ee4bda8d3b050b5932501ce9703844d3ee23fbe84fd
```

## Scope

CompText remains experimental developer tooling. Guard decisions are bounded policy decisions rather than a sandbox or proof of security. Benchmark numbers apply to the exact fixtures and execution conditions that produced them; the bundled 58% token-reduction result is not a universal performance claim.
