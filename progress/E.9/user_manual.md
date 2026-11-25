# E.9 local prototype manual

The [walkthrough](sprint_E.9_increment_demo.md) explains the journey and
[implementation](sprint_E.9_implementation.md) defines its trust limits.
Python 3 and Git must be on PATH. Run from a clone with the `code` command
available for inspection. No credentials, database mutation or remote push occurs.

The lab driver creates a temporary repository, commits a greeting and assertion,
retains actual diffs, executes the assertion, validates the retained Codex report,
and performs a controller-authorized local merge. It preserves a bundle and JSON
records under progress/E.9/tests, then removes only its temporary directory.
Each rerun replaces current journey/summary records and retains hashed reports.
Do not treat earlier receipts as authorization for another candidate.

```bash
cd "$(git rev-parse --show-toplevel)"
python3 tests/review_lab.py
code progress/E.9/tests/journey.json
code progress/E.9/tests/refreshed.diff
```

The unit runner exercises synthetic rejection cases independently of Git. A
passing result verifies policy logic; it does not authenticate the injected users.

```bash
python3 tests/test_review.py
```

On failure, retain the traceback, inspect it with the current diff, correct the
cause and rerun. Never replace missing evidence with success. Unchanged blank
input and non-string behavior are explicit limitations of the greeting fixture.
There is no supported production merge command. Hosted protection verification
and atomic integration remain pending.
