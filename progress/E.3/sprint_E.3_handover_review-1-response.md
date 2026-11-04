# Sprint E.3 technical handover — round 1 engineering response

**Round:** E.3, round 1, engineering response, 2026-11-04.

**Revision:** Original parent source
`b695ec9627f1453220a04032563f812242f7ac0f`; application
`fbda57a0cbe4d32961ad826852bd04394a500c11` / v1.0.4. The maintained parent
baseline at response preparation is
`6e975b93e5e59789a749478be3c90fa840b8d359`, which adds the review prompt and
navigation only. No implementation patch or finding correction is included in
this response. The incoming expert report was untracked at entry and is
published unchanged with this response.

**Reviewer:** Codex, engineering coordinator/respondent. The original external
review identifies a separate Codex GPT-6-based reviewer and explicitly disclaims
independent human peer review and runtime qualification.

**Scope:** Assessment of all four reported findings against the current source,
PPTX text, manual/test guidance and existing native logs. A bounded offline
evaluation of the current negative-log predicate was performed. No application,
workflow, runner or database execution, production qualification or source fix.

**Inputs:** [Original expert report](sprint_E.3_handover_review-1.md),
[issued prompt](sprint_E.3_handover_review-1-prompt.md),
[walkthrough](sprint_E.3_increment_demo.md),
[implementation](sprint_E.3_implementation.md),
[manual](user_manual.md), [test profile](../../docs/test-profile.md),
[test source](../../tests/integration/test_pipeline.sh) and evidence cited below.

## Finding status

These are engineering positions, not Product Owner selections or verified fixes.

| ID | Status | Engineering position |
|---|---|---|
| R1-M1 | agreed | Deck commands still target the seed/default runner; align them with the current LAB journey. |
| R1-M2 | agreed | Current tests read fixed reference evidence, not the selected operator replay. |
| R1-L1 | partly-agreed | Contradiction is real; removing the requested legacy lookup requires reconciling explicit Product Owner directions. |
| R1-L2 | agreed | Current negative predicate can accept an unrelated error with successful stage-rule rows. |

## R1-M1 — Presentation commands target the shared seed

**Facts and evidence.** The actual PPTX slide 4 contains the two launcher calls
without `--repo`/`--directory` and advertises `~/actions-runner-e3`. The
[launcher defaults](../../scripts/e3-runner.sh) select the shared seed unless
overridden. Actual slide 10 contains `--repo rstyczynski/APEX_CICD_E3`, fixed
v1.0.4 and a historical run ID. The corresponding authoring source contains
the same instructions. Current walkthrough B/F instead selects the operator's
LAB and its published tag. This is a present operating-pair inconsistency;
labeling a separate Markdown section historical does not correct the slide.

**Impact.** Agree with the reported risk: an operator can start a listener for
the wrong repository or dispatch the seed instead of the intended LAB. This
does not overturn the recorded seed deployment, but it needs correction for
the current handover.

**Proposed action.** Change slide 4's copyable commands and notes to pass the
selected `e3_repo` and explicit LAB runner directory. Make slide 10's dispatch
use the selected repository and `version_tag`; label the v1.0.4/run observation
as historical rather than presenting it as replay input. Keep the authoring
source, slide map and manual references synchronized. This is a proposal; no
deck or runtime change has been made in this response.

**Acceptance.** Extract the final slide text/notes and establish that each live
setup/run/dispatch command selects the same repository, directory and published
tag as the walkthrough. Render the changed slides, inspect their readability
and preserve unrelated package parts. No seed redeployment is needed.

## R1-M2 — Reference-evidence checks are described as selected-replay checks

**Facts and evidence.** Both functions in
[tests/integration/test_pipeline.sh](../../tests/integration/test_pipeline.sh)
hard-code the seed and consume the committed
[reference journey](tests/github-environment-journey.json). The
[platform smoke](../../tests/smoke/test_platform.sh) also reads settings from
that seed. A new temporary download directory changes neither the selected
run IDs nor the evidence's age. The manual's “selected repository” description
and the test profile's “fresh attributable qualification run” are too broad.

**Impact.** Agree. These readers can confirm the retained reference run's
evidence without validating a newly executed LAB journey. Re-fetching a
historical artifact is a new evidence retrieval, not a new deployment or
qualification experiment. The original logs/receipts remain attributable
historical evidence. The platform check additionally needs authorization to
read seed environment variables, which public source access does not imply.

**Proposed action.** Prefer the reviewer's smaller documentation option for
this bounded prototype: identify these parent commands as fixed reference-run
evidence regression; state the seed, committed journey/run identities and
environment API access requirement. Make replay acceptance explicitly inspect
the selected LAB's actual receipt, native logs and browser observation. Reconcile
the manual, test profile, test record, configuration/handover guidance and current
implementation claims wherever they imply selected-replay validation. Keep
older raw logs as historical evidence. Parameterized selected-replay automated
validation remains a separate design choice, not an unstated capability.

**Acceptance.** A source/document review can distinguish SM-1 static contract
checks, seed-specific IT-1/IT-2 evidence readers, seed-configured platform smoke
and acceptance of a new LAB run. No current instruction treats a passing seed
reader as acceptance of another repository's deployment. If parameterization is
chosen instead, use explicit repository/journey inputs and prove with offline
fixtures that one repository's evidence cannot satisfy another's check.

## R1-L1 — Scratch policy and retained-lab instructions conflict

**Facts and evidence.** Agree with the inconsistency. AGENTS and the manual
categorically prohibit scratch as an environment/credential authority, while
the current manual/walkthrough explicitly reads the retained
`.local-apex/e1-secrets.json` record. The walkthrough already labels it a
legacy lookup and identifies assigned credentials as the alternative on another
host. That labeling does not erase the contradiction with “never.” The inherited
[VM-start helper](../../scripts/apex-vm-start.sh) also supplies a scratch
`containers.conf` override without generating it. The intended walkthrough
starts/checks the VM beforehand; the fallback dependency is still in source.

**Product Owner direction.** The credential lookup is not an accidental
unrequested dependency introduced by an expert: the Product Owner explicitly
asked to retrieve Builder, author-database and LAB_USER passwords from their
existing source rather than requiring an operator to guess or type unavailable
values. The Product Owner also explicitly prohibited using `.local-apex` for
environment settings and defined it as temporary only. Both directions must
be reconciled. The engineering response must not delete the lookup or invent
a new secret store merely because the reviewer proposed it.

**Impact and position.** Partly agreed: accept the documentation/source
inconsistency and need for an explicit supported boundary. Do not treat removal
of the requested lookup as selected, or infer authority to migrate/delete any
private record. The GitHub job itself generates its connections from environment
secrets; the contradiction concerns current local setup/sign-in and inherited
startup behavior. No private credential value was inspected for this response.

**Proposed action.** Ask the reviewer whether a precise current instruction
using already assigned operator credentials, with retained-host lookups clearly
separated and expressly acknowledged as conflicting legacy accommodation, is
an adequate proposed handover disposition. The Product Owner must choose the
credential-source policy before we claim the contradiction resolved. The final
supported path must not require a new hidden store. Preserve private records.
Separately document the startup fallback dependency and bound the present
supported path to explicit VM startup, or select a narrowly scoped helper
correction. Do not claim full PBI-054 infrastructure reproduction.

**Acceptance.** One explicit supported path covers startup, Builder sign-in,
author profile and application sign-in using authorized credentials with a
clear provenance and no persistent configuration authority in scratch. Any
legacy accommodation is reconciled with the Product Owner's standing rule,
not disguised as disposable state. Static checks identify fallback configuration
dependencies accurately; no credential migration/deletion is a closing test.

## R1-L2 — Negative predicate is not specific enough

**Facts and evidence.** The
[qualification workflow](../../examples/git-pipeline/.github/workflows/qualification.yml)
and parent IT-2 reader reject an `Errors: 0` summary and require either native
stage rule name anywhere. Both rule names occur in successful INFO output.
The [retained negative log](tests/github-native-rejection.log) genuinely contains
an ERROR for `stagechangelogfilesvalid` and the missing path; it is not a false
positive. The [manual exercise](sprint_E.3_increment_demo.md#first-demonstrate-the-native-check-manually)
already requires an ERROR on the expected rule, but does not yet assert all
three proposed conditions: positive error count, expected rule and selected path.

**Bounded check performed.** Evaluating the current predicate against retained
logs accepts the actual missing-file log and rejects the positive log. A
synthetic log with `Errors: 1`, a version error and successful INFO stage rows
is also accepted. A synthetic connection failure with no rule names is rejected.
This demonstrates the predicate's classification defect offline; it is not a
reproduced SQLcl runtime failure or evidence that the historical qualification
misclassified its actual result.
The [offline check record](tests/review-1-negative-predicate.json) preserves the
input identities, synthetic strings and observed classifications.

**Proposed action.** Align the qualification step, parent evidence reader and
manual exercise to require an explicit positive error summary, ERROR on the
intended missing-file rule and the exact selected missing path. Normalize ANSI
formatting and line wrapping consistently. Record the selected path in the
qualification receipt so an evidence reader can check the same assertion rather
than guessing the file. Validate receipt/log agreement and reject unrelated or
incomplete diagnostics. Update the parent example and qualified application
source together through a reviewed revision; never rewrite v1.0.4 or retrofit
its historical receipt with a claim from a later check.

**Acceptance.** Offline fixtures accept the real missing-file diagnostic,
including supported formatting, and reject zero-error output, unrelated errors
with INFO stage rows, a different missing path and incomplete/connection-failure
logs. A newly selected runtime qualification must record the corrected source
and receipt identity if used to claim fresh native verification; offline parsing
tests alone must not be called an independent native run.

## Proposed next decisions and closing conditions

Keep all four findings open for the Product Owner's disposition; the status table
records engineering agreement, not implementation selection. Recommend selecting
the bounded M1 presentation correction, M2 documentation clarification and L2
specific-result assertion. For L1, reconcile the two explicit credential-source
directions rather than unilaterally removing an instruction or creating a store.
No wider sprint scope or backlog assignment follows from these proposals.

The report's positive historical evidence and its production deferrals are
consistent with the bounded objective. Preserve the distinction between
recorded reference success, present reproducibility, independent review and
production readiness. No finding is fixed or verified by this response.

## Checks performed

Read the original report and compared its revision with the issued prompt and
current Git baseline. Its original bytes have SHA-256
`532cbcc6a732a7b654cc858a4985f417e2ccf500af834825a79695dc0973a57f` and are
preserved unchanged. Inspected the actual PPTX slide-4/10 XML text, matching
authoring source, launcher defaults, manual, test profile, platform/integration
test source, qualification source, VM-start dependency and retained native logs.
Evaluated the current log predicate on the two retained logs and two explicitly
synthetic strings as described above. No repository test suite, reviewed project
script, SQLcl command, deployment, workflow dispatch, browser login or container/
runner operation was executed. No source fixes, credential lookup, private
snapshot inspection, production validation or reviewer-contact action occurred.

The next exchange asks the expert to challenge these positions and closing
conditions. Selection, implementation, runtime revalidation and sprint acceptance
remain distinct later steps.
