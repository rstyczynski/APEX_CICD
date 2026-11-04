# Sprint E.3 technical handover — round 1 expert feedback prompt

**Round:** E.3, round 1, outbound request for expert reaction, 2026-11-04.

**Revision:** Original reviewed parent source
`b695ec9627f1453220a04032563f812242f7ac0f`; original application
`fbda57a0cbe4d32961ad826852bd04394a500c11` / v1.0.4. The engineering answer
and original expert report are published at parent commit
**`b0e4580a9b099b622dd217694431b71a1070c94f`**. That revision adds review
artifacts/navigation and an offline predicate-check record, not source fixes.
No uncommitted implementation patch is included. This later feedback-prompt
publication also changes coordination metadata only.

**Reviewer:** The original external reviewer is invited to react; their report
identifies Codex, GPT-6-based review agent, exact model build not exposed.
Engineering respondent: Codex review coordinator.

**Scope:** Same four E.3 findings and proposed closing conditions, assessed
against the bounded Elaboration prototype. Source/evidence inspection only;
no runtime execution, implementation selection or production qualification.

**Inputs:** [Original expert report](sprint_E.3_handover_review-1.md),
[engineering response](sprint_E.3_handover_review-1-response.md),
[offline predicate check](tests/review-1-negative-predicate.json),
[original prompt](sprint_E.3_handover_review-1-prompt.md) and the pinned
source/evidence inventory identified there. Read the response/report from
commit b0e4580a9b099b622dd217694431b71a1070c94f, not an arbitrary later main.

## Engineering positions entering feedback

| Finding | Current engineering status | Proposed action, not a selected fix |
|---|---|---|
| R1-M1 | agreed | Align current PPTX setup/run/dispatch commands with the operator's LAB and selected tag; label seed results historical. |
| R1-M2 | agreed | Prefer accurate reference-evidence documentation over adding selected-replay test parameterization to E.3. |
| R1-L1 | partly-agreed | Resolve contradictory scratch/credential directions with the Product Owner; do not silently remove a requested lookup or migrate private records. |
| R1-L2 | agreed | Require a positive error count, ERROR on the expected rule and the exact selected missing path, with offline negative coverage. |

No finding is fixed or verified. No action is selected, deferred or rejected
on the Product Owner's behalf. The review round remains open.

## Copyable expert instruction

Act as the external reviewer for Sprint E.3, handover review round 1, reacting
to the engineering response. This is a continuation of the same round, not a
fresh review or an implementation/retest request.

Git repository URL: **https://github.com/rstyczynski/APEX_CICD**.
Branch/ref: **main**. Original reviewed parent revision:
**b695ec9627f1453220a04032563f812242f7ac0f**.
Engineering-answer revision:
**b0e4580a9b099b622dd217694431b71a1070c94f**.
The latter full SHA was verified on the published origin/main before this
feedback prompt was prepared. Application source remains
**fbda57a0cbe4d32961ad826852bd04394a500c11** in the tracked bundle and public
APEX_CICD_E3 v1.0.4 snapshot. The answer does not alter that implementation.

Read the original report, engineering response and bounded offline predicate
record at the engineering-answer revision. For each stable ID R1-M1, R1-M2,
R1-L1 and R1-L2, state whether you accept the response, accept with a specific
correction, or dispute it with source/evidence. Assess the proposed acceptance
check and state the remaining closing condition. Preserve the distinction
between agreement on a proposal and verification of implemented behavior.

In particular:

1. For M1, assess whether the proposed focused PPTX/notes/source correction
   resolves the operating-pair mismatch without another seed deployment.
2. For M2, assess whether accurately labeling the fixed seed evidence readers,
   their access requirements and separate new-LAB acceptance is sufficient for
   this bounded handover. Identify exact claims that still need qualification;
   do not assume parameterization is mandatory for this prototype.
3. For L1, address the engineering response's two explicit Product Owner
   directions: direct retrieval from the existing credential source, and no
   persistent configuration/credential authority in scratch. Is the proposed
   reconciliation boundary sound? Distinguish a temporary acknowledged legacy
   accommodation from an actual closing correction; do not grant or infer a
   Product Owner exception. State the minimal coherent supported path and any
   decision still needed, without demanding full fresh-host provisioning or
   requiring deletion/migration of private records.
4. For L2, challenge the proposed error-count/rule/path assertions and their
   formatting/receipt requirements. The offline record confirms the present
   predicate accepts an unrelated-error fixture; it does not invalidate the
   genuine historical missing-file log. State what offline evidence suffices
   for the parser correction and what needs a newly identified native run if
   fresh runtime verification is claimed.

Allowed actions remain read-only inspection of the pinned source, public
artifacts/metadata and recorded evidence. Do not execute project scripts, SQLcl,
deployment or workflow code; connect to the database; operate runners/containers;
modify source/settings/credentials; push; or contact others. Do not request
credentials or private business snapshots. Disclose unavailable inputs and
unrun checks. No new runtime result is expected from this feedback request.

New findings belong to a later review pass. If something new is discovered,
label it a candidate for that pass rather than rewriting this round's scope
or renumbering existing IDs. Neither this exchange nor agreement grants sprint
acceptance, implementation authority or production qualification.

Save the complete Markdown as
**`progress/E.3/sprint_E.3_handover_review-1-feedback.md`**. Use the same subject
base. Begin with subject/round/type, both exact revisions, reviewer identity,
actual scope/checks/exclusions and inputs; then include a per-finding reaction
and status table followed by evidence and remaining closing conditions. End
with any bounded Product Owner choices still needed. Preserve the original
report and engineering response. If file writing is unavailable, return the
complete Markdown for the Product Owner to save at that exact path.
