# E.3 — Native inheritance correction

The Product Owner explicitly required removal of E.3 Python and use of native
APEX tools with GitHub Actions as controller on 2026-11-03. This corrects the
initial handover and supersedes its recurring source adapter. The
[accepted design refinement](sprint_E.3_design.md#product-owner-correction--native-tools-and-github-control),
[walkthrough](sprint_E.3_increment_demo.md), [manual](user_manual.md),
[handover](sprint_E.3_handover.md), [architecture](../../docs/architecture.md) and
[test profile](../../docs/test-profile.md) form the maintained delivery set.
Historical 1.0.1 logs/receipts remain attributable to their original code.

## Why correction was necessary

E.2 adapted its native deployment candidate, leaving authoring Main 810003 with
E1's initialization hook. Initial E.3 recaptured that author and replaced the
hook on each capture. That repeated adaptation instead of establishing the
native authoring baseline once. Python also obscured the native operations in
the demonstration. The Product Owner rejected that implementation direction.

Main's initialization setting was changed through App Builder. The first edit
left whitespace because Tab indented the native editor instead of moving focus.
The 1.0.2 workflow succeeded, but the browser failed at initialization. This is
**failed runtime evidence**, not a successful handover. Native
APEX_SESSION.CREATE_SESSION reproduced the same error; its
[log](tests/native-session-rejection-1.0.2.log) and
[browser capture](tests/native-login-failure-1.0.2.png) are retained.

The editor was cleared again and saved without Tab. Native export now omits
the initialization property entirely in both SQL and readable source. The
[final saved native screen](tests/native-author-baseline.png) shows the empty
field. Native stage and verify passed with zero errors/warnings. No export
rewrite or archive edit was used. Old Working Copies must refresh the changed
application definition from Main before later merges; retained UAT and the
historical E.2 evidence remain unchanged.

## Implemented boundary

Removed E.3's lab.py, check_pr.py, e3-prepare.py, e3-runner.py, e3-evidence.py,
Python-based tests and shell capture/check/release wrappers. Removed their
compiled caches and obsolete private rehearsal/runner source copies. Existing
E.1/E.2 code and the adopted delivery method are outside this correction.
Git history retains the retired implementation; it is not executable current
source. The complete native source/distribution history remains bundled.

The [example](../../examples/git-pipeline/README.md) contains workflow YAML,
SQL files, jq PR metadata policy and Release Please configuration. SQLcl PROJECT
owns export/stage/verify/gen-artifact/deploy. GitHub Actions owns ordering,
version-tag selection, required output checks, preservation comparison and
receipt creation. There is no standalone release controller. Native APEX
availability restricts/publishes the app. LAB_RUNTIME remains inherited business
readiness, with no application initialization dependency on either controller.

Native acceptance SQL now creates/deletes an APEX session before publication.
[Oracle documents](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/CREATE_SESSION-Procedure.html)
that CREATE_SESSION runs application initialization. This directly checks the
failure observed in 1.0.2, without adding an authentication or migration engine.
Actual browser authentication/heading/history validation remains separate.

GitHub control SQL comes from accepted main; tagged application source and
mapping configuration use a separate checkout. Verification precedes all target
writes and explicitly requires Errors: 0, because native verification can return
process success with reported errors. The selected tag uses a named build branch
as required by the pinned client. No DEV export runs during release.

## Evidence and completion

[PR6](https://github.com/rstyczynski/APEX_CICD_E3/pull/6) removed the controllers;
[PR7](https://github.com/rstyczynski/APEX_CICD_E3/pull/7) completed native initialization
and session validation. Both patch PRs passed hosted checks and were reviewed
and squash merged. [Release PR8](https://github.com/rstyczynski/APEX_CICD_E3/pull/8)
changed only the version, changelog and release manifest. Its latest head passed
[hosted check 41673185644](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41673185644).

[Published v1.0.3](https://github.com/rstyczynski/APEX_CICD_E3/releases/tag/v1.0.3)
resolves to 4f378fbb5bc620070df0001847b905b03e235a7b. The explicitly dispatched
[native workflow 41673394174](https://github.com/rstyczynski/APEX_CICD_E3/actions/runs/41673394174)
passed all steps, including native APEX session initialization before publication.
The [receipt](tests/native-release-receipt.json) binds the selected source and ZIP
SHA-256 230461368c1ec085b7e9cea442f13e23f23b157966626d2614a757ba05b15acf.
The selected tag and accepted control main currently identify the same commit;
the workflow still records them as separate checkouts. No older tag was moved.

Fresh A1 smoke passed 1/1; A3 integration passed 2/2; B1 full smoke regression
passed 2/2. [A1](tests/native-A1-smoke.log), [A3](tests/native-A3-integration.log)
and [B1](tests/native-B1-smoke.log) are the final correction gate logs. No unit or
broader regression was selected. IT-1 re-queries live PR/run/release state,
verifies the downloaded ZIP hash, both changelogs and all seven business tables
against the private pre-correction baseline. It requires the selected tag to
contain no Python files. IT-2 uses real native verification on an included
changeset removed in a disposable clone, requires rejection and confirms no
target change. Its [native log](tests/native-only-rejection.log) and
[receipt](tests/native-only-rejection.json) record the failure gate; no deploy
command is called. [Native source verification](tests/native-only-verify.log)
reported zero errors/warnings. Original raw native logs remain private;
readable public copies normalize only console coloring/trailing padding.

Real browser sign-in as LAB_USER now succeeds, with the expected heading and
the original Hello World history row. [Observation](tests/native-browser.json),
[Home](tests/native-deployed-home.png) and [history](tests/native-deployed-history.png)
record the final run. No greeting was inserted during these checks. The original
preservation baseline is unchanged. The 1.0.2 workflow success remains historical;
its failed browser result was corrected, not counted as final acceptance.

The regenerated native [bundle identity](tests/native-bundle.json) covers current
main and tags 1.0.0–1.0.3. All current example/SQL files agree with accepted main.
The [deck check](tests/native-presentation-checks.json) records the final 12-slide
package/layout/import checks and individual visual inspection. Native PowerPoint
execution was not claimed. SQLcl connections/private runner files remain local;
this correction uses the prepared lab and does not deliver independent clean
checkout provisioning.

## Limits retained

This is the same bounded Elaboration happy path. Native import can restore source
availability during import; the workflow reapplies restriction immediately
afterward. This does not provide atomic maintenance fencing, active-request
quiescence, drift/identity coverage or general DDL recovery. A later required
failure stops subsequent steps and needs operator inspection, not an invented
rollback claim. Native session creation does not test password authentication.
The inherited footer is still 1.0.0; repository release versions remain separate.
No new backlog scope, next sprint activation or Product Owner acceptance is
inferred by correcting the implementation.
