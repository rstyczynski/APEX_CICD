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

## BUG-5 — Review R1-M1: seed commands in the current deck

**Item:** PBI-053.3. **Severity:** medium. **Status:** fixed.
Slides 4/10 retained seed/default runner and fixed-tag instructions after the
walkthrough moved to operator LAB repositories. Current commands now define
their terminal variables, pass the same explicit LAB/directory and select the
published tag from step E. Notes and authoring source are synchronized; seed
results are historical. Package/text checks and rendered slide inspection are
recorded in tests/review-1-correction-checks.json. No deployment was repeated.

## BUG-6 — Review R1-M2: misleading reference-test descriptions

**Item:** PBI-053.3. **Severity:** medium. **Status:** fixed.
Current copyable test guidance implied selected-replay or fresh native execution,
although the readers use fixed seed run IDs. Manual, test profile/record,
configuration, implementation and handover now identify reference evidence,
seed environment permissions and the new LAB's separate acceptance evidence.
Static comparison with test source closes this wording defect; old results
remain historical, not rerun claims.

## BUG-7 — Review R1-L2: unrelated errors could pass rejection classification

**Item:** PBI-053.3. **Severity:** low. **Status:** fixed (offline classification).
Matching any stage-rule name without a zero-error summary also accepted an
unrelated error with INFO stage rows. The shared AWK assertion requires a
consistent positive error count, intended ERROR rule and selected path inside
that diagnostic. Workflow/manual/reference-reader semantics agree; schema-2
receipts bind the path/controller and legacy receipt support is explicitly
pinned. The actual corrected assertions pass 21 offline fixture checks. This
does not claim a fresh native workflow run. R1-L1 is a separate approved policy
deferral in the review decisions; no private record was migrated/deleted.
