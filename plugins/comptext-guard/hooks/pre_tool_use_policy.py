#!/usr/bin/env python3
"""Small local safety policy for CompText Guard."""
from __future__ import annotations

import json
import sys

from policy_common import command_from, protected_message
from policy_remote import remote_reason
from policy_secret import secret_reason


def deny(reason: str) -> dict:
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}


def warn(message: str) -> dict:
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": message,
    }}


def evaluate(command: str) -> dict | None:
    reason = secret_reason(command) or remote_reason(command)
    if reason:
        return deny(reason)
    message = protected_message(command)
    return warn(message) if message else None


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    command = command_from(event)
    if not command:
        return
    result = evaluate(command)
    if result is not None:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
