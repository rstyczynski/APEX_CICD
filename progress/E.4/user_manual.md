# E.4 — Operating manual

## Supported work

Use this prepared-host prototype to understand independent APEX authoring with SQLcl
PROJECT, later release announcement, developer opt-in, separate manager admission,
A/C integration and B deferral, and deliberate central DEV upgrade/repeat. The
[complete walkthrough](sprint_E.4_increment_demo.md) is the operating sequence and
contains full helper SQL before invocation. The [presentation](sprint_E.4_increment_demo.pptx)
uses the same stage map. [Implementation](sprint_E.4_implementation.md) owns actual
provenance; [tests](sprint_E.4_tests.md) own outcomes; [handover](sprint_E.4_handover.md)
owns the Product Owner decision. Requirements/design remain in the linked SRS and
[sprint design](sprint_E.4_design.md).

## Current state and prerequisites

Release v1.0.7 is already deployed to E3_TARGET / app 810203 and safely repeated.
It is Available. B remains on e4-b with its original staged work. E4A/B/C are fixed
independent author services and E4I is a separate integration fixture; canonical
schema/workspace E1_DEV_C and app 810003 preserve native paths. The host has Oracle
Free 23.26.3, APEX 24.2 and ORDS 25.3. SQLcl must be exactly release 25.4.1.0/build
25.4.1.022.0618 for these Git states, with Java 21. Discover the repository root;
never treat .local-apex as authoritative configuration or credential storage.

Read-only handover inspection needs Git, gh, jq, unzip, Node.js, actionlint and `code`.
A new native replay additionally needs separately approved native connection stores
outside the checkout, effective schema/service verification, clean selected source,
qualified fixture baseline and a reserved target interval. Temporary central
E4_VERIFY/E4_SYNC access was removed. Obtain authorized access for a future live
write demonstration rather than reusing a dead profile or silently widening grants.
New-host provisioning is not supplied by this sprint. Fixture SQL is retained as
bounded experiment setup evidence; it is not an idempotent provisioning service.

## Ordinary author and manager journey

Each developer changes only its independent fixture, confirms Page Designer Save,
exports native source, reviews/commits src, stages against the immutable comparison
branch, verifies zero errors and commits dist. Developers do this before any release
admission. Native SQLcl's exit code alone does not prove verify passed.

The manager later branches from current accepted main and announces the branch name.
Developers choose whether to submit a PR to it; submission is not admission. Review
source, dependencies and current checks before each merge. Full-app exports can
conflict even for separate pages. Resolve selected intents in a separate native
integration fixture using consistent ID/export options, recapture/restage and run
fresh verification. Do not take one whole export and lose another contribution.

Promote the verified candidate to main, select the unused version through the checked
version PR, run native release, inspect/commit its numbered output, then tag and
package the clean frozen source. The installed artifact must exclude B in src,
distribution and ZIP, not merely omit a stage include. The current native APEX graph
uses one shared runOnChange installer; these feature stage files contain no schema
changes. No false database dependency is introduced for explanation.

## B's deferred continuation

Preserve ed9fe37bbebe30306ce91e981da9b5565b44c5c5 as original B provenance. When a later
release is announced and B chooses to join, update B against that branch, reconcile
A/C without overwriting them, reconstruct/refresh the author or integration fixture
through supported native imports when needed, inspect existing staged metadata and
freshly stage/verify. Submit a new release PR and obtain manager admission. Never
blindly duplicate old changesets, rewrite previously numbered history, or assume
an old clean stage qualifies newly combined bytes. B delivery was not performed now.

## Central synchronization and refusal

Bind a trusted baseline to target identity, last accepted archive/source, exact
export/checksum profile and actual availability. On first use without a trusted
checksum, privately compare complete live source against a native mapped reference
from the verified accepted archive. Unknown differences block; first checksum alone
never establishes authority. Keep every history/configuration field separately.

Before install, compare requested source/hash to the explicitly selected accepted
release and live checksum to the trusted final Available-state receipt. Refuse stale
source or pending work without deploying. Preserve diagnostics, edits, data and
prior receipt. Restore only a controlled test property. APEX's generated version
counter can still change the checksum: E.4's Product Owner approved a narrow complete-
diff counter-only recovery, not a general bypass. Any other difference requires review.

Reserve users/authors for the entire operation. Observe → restrict → observe → native
deploy → observe actual state → restrict again → check selected behavior and every
business field → publish → observe twice → finalize receipt. An import can restore
Available before re-restriction; this prototype does not technically deny all traffic
throughout. Repeat admission uses the finalized Available receipt. Status API calls
can change the checksum even when definitions are otherwise unchanged.

## Failure and recovery

Stop before writes for missing identity/access, wrong SQLcl build, stale source,
unknown baseline or pending definitions. A failed native operation requires observing
actual status/checksum, attempting the known supported restriction, retaining evidence
and maintaining coordinated exclusion. Never infer rollback, successful deployment
or persisted restriction from an error. Unknown partial state requires a reviewed
operator recovery decision. Do not reinstall the old archive to conceal pending work.

After success remove temporary access and private credential material according to
its scope, confirm Available, then release the reservation. Preserve B and all
retained data. Do not run broad scratch cleanup while the prepared-host credential
exception remains. The full archive, redacted receipts and native logs are in tests/;
raw business snapshots and private connection stores must not enter Git or slides.

## Limits and support boundary

This is a single-operator Elaboration experiment on a retained supported upgrade
path. There is no production fencing, automated admission service, broad schema
fingerprint, arbitrary fresh-install support or PBI-056 provisioning. The runtime
footer is static 1.0.0; release identity is the tag/source/archive receipt. Live
Product Owner acceptance remains pending, and Sprint E.4 remains Progress.
