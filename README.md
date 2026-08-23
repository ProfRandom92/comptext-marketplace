# CompText Marketplace

CompText is a small collection of Codex plugins built around one idea: **compute before context**.

Instead of pushing more raw material into an agent, the plugins focus on compact operational context, verifiable evidence, bounded safety policy, and reproducible measurement.

## Plugins

| Plugin | Purpose |
| --- | --- |
| **CompText Context** | Compile explicit requirements into a minimal, deterministic operational context. |
| **CompText Evidence** | Check whether verification evidence is still fresh after the latest successful mutation. |
| **CompText Guard** | Apply local pre-tool policy for secret reads, remote writes, releases, and deploy actions. |
| **CompText Benchmark** | Compare Raw vs CompText workflows while keeping quality and efficiency separate. |

## Install

```bash
codex plugin marketplace add ProfRandom92/comptext-marketplace

codex plugin add comptext-context@comptext-marketplace
codex plugin add comptext-evidence@comptext-marketplace
codex plugin add comptext-guard@comptext-marketplace
codex plugin add comptext-benchmark@comptext-marketplace
```

Check the installation with:

```bash
codex plugin list --json
```

The marketplace is designed to work with a non-default `CODEX_HOME` as well. Script-backed skills resolve `${CODEX_HOME:-$HOME/.codex}`.

## Quick start

### Context

Use `CompText Context` when a task has explicit requirements, dependencies, blockers, ordering, or recovery paths and you want to load only the operational information that is actually required.

Example intent:

```text
Compile the minimum context required for this task and show any missing required fields.
```

### Evidence

Use `CompText Evidence` after repository mutations when a completion claim depends on verification performed against the current state.

Example intent:

```text
Is the available verification evidence still fresh after the latest successful mutation?
```

### Guard

`CompText Guard` ships a local `PreToolUse` hook. It blocks selected secret/environment reads and unscoped Git, GitHub, release, and deployment writes, while warning on protected repository-control paths.

Read-only operations such as `git status`, `git diff`, and `git log` remain allowed by the default policy.

Guard decisions are **policy decisions, not a sandbox or a proof of security**. Review and trust hook code before enabling it in an environment you care about.

### Benchmark

Use `CompText Benchmark` to measure Raw and CompText paths under the same frozen experiment conditions.

The bundled deterministic smoke fixture currently reports Raw `1000` vs CompText `420` input/effective-context tokens — a **58% reduction in that fixture** with no recorded fixture quality regression. This is a reproducible smoke result, not a universal performance claim.

## Design principles

```text
Compute before Context
Route before Load
Evidence before Trust
Verify before Memory
Measure before Claim
```

The plugins deliberately remain narrow. Large research experiments, historical prototypes, provider adapters, UIs, and optional runtimes do not belong in the hot plugin path.

## Verification

The current release process checks:

- current OpenAI plugin validation for all four plugins;
- Plugin Eval for packaging and context cost;
- deterministic context/evidence receipts;
- Benchmark Lab regression tests;
- Guard policy regression tests, including chained Git writes and interpreter-based secret reads;
- clean installation from a fresh `CODEX_HOME` using this Git repository as the marketplace source.

Release claims should always be tied to the exact tagged revision and its verification output.

## Privacy and scope

The four plugins are local developer/research plugins and do not operate a CompText-hosted telemetry service. Each plugin includes its own `PRIVACY.md` and `TERMS.md`.

Do not put credentials, secret values, private prompts, or unnecessary raw source content into CompText fixtures or evidence traces.

## License

CompText Marketplace is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

## Contributing

Issues and focused pull requests are welcome. Good contributions are small, testable, and preserve the separation between context, evidence, policy, and benchmarking.

Before proposing a change:

1. keep plugin behavior narrow;
2. add or update a regression test for behavior changes;
3. avoid adding large assets or documentation to the runtime path when they can remain deferred;
4. do not turn fixture numbers into general performance claims;
5. preserve failed checks and regressions instead of rewriting them into success.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution expectations and [`SECURITY.md`](SECURITY.md) for security reporting guidance.

For security-sensitive findings, avoid publishing secrets or live credentials in an issue. Prefer a minimal reproduction against synthetic data.

## Status

This repository is the canonical public distribution source for the CompText Marketplace. The initial public release contains:

- `comptext-context` `0.1.0`
- `comptext-evidence` `0.1.0`
- `comptext-guard` `0.1.0`
- `comptext-benchmark` `0.1.5`

CompText remains experimental developer tooling. Treat receipts and benchmark outputs as evidence for the exact inputs and execution conditions that produced them.
