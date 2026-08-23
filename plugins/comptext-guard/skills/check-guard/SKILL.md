---
name: check-guard
description: Use when the user asks why CompText Guard blocked or warned on a repository action, or whether a planned shell action falls inside the current local policy.
---

# Check CompText Guard

Explain the active local hook policy; do not bypass it.

The default v0.1 policy blocks direct secret/environment reads, unscoped Git history-changing operations, GitHub PR/issue/release writes, and common deploy/release commands. It warns when protected repository-control paths are mentioned.

Read-only Git operations such as `git status`, `git diff`, and `git log` remain allowed.

If the user explicitly authorizes a release or remote-write scope, report that the default hook still blocks it until the policy profile itself is changed; do not silently disable or edit the hook.

Treat hook output as policy evidence, not proof that an action is otherwise safe.