"""Exercise the sprint launcher without starting Codex or changing sprint state."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin/sprint-finalize.sh"
MOCK = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
if args == ["--broker", "stop"]:
    sys.exit(0)
capture = Path(os.environ["CAPTURE"])
previous = capture.read_text().splitlines() if capture.exists() else []
with capture.open("a") as output:
    output.write(json.dumps({"args": args, "cwd": os.getcwd()}) + "\n")
Path(args[args.index("--state") + 1]).write_text("saved state")
mode = os.environ["MOCK_MODE"]
complete = mode == "retry" and bool(previous)
print("Sprint status: COMPLETE")  # An interim status must never suffice.
if mode != "unmarked":
    print("Sprint result:")
    print("Sprint status: COMPLETE" if complete or mode == "error" else "Sprint status: INCOMPLETE")
sys.exit(130 if mode == "interrupt" else 7 if mode == "error" else 0)
'''


class SprintFinalizeTest(unittest.TestCase):
    def run_launcher(self, mode, *args):
        with tempfile.TemporaryDirectory(prefix="test-sprint-finalize-") as directory:
            root = Path(directory)
            cli = root / "codex-cli"
            cli.write_text(MOCK)
            cli.chmod(0o755)
            capture = root / "calls.jsonl"
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"],
                       CAPTURE=str(capture), MOCK_MODE=mode, TMPDIR=directory)
            result = subprocess.run(["bash", str(SCRIPT), *args], cwd=directory,
                                    env=env, capture_output=True, text=True, timeout=30)
            calls = [json.loads(line) for line in capture.read_text().splitlines()] if capture.exists() else []
            return result, calls

    def test_retry_resumes_checkout_and_preserves_literal_instructions(self):
        literal = 'Keep $(do-not-execute) and `literal text`.'
        result, calls = self.run_launcher("retry", "--sprint", "E.18",
                                          "--extra-prompt", literal,
                                          "--extra-prompt", "Check compatibility.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 2)
        self.assertIn("--new", calls[0]["args"])
        self.assertNotIn("--new", calls[1]["args"])
        states = []
        for call in calls:
            self.assertEqual(call["cwd"], str(ROOT))
            args = call["args"]
            states.append(args[args.index("--state") + 1])
            prompt = args[args.index("--prompt") + 1]
            self.assertIn("Additional instructions for Sprint E.18:", prompt)
            self.assertIn(literal + "\n\nCheck compatibility.", prompt)
            self.assertNotIn("Sprint E.17", prompt)
        self.assertEqual(states[0], states[1])
        master = (ROOT / "etc/sprint-finalize-master.prompt").read_text().rstrip("\n")
        expected = master.replace("${sprint}", "E.18")
        expected += "\n\nAdditional instructions for Sprint E.18:\n" + literal + "\n\nCheck compatibility."
        first_args, retry_args = (call["args"] for call in calls)
        self.assertEqual(first_args[first_args.index("--prompt") + 1], expected)
        retry = (ROOT / "etc/sprint-finalize-retry.prompt").read_text().rstrip("\n")
        retry = retry.replace("${sprint}", "E.18").replace("${rc}", "0").replace("${prompt}", expected)
        self.assertEqual(retry_args[retry_args.index("--prompt") + 1], retry)

    def test_incomplete_unmarked_and_failed_process_exhaust_retries(self):
        for mode in ("incomplete", "unmarked", "error"):
            with self.subTest(mode=mode):
                result, calls = self.run_launcher(mode, "--sprint", "E.18")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(len(calls), 10)

    def test_interruption_is_not_retried(self):
        result, calls = self.run_launcher("interrupt", "--sprint", "E.18")
        self.assertEqual(result.returncode, 130)
        self.assertEqual(len(calls), 1)

    def test_help_and_invalid_arguments_never_launch(self):
        for args, expected in (([], 2), (["--help"], 0), (["--sprint"], 2),
                               (["--extra-prompt", "Check compatibility."], 2),
                               (["--extra-prompt"], 2), (["--unknown"], 2),
                               (["--sprint", ""], 2)):
            with self.subTest(args=args):
                result, calls = self.run_launcher("retry", *args)
                self.assertEqual(result.returncode, expected)
                self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
