# E.3 — Corrected implementation findings

Current correction — 2026-11-03: the Product Owner required native APEX/SQLcl
and GitHub Actions control, with all E.3 Python removed. The
[native correction record](sprint_E.3_native_correction.md) supersedes the earlier
1.0.1 implementation described below. Historical evidence is retained.

## BUG-1 — Native stage branch path

PBI-053.1; fixed. Slash-containing stage branch names produced native source/dist
verification errors. An explicit slashless demo branch convention corrected the
issue; zero-error native verification followed. This is not a generic tool fix.

## BUG-2 — Native mapping property lookup

PBI-053.1; fixed. The artifact excludes repository-level utils, so deployment
could not find the relative defaults file. The thin installer now passes the
committed file's absolute checkout path. Retry installed the scoped baseline.

## BUG-3 — Inherited runtime controller hook

PBI-053.1; fixed for this prototype. The source contained E1_CTRL's runtime
assertion, which is not installed in the native target. PR 3 introduced an
explicit, reviewed pre-stage source adapter to LAB_RUNTIME.assert_ready. Native
verification and browser login then passed. General production fencing remains
separate backlog work.

## BUG-4 — Detached release checkout

PBI-053.3; fixed. Remote run 41664285664 stopped during native verification on a
detached HEAD. PR 4 attaches the same selected tag commit to a local named build
branch. Run 41664798289 passed without moving the tag. See
[test evidence](sprint_E.3_tests.md) and [implementation](sprint_E.3_implementation.md).
