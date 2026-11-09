# E.4 — Implementation record

## Scope and current state

The [approved handoff](sprint_E.4_implementation_handoff.md) and
[design](sprint_E.4_design.md) govern PBI-042/PBI-060. This is an Elaboration
experiment, performed by one Codex operator simulating A/B/C and Release Manager.
The native work uses three independent databases and concurrent processes; no
three-person team or simultaneous human editing is claimed. Native validation, required evidence gates, handover preparation and independent
review/recheck are complete. Live Product Owner acceptance remains pending. [Setup](sprint_E.4_setup.md) owns
analysis; [the audit](sprint_E.4_documentation_audit.md) owns reconciliation.

## Fixed author fixtures and capacity

E4A was created from PDB$SEED, with fresh APEX 24.2, accepted schema/application
source and literal synthetic Hello/World values. Only this new fixture was cloned
to E4B/E4C/E4I. Retained runtime data and the prepared-host credential record were
not copied. All authors use canonical E1_DEV_C, workspace 3069011249066219,
application 810003 and offset 3270698107083768; services and private connection
stores are separate. E4I is the integration fixture, not a shared author prerequisite.
FREEPDB1 / E3_TARGET / 810203 remains central DEV.

Oracle Free 23.26.3.0.0 and ORDS 25.3 run in the existing Podman VM (4 virtual CPUs,
6 GiB). Oracle reported 2 usable CPUs, 1.5 GiB SGA and 2 GiB PGA limit; initial
volume free space was 17 GB. The [parallel receipt](tests/parallel-contributions.json)
records approximately 24.84 seconds of overlapping overall author workers. The
individual native process receipts independently establish 14.757295 seconds of
three-way capture overlap and 4.155229 seconds of three-way stage/verify overlap.
The broader worker interval includes toolchain checks and Git work; it is not one
continuous SQLcl process interval.
This qualifies the fixed experiment, not PBI-056 provisioning or load capacity.

The first PDB administrator syntax was unsupported and failed before creation.
The corrected fixed fixture uses a new random password and locks that administrator.
ORDS installation initially lacked installer privileges: the vendor installer-grant
script, native removal of the partial new installation and native reinstall fixed
E4A. The temporary installer user was removed. An installer option briefly removed
the global database.api.enabled setting; it was restored to its retained true value.
No retained schema data was changed by these setup corrections.

Six native table snapshots initially differed in CHECK-constraint whitespace/order
although SQL semantics matched. The fixture constraints were restored from accepted
SXML text using [the guarded SQL](fixtures/restore-original-check-text.sql), then
fully recaptured. No snapshot was hand-edited. All three no-edit recaptures matched
the qualified baseline, including the reviewed fresh-instance comment difference.
The historical fresh PROJECT installation guard was neither bypassed nor modified.

## Toolchain and baseline

Every native invocation checked project sqlcl.version 25.4.1.0 and the actual
25.4.1.022.0618 executable build. The pinned ZIP SHA-256 is
b717d83aa1a7ada2ca38e7c8be5b369ea6a2f9f50c5fdb55e18d263b471ecab9.
Java 21 was used. Temporary connection inputs/stores are private OS-temporary
material; scratch contains checkouts/build evidence only. GitHub retains its own
explicit setup and environment secrets. No new persistent configuration authority
was placed in .local-apex.

The corrected seed main was 5e0ac11fb93955f3806f5b55f917eb0c36196864. Writable lab
main 1fb3bfceea536f77a24954219b7bbf1cad5566dd contained newer accepted Home text;
baseline PR #5 retained it and reconciled corrected native history. Native baseline
verify and GitHub checks passed. Its accepted merge
5a7655ffd3e6be92bcd88e9581612be17dc3059c is the common author start, not the later
release-branch creation rule.

## Independent contribution and selection

A added the Home header, B changed the Hello report label, and C changed the World
report label in separate Page Designer sessions. An initial automation attempt
changed DOM values without notifying Page Designer's model. Native export detected
missing changes, and execution stopped before commits/stages. Native keyboard input
and confirmed Save corrected that harness issue. Retained first-attempt logs are
failure evidence, not accepted authoring.

All three actual exports started around 12:35:31 UTC on 2026-11-09, followed by
source commits and independently staged/verified distribution commits. Each had
zero native errors and one explained APEX-only warning (no soft objects to order).
Original staged heads are A fdb755155dce91541404af43ecc7e02ff63e9275,
B ed9fe37bbebe30306ce91e981da9b5565b44c5c5 and
C 2c966891b0bfd06fbfeff3f0500501eeb7b69f22.

Later accepted context PR #7 advanced main to
a018a677653935200ff32eb9982f207a72bbd162. The manager created release-e4-candidate
there and announced [issue #8](https://github.com/rstyczynski/APEX_CICD_E3_LAB/issues/8).
A/C opted in through PRs #9/#10. B postponed without opening a release PR and keeps
its original branch/source/stage. Manager admission was a separate review after
checks, with no source dependency on B.

## Native conflict resolution

Merging admitted A into C produced real conflicts in full application SQL, native
snapshot XML and application YAML. Whole-side selection would lose intent. In E4I,
we imported A's full app and C's page 200 through native APIs, recaptured the combined
source, retained admitted distribution as the comparison and freshly staged it.

The first component import mixed PROJECT current IDs with original-ID component
export and failed an APEX foreign key in E4I. A trial with current IDs/zero offset
preserved component IDs but changed the default offset. The qualified resolution
instead used matching original-ID exports for A and C with canonical fixed offset.
Its complete source diff against admitted A contains only C's selected region label
and generated hash; canonical IDs and offset remain intact. No central import ran
in these fixture corrections. Fresh stage/verify passed; C's corrected PR check
run 42621680105 passed before admission. Promotion PR #11 passed checks and merged
at d97a417531f864b8efb1e36f51b516db760ee387.

APEX is a shared full-app runOnChange installer (INSTALL_810003, SQLCL-Generated).
The per-feature stage files are empty for these metadata-only changes; they are not
independent database migrations. The include graph retains accepted release 1.0.5,
shared apex/apex.changelog.xml, then the newly numbered release and next. There is no
invented A-to-C schema dependency. Generated YAML trailing whitespace is retained
as native output, not manually reformatted to satisfy git diff --check.

## Central DEV authorization and baseline

The target initially had only runtime LAB_USER and no Builder account. The Product
Owner explicitly authorized a temporary developer and reserved central DEV. Temporary
E4_VERIFY and proxy E4_SYNC were created for the bounded tests and removed after validation
(counts zero in the cleanup receipt). Retained users/passwords were not changed.

The actual accepted 1.0.5 archive hash
969c567c26d6b092230db9426c99078a1c91d0f2bf4f75e2478b7b68d2d43fcc was verified.
Its app was natively imported into separate E4I reference app 810203 using the known
central mapping, never reinstalled on central DEV. Complete original-ID exports
matched except exporter comment, instance comment and application version counter;
all are individually recorded in [the reconciliation](tests/initial-reconciliation.diff).
Raw exports/diffs and full business-field snapshots stay private.

The pre-baseline pending Home title blocked qualification and remained saved. After
restoring only that title, full reconciliation and two identical Available-state
reads established [the initial baseline](tests/trusted-initial-baseline.json).
The post-baseline title change similarly caused refusal with no deploy; all business
fields and the prior receipt remained intact. Restoring the title did not restore
the checksum: the complete diff contains only p_version_scn 6207684→6208968.
The Product Owner explicitly approved reviewed counter-only recovery. The
[recovery receipt](tests/trusted-recovered-baseline.json) preserves the old identity,
exact raw difference and two new identical reads. Unknown differences remain blocked;
no general checksum-normalization algorithm or silent rebaselining was introduced.

## Release, synchronization and repeat

The checked version PR #6 selected 1.0.7. Native release froze the numbered
distribution and its reviewed output was committed at
`e0f60ff5efc6905c3b6a4c0e7a7a79a6b0134b0c`. Clean-source packaging produced
[the published archive](tests/e3-1.0.7.zip), SHA-256
`27541bed6550c9f2dcfb36aeabd5e903bfe09a475fda0b0ec1972aa8ad9a1535`.
The annotated v1.0.7 tag and GitHub release bind that same source and artifact.

[PBI-060](../../BACKLOG.md#pbi-060-present-multi-developer-sqlcl-changes-in-one-release)
meets the approved selective experiment criterion: A/C and inherited main context
are present in source, distribution and artifact, while B's original branch remains
unchanged and unmerged. Its later release is documented, not performed.

[PBI-042](../../BACKLOG.md#pbi-042-synchronize-central-development-after-accepted-merges)
completed initial qualification, both pending-edit refusals, stale-candidate refusal,
native sync and safe repeat. First deploy ran one changeset with 22 previously
applied; repeat ran zero with 23 previously applied. Both preserved all fields in
seven retained business/configuration tables. First import restored Available;
restriction was reapplied before acceptance. The reserved no-user/no-author interval
was operational coordination, not continuous technical denial. Repeat stayed
Restricted after native deploy because no import ran.

Acceptance checked A/C, baseline Hello, no B, native readiness and verifier session
before publication. Two matching final Available-state reads finalized each receipt.
Status API calls advance counters too; a restricted checksum is not the next baseline.
The final checksum is `SH256:lC3Z66l3GpaopFf/fj5VddcsUPaC61O57kzlWFdj6SQ=`.
Full final export versus a mapped selected-archive reference differs only in exporter,
instance and generated version counter. Browser inspection confirmed the selected
result without creating business data. [Cleanup](tests/cleanup.json) removed the
temporary central developer/proxy and released the reservation with app Available.

The [test report](sprint_E.4_tests.md) distinguishes native observations from repeatable
evidence readers. The [handover](sprint_E.4_handover.md) and complete paired walkthrough/
editable presentation cover the journey and limitations. Independent review and live
Product Owner acceptance are separate from these implementation outcomes.
