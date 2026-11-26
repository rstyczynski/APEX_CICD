# E.15 implementation

## Delivered boundary and source

[Design](sprint_E.15_design.md) owns the accepted mechanism, [checklist](sprint_E.15_checklist.md) owns requirement traceability and [verification](sprint_E.15_tests.md) owns actual results. The [manual](user_manual.md) and [walkthrough](sprint_E.15_increment_demo.md) provide prerequisites, complete SQL, staged commands, expected outputs and recovery.

Candidate PRs and SQL live in the explicitly authorized standalone APEX_CICD_E.15-candidates repository with Actions disabled. Trusted Oracle workflow, Review and the local operator controller live in APEX_CICD_E.15. The self-fork API returned the original non-fork repository, so a standalone companion implements the same authorized separation purpose without inventing a fork network.

Qualified core source is f98403720cd8c6fa49cba9a019590c08767db648, tag e15-qualified. The mirrored controller and workflow are in [sprint-work/E.15](../../sprint-work/E.15). Later commit 3f76037 adds a separate publication-authority probe and current guidance; validator/controller/Review core files remain byte-identical to the qualified tag. A fresh tagged clone and CLI help were checked. Git bundles preserve validator and candidate history independently of disposable checkouts.

## Runtime and authority

The trusted dispatcher accepts a numeric companion PR ID, obtains immutable candidate source as data, checks changed paths and exact trusted Review, and executes actual Oracle assertions through oracledb. Oracle uses a pinned disposable image, application user and loopback-only service port. SYSDBA is used only to initialize the private sentinel inside that service. Candidate SQL receives no operator credential and is never executed as runner shell.

The Python/GitHub CLI controller checks candidate Actions disabled, current head/base, trusted policy commit, approved SQL digest, correlation and actual job provenance. It publishes pending before execution and failure on rejection/cancellation. Success requires actual terminal Oracle/Review success and a fresh state recheck. Existing receipts are revalidated, not trusted as assertions. Ordinary merge revalidates again and uses --match-head-commit without --admin.

Only the configured trusted owner has target write access; no other human writer is provisioned in this fixture. A real read-only hosted principal's cross-repository publication attempt received HTTP 403. The candidate-owned dispatch allocated no jobs under disabled Actions. This qualifies the chosen candidate-code boundary, not organization-wide IAM or hostile administrator resistance. The local trusted operator is explicit; no autonomous hosted publisher or independent human identity is invented.

## Actual journey, negative cases and recovery

Companion PR 1 passed real Oracle Testing, exact Review and ordinary protected merge after recovery, commit 640bee9f260b52a85a212183fbc1c1938c696473. The full live replay, PR 3, merged at 2d5a94a55fef741f052a061ee06470439624e3e8. Both source and run identities are retained. Fixture baseline preparation used a forward-only owner maintenance commit with temporary administrator exemption and immediate restoration; neither candidate acceptance merge used that exemption.

Actual invalid paths were refused: stale base despite prior green head evidence, changed-head receipt, changed SQL Review digest, and another candidate's successful real run substituted into the current receipt. Native merge was refused in each case. Both Oracle services were observed after assertions in Inspection interval; cancelling A removed its own container/network, B completed successfully, A published failure and native merge was refused. A fresh A run then recovered and merged. The earlier image-download interruption is retained as narrower network-cleanup evidence.

## Failures, repairs and decisions

The original same-repository workflow authority failed: candidate code obtained same-app check publication and cross-run cancellation authority. Code-owner approval mitigated invalid merge but not run interference. The authorized companion boundary replaced that approach. The original failed evidence remains unchanged in meaning.

Recovered implementation defects include YAML header parsing, trusted report checkout and the hosted checker assuming exactly one dispatch job. The corrected checker explicitly requires Oracle success and allows the documented skipped PR-only publisher. New gates pass 1/1 smoke, 2/2 unit and 1/1 integration; full regression passes 14/14 smoke, 16/16 unit and 24/24 integration. Receipt unit cases are labelled contract checks and do not substitute for actual GitHub/Oracle cases.

GitHub retained a zero-job disabled dispatch metadata record that cancel/force-cancel/delete APIs could not remove. No runner/container or runtime token was allocated. This is a platform metadata limit, not a leaked Oracle workload. Actual active-service cleanup is independently evidenced.

The trusted operator and real Oracle image/driver are the declared experiment dependencies. No SQLcl PROJECT metadata or approved tool release was changed. Historical regression checks qualified SQLcl 25.3.0.274.1210 before native target preparation. Native release provenance, independent clean-host reproduction and capacity measurement remain later assigned work; this implementation does not claim their acceptance.
