"""Remote-write classification for CompText Guard."""
import re

BLOCKED_GIT = {"commit", "push", "pull", "merge", "rebase", "tag"}
BLOCKED_GH = {"pr", "issue", "release"}
BLOCKED_DEPLOY = (
    "vercel", "netlify", "wrangler deploy", "fly deploy",
    "railway up", "render deploy",
)
TOKEN_RE = re.compile(r"[^\s;&|()]+")


def tokens(command: str) -> list[str]:
    return [item.strip("\"'").lower() for item in TOKEN_RE.findall(command)]


def blocked_after(items: list[str], marker: str, blocked: set[str]) -> str | None:
    positions = [index for index, item in enumerate(items) if item == marker]
    for index in positions:
        match = next((item for item in items[index + 1:index + 9] if item in blocked), None)
        if match:
            return match
    return None


def remote_reason(command: str) -> str | None:
    items = tokens(command)
    git_verb = blocked_after(items, "git", BLOCKED_GIT)
    if git_verb:
        return f"Blocked by CompText Guard: git {git_verb} requires explicit release scope."
    gh_verb = blocked_after(items, "gh", BLOCKED_GH)
    if gh_verb:
        return f"Blocked by CompText Guard: GitHub {gh_verb} writes require explicit release scope."
    lowered = command.lower().replace("\\", "/")
    if any(item in lowered for item in BLOCKED_DEPLOY):
        return "Blocked by CompText Guard: deploy/release commands require explicit release scope."
    return None
