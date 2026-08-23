"""Shared bounded metadata helpers for CompText Guard."""

PROTECTED = (
    "README.md",
    "SECURITY.md",
    ".github/workflows/",
    ".codex/",
    ".agents/",
)


def command_from(event: object) -> str:
    if not isinstance(event, dict):
        return ""
    tool_input = event.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return ""
    value = tool_input.get("command") or tool_input.get("cmd") or ""
    return value if isinstance(value, str) else ""


def protected_message(command: str) -> str | None:
    lowered = command.lower().replace("\\", "/")
    touched = [item for item in PROTECTED if item.lower() in lowered]
    if not touched:
        return None
    joined = ", ".join(touched)
    return (
        "Protected path mentioned; verify authorization and validation "
        f"before completion: {joined}"
    )
