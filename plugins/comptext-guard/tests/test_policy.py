import json
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "hooks" / "pre_tool_use_policy.py"


def run(command: str):
    event = json.dumps({"tool_input": {"command": command}, "cwd": "/tmp/repo"})
    proc = subprocess.run(
        ["python3", str(SCRIPT)], input=event, text=True,
        capture_output=True, check=True,
    )
    return json.loads(proc.stdout) if proc.stdout.strip() else None


class GuardPolicyTest(unittest.TestCase):
    def test_allows_read_only_git(self):
        self.assertIsNone(run("git status"))

    def test_blocks_secret_read(self):
        out = run("cat .env")
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")


class GuardBypassTests(unittest.TestCase):
    def test_blocks_chained_and_git_option_remote_writes(self):
        for command in (
            "echo ok && git push origin main",
            "git -C . push origin main",
            "printf ok; gh pr create --title x",
        ):
            out = run(command)
            self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_blocks_shell_and_runtime_secret_reads(self):
        for command in (
            "source .env",
            "python3 -c \"print(open('.env').read())\"",
            "node -e \"require('fs').readFileSync('.npmrc')\"",
        ):
            out = run(command)
            self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
