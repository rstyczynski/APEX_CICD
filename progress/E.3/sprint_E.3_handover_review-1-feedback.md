# Sprint E.3 technical handover — round 1 reviewer feedback

**Round:** E.3, round 1, original reviewer's reaction to the engineering response, 2026-11-04.

**Revisions:** Original reviewed parent source **b695ec9627f1453220a04032563f812242f7ac0f**; engineering-answer revision **b0e4580a9b099b622dd217694431b71a1070c94f**, repository [rstyczynski/APEX_CICD](https://github.com/rstyczynski/APEX_CICD), branch/ref `main`. Application source remains **fbda57a0cbe4d32961ad826852bd04394a500c11**, public APEX_CICD_E3 tag `v1.0.4`. The maintained checkout at feedback entry was **9987e529caf8b9ad15f05cf536afc6c6baded036**, clean. Its changes after the answer revision are feedback coordination/navigation, including a backlink appended to the response. This assessment uses the answer/report at the requested `b0e4580a...` revision. No implementation patch is included or verified.

**Reviewer:** The original Codex GPT-6-based engineering review agent; exact model build is not exposed. This is reviewer feedback on proposals, not independent human review or runtime validation.

**Scope, checks and exclusions:** Read the complete feedback prompt, pinned engineering response, original report and offline predicate record. Checked Git differences, original report integrity, and the relevant unchanged workflow, test, manual, test-profile, startup and native-log passages. No project script, test suite, SQLcl, deployment or workflow code was executed. No database/browser login, runner/container operation, credential/private-snapshot access, remote mutation, source fix, commit or push occurred. The only project write is this feedback file. This continues the four existing findings; it introduces no new finding or sprint disposition.

**Inputs:** [Feedback prompt](sprint_E.3_handover_review-1-feedback-prompt.md), [original report](sprint_E.3_handover_review-1.md), [engineering response at the answer revision](https://github.com/rstyczynski/APEX_CICD/blob/b0e4580a9b099b622dd217694431b71a1070c94f/progress/E.3/sprint_E.3_handover_review-1-response.md), [offline predicate record](tests/review-1-negative-predicate.json), and the original report's pinned source/evidence inventory. The original report's SHA-256 remains `532cbcc6a732a7b654cc858a4985f417e2ccf500af834825a79695dc0973a57f`.

## Reactions and status

The engineering response addresses the findings constructively and preserves the prototype boundary. I accept its direction, subject to the specific closing clarifications below. The status column preserves the engineering positions; reviewer agreement does not change them to selected, fixed or verified.

| Finding | Reviewer reaction | Current engineering status | Remaining condition |
|---|---|---|---|
| R1-M1 | Accept | agreed | Correct and inspect the deck/notes/source against the current LAB journey. |
| R1-M2 | Accept the documentation-only option | agreed | Identify fixed seed evidence and distinguish new-LAB acceptance consistently. |
| R1-L1 | Accept with clarification | partly-agreed | Record a coherent credential/startup policy; acknowledgment alone does not resolve the contradiction. |
| R1-L2 | Accept with clarification | agreed | Implement and verify specific error classification, path provenance and receipt/log agreement. |

All four remain unresolved. There is no implemented correction in the supplied answer.

## R1-M1 — Presentation commands

The proposed focused correction is sufficient. It addresses the actual mismatch between the deck and walkthrough without expanding E.3. Preserve historical v1.0.4 results, but label them as observations rather than inputs for a new dispatch. The launcher defaults need not be changed to resolve this finding if every current slide command passes the correct explicit arguments.

The closing check must also establish where `e3_repo` and `version_tag` come from in the terminal used for the command. Merely substituting those variable names on a slide is insufficient if that slide still directs the user to a historical setup chapter or omits the current setup reference. The explicit runner directory must agree across setup and run.

Close after a committed deck/notes/authoring-source correction, comparison with walkthrough B/F, and rendered inspection of the changed slides. Preserve unrelated presentation content. No seed deployment, new runner registration or live workflow is needed to validate this documentation correction. I have not inspected a corrected deck because none was supplied.

## R1-M2 — Reference evidence versus a new LAB run

I accept accurate documentation as the smallest sufficient correction. Parameterized replay tests are not mandatory for this bounded prototype. The existing readers can remain useful regression checks of the recorded seed evidence, provided their results cannot be mistaken for acceptance of a new deployment.

The following current claims need qualification at the original source revision:

1. `progress/E.3/user_manual.md:244–249` says access is to the “selected repository” and describes “fresh attributable workflow evidence.” Name the hard-coded seed and distinguish freshly retrieved artifacts from newly executed workflows.
2. `docs/test-profile.md:264–268` says IT-2 consumes a “fresh attributable qualification run.” Identify the fixed reference run selected by the committed journey record. State that the parent command does not dispatch qualification or inject the missing-file defect itself.
3. `progress/E.3/sprint_E.3_tests.md:32–44` offers reproduction commands followed by an older description in which the integration rejection case creates a throwaway clone and live checks require private preservation state. The introductory supersession notice helps, but the currently copyable commands should have a nearby explanation of their present evidence-reader behavior. Preserve the old account as explicitly historical.
4. Wherever configuration/handover guidance describes fresh checks, distinguish the dated engineering execution from what running the parent commands now does. Platform smoke is a current HTTP probe using seed-configured endpoints, whereas IT-1/IT-2 inspect historical runs. Public source visibility does not grant access to seed environment variables.

For a new LAB journey, the instructions should identify the operator's repository, actual source/release PRs, generated tag and resolved source SHA, deployment receipt/archive identity, native logs, separate qualification run if performed, and browser title/history observation. These are already components of the intended journey; the correction needs to connect them explicitly to that journey's acceptance. Passing the seed reader must neither substitute for those observations nor be presented as a prerequisite available to every LAB owner.

Close with a committed documentation reconciliation and static cross-check against the actual test inputs. No new deployment or evidence download is necessary solely to prove this wording correction. Retain the recorded passes as historical results, including their original run identities and artifact-availability limitations.

## R1-L1 — Credential provenance and the scratch boundary

I accept the engineering caution about competing Product Owner directions. My original proposal was a correction option, not authority to remove a requested lookup, invent a secret store, move private files or delete evidence. The response attributes a direct existing-source lookup request to the Product Owner. I acknowledge that reported context; I have not independently inspected the originating conversation and do not reinterpret it as a blanket exception to the standing scratch rule.

The proposed reconciliation boundary is sound, but simply calling the lookup an “acknowledged conflicting legacy accommodation” does not close the finding. It accurately reports an unresolved exception. A reviewer cannot grant the exception, and labeling the file legacy does not make an operational credential dependency disposable.

The minimal coherent supported path is:

1. Start/check the retained VM and containers through the explicit current walkthrough sequence. Document that the inherited VM-start fallback still reads the scratch `containers.conf` override and is outside that supported sequence until corrected; do not describe the fallback as free of local configuration dependencies.
2. Obtain the already assigned Builder, author-schema and application-user credentials through a Product Owner-confirmed authorized source. Keep those identities distinct. GitHub job secrets remain the workflow authority; do not promise that GitHub can reveal their plaintext to supply interactive logins.
3. Create/use the author's native profile outside checkout scratch, and retain the existing temporary job connection mechanism. No new credential store or full lab provisioning is required by this finding.

If assigned credentials are already accessible through a compliant existing source, current instructions can use that path and leave old file lookup examples historical. If the legacy scratch file must remain the current retrieval source, the Product Owner must explicitly choose a narrowly scoped accommodation or authorize a separate remedy. A temporary accommodation should identify the prepared host/use, its dependency and the event that ends it. That would support an explicit **deferral with a trigger**, not verification that the scratch prohibition has been met. No deletion or migration is a closing test.

Close through either a consistent committed supported-path correction or an explicit Product Owner disposition documenting the residual dependency. The reviewer grants neither choice here. The low severity and the accepted prepared-lab prerequisite remain unchanged; this does not require PBI-054 completion.

## R1-L2 — Specific negative classification

I accept the engineering counterexample and proposed direction. In the supplied synthetic log, `Errors: 1` is caused by a version error while both stage-rule rows are INFO. By inspection, that satisfies the current absence-of-zero plus rule-name predicate. The offline record therefore supports the original source-inspected defect. It does not invalidate the actual historical negative log, whose lines 25–29 contain the expected ERROR and missing path. I did not rerun the predicate in this feedback turn.

The proposed positive error count, ERROR-level expected rule and selected missing path are appropriate. Apply them to the same verification result. The expected path must come from the file actually selected for removal; finding an unrelated occurrence elsewhere in a log is not enough. For this lab, support the documented SQLcl table format rather than building a general diagnostic parser.

Formatting handling must preserve the association between the rule's ERROR row and its continuation message/path. Removing ANSI control sequences and trailing padding is reasonable. Unrestricted whitespace removal or independent whole-log string matches can conceal mismatches. Use literal comparison for the selected path, or correctly escape it if a regular expression is used. Inconsistent or incomplete output must not produce a successful rejection receipt.

The proposed new receipt field for the selected path is useful, with one compatibility condition: v1.0.4's historical receipt has no such field. Do not add it retrospectively or infer a new-format pass from its absence. Keep the old evidence explicitly legacy, using its pinned fixture/log context where needed, and require the new field for new-format evidence. Record which controller/workflow revision performs a corrected qualification separately from the application tag being checked; dispatching from a corrected main does not change v1.0.4's application identity.

Sufficient offline evidence for the classification correction consists of running the **actual corrected predicate** on the retained positive/negative logs and bounded synthetic fixtures: unrelated error with INFO stage rows, wrong missing path, incomplete/connection-failure output, and supported ANSI/padding/wrapping variants. Check receipt/path agreement and inspect that the qualification workflow, evidence reader and manual use the same acceptance semantics. A JSON record describing the old predicate's behavior is evidence of the defect, not a test of the correction.

Those checks can establish the parser correction without a database or deployment. They cannot establish a newly successful native qualification workflow. If fresh runtime verification is claimed, a separately authorized qualification run must identify its controller revision, selected application SHA, tool build, removed path, positive/negative native logs, unchanged-target check, receipt and cleanup outcome. No deployment is necessary for that experiment. Preserve the original v1.0.4 evidence and state exactly which level of validation has been completed.

## Outcome and bounded Product Owner choices

The original recommendation remains **corrections required for the bounded handover**, with no new high-severity finding and no reversal of the positive historical architecture evidence. The production deferrals in the original report remain appropriate. Agreement on these proposals is not review closure, sprint acceptance or implementation authority.

The response is specific enough to proceed to Product Owner selection without another clarification round. The remaining choices are to select the focused M1 deck correction, select M2's documentation-only clarification (my recommended sufficient option), select the bounded L2 assertion correction and its validation level, and resolve L1's credential/startup policy as a compliant supported path or an explicit temporary deferral. If the existing credential source cannot satisfy both instructions, that is the particular Product Owner decision still needed; no private values need to be supplied to the reviewer.

After selected corrections are committed, the coordinator should provide their exact revisions and proportionate acceptance evidence for recheck. Until then, preserve the original report and response, keep all four findings unresolved, and make no claim of verified fixes or sprint closure.
