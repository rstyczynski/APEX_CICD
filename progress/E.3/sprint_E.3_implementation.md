# E.3 — Implementation record

Current correction — 2026-11-03: the Product Owner required native APEX/SQLcl
and GitHub Actions control, with all E.3 Python removed. The
[native correction record](sprint_E.3_native_correction.md) supersedes the earlier
1.0.1 implementation described below. Historical evidence is retained.

The Product Owner authorized implementation through handover without further
questions on 2026-11-03. The [accepted design](sprint_E.3_design.md) and its
three child outcomes govern the prototype. [PLAN](../../PLAN.md) owns status;
[tests](sprint_E.3_tests.md) will own actual outcomes. This record is updated as
execution completes, not a claim of production readiness.

## PBI-053.1 — Capture and native baseline

Created the private application repository
[APEX_CICD_E3](https://github.com/rstyczynski/APEX_CICD_E3), a schema/workspace
E3_TARGET and application 810203. Retained E1_UAT and earlier sprint files remain
untouched. APEX Main is E1_DEV_C/810003. New Working Copy 100, “E3 heading patch”,
changed one Home region heading. Native browser comparison found one changed
page; it was selectively merged into Main with a target backup. Native PROJECT
export captured the result into the application Git repository.

SQLcl 25.4.1.022.0618 verifies consistent source/distribution with zero errors.
The slash-containing branch issue still appears during native source/dist
comparison; explicit slashless e3-initial/e3-heading/e3-runtime-correction branches
are used in this separate demo repository. The parent project retains its
normal branch conventions. The original failing stage output stays private.

Initial deployment exposed a mapping lookup failure because the generated
archive excludes repository-level utils. The thin installer now supplies the
absolute defaults-file path computed from its checked-out repository; the file
is committed, contains no secrets and is selected from the same source revision.
The first attempt rolled back before application installation. A retry installed
the baseline and a real greeting/history row was then added in the disposable
schema for preservation verification.

Browser validation exposed a retained E1_CTRL session hook unavailable on the
new target. A second patch PR replaces it in reviewed source with the existing
LAB_RUNTIME.assert_ready before native staging. The explicit capture adapter
performs this bounded conversion of SQL/readable source after export and before
review/stage; no post-stage archive patching occurs. Native verification passes.
The original author application/control packages and retained UAT are not changed
by that conversion. This is a documented prototype adapter, not general removal
of E.1 fencing/ownership guarantees.

## PBI-053.2 — GitHub integration and version preparation

The three workflows and thin scripts are versioned in
[examples/git-pipeline](../../examples/git-pipeline/), with a baseline Git bundle
and [preparation script](user_manual.md#prepared-laboratory) preserving source provenance.
PR checks validate exactly one patch/minor/major label against the Conventional
Commit title, run source/shell checks and actionlint. Squash merge retains that
title. Release Please generates the version/changelog release PR; both that
record and GitHub Release notes use the same history. Its bot PR is explicitly
checked through manual hosted dispatch, accounting for GITHUB_TOKEN event
suppression. Deployment has no PR/push/tag/release event trigger.

Change PR 1 introduced the heading. PR 3 contains the bounded runtime adapter;
both are patch fixes accumulated into release PR 2 for 1.0.1. The sequential
review/merge roles are exercised by Codex under the Product Owner's instruction;
this is not an independent human peer-review claim.

## PBI-053.3 — Manual deployment and handover

A dedicated runner, e3-lab-mac, is registered only to the private demo repository.
The official runner archive SHA-256 was checked before extraction. Registration
required running outside the filesystem sandbox after .NET initialization failed.
No OS service was installed. PR/version jobs run on hosted runners; only the
manually dispatched lab deployment uses this local runner and private connection
configuration. [Runner entry point](user_manual.md#manual-deployment-and-runner) starts it for
future use. Run results, evidence and final limitations belong in the test and
handover records as they become available.

The first manual 1.0.1 run (41664285664) failed before deployment because native
PROJECT cannot verify detached HEAD. PR 4 corrects the main workflow to attach
the exact selected tag commit to a local e3-release-build branch. It does not
retag or modify application version 1.0.1. The deployment workflow is read from
accepted main while application bytes come from the selected version tag; run
history preserves both revisions. The second dispatch uses the same 1.0.1 app
version with that corrected workflow. Later Release Please proposals need not
be published or deployed for this experiment.

## Delivered verification and retention

The second manual run 41664798289 passed, binding version v1.0.1 to source
2e203ba571bbce9fd30cafc5531e36250d5594b2 and the downloaded native ZIP hash.
The deployed browser heading and existing greeting/history were inspected.
All required new-code and smoke regression gates passed. A further isolated
source-clone rehearsal ran the reusable capture.sh adapter, stage and native
verify successfully, without deployment. [Its receipt](tests/capture-rehearsal.json)
records scope. The source bundle now preserves final accepted main, both tags
and comparison history, with [identity](tests/bundle.json).

Retain the small example and scripts as a reference architecture prototype;
do not promote them to a production service without the registered additional
proofs. The [walkthrough](sprint_E.3_increment_demo.md), [manual](user_manual.md)
and [handover](sprint_E.3_handover.md) are the user-facing delivery set.
