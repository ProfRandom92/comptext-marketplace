"""Secret-read classification for CompText Guard."""
import re

SECRET_PATTERNS = (
    r"(?<![a-z0-9_.-])\.env(?:\.[a-z0-9_.-]+)?(?![a-z0-9_.-])",
    r"(?<![a-z0-9_.-])\.(npmrc|pypirc|netrc)(?![a-z0-9_.-])",
    r"(?<![a-z0-9_.-])id_(rsa|ed25519)(?![a-z0-9_.-])",
    r"(?<![a-z0-9_.-])(credentials?|secrets?)(?:\.[a-z0-9_.-]+)?(?![a-z0-9_.-])",
)
READERS = r"\b(cat|type|get-content|gc|more|less|grep|awk|sed|head|tail|jq|yq)\b"
RUNTIMES = r"\b(python3?|node|ruby|perl|pwsh|powershell|bash|zsh|sh)\b"


def secret_reason(command: str) -> str | None:
    lowered = command.lower().replace("\\", "/")
    if re.search(r"(^|[;&|]\s*|\s)(printenv|env)(\s|$)", lowered):
        return "Blocked by CompText Guard: environment reads are not allowed."
    matches_secret = any(re.search(pattern, lowered) for pattern in SECRET_PATTERNS)
    if not matches_secret:
        return None
    shell_source = bool(re.search(r"\bsource\b|(^|[;&|]\s*)\.\s+", lowered))
    runtime_read = bool(re.search(RUNTIMES, lowered))
    direct_read = bool(re.search(READERS, lowered))
    redirected_read = "<" in lowered
    if direct_read or shell_source or runtime_read or redirected_read:
        return "Blocked by CompText Guard: credential or secret-file reads are not allowed."
    return None
