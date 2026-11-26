# E.18 observed failures

[Implementation](sprint_E.18_implementation.md), [verification](sprint_E.18_tests.md) and the [gallery](screenshots/index.html) connect repairs to actual outcomes.

## BUG-18.1 — utPLSQL source directory ownership

Run 45844508366 replica 1 at f2be037 failed in Install pinned utPLSQL. The [actual installer log](tests/trial-45844508366-1/utplsql-install.log) reports SP2-0606 cannot create params.sql.tmp, subsequent missing-file SP2-0310 and ORA-01917 after an unintended EXIT substitution. Docker cp retained a directory not writable by the image's native oracle account. The installed native objects alone do not establish a successful installation.

Correction d878df0 adds an explicit root-owned chown to oracle:oinstall before invoking the vendor installer, retaining the native installer and its error gate. All initial trials were cancelled once the defect was identified; retained observations are diagnostic, excluded from performance results. Corrected real execution remains pending. No external blocker is claimed.

## BUG-18.2 — SYS cannot invoke an invoker-rights utPLSQL entry point

Corrected installer trial 45845314659 reaches Execute actual utPLSQL regression, then reports [ORA-06598](tests/trial-45845314659-1/utplsql-tests.log). This confirms that writable installer source alone does not establish usable tests. The original arithmetic fixture was also too narrow to represent the project backend workload; source 1470fb3 replaces it with the existing five-case Hello entry API suite. Source aea3a77 then invokes that suite as E5_TEST through a newly supplied private password rather than SYS. It does not grant inheritance of SYS privileges. The required report line includes zero failed and zero errored tests. All superseded trials are excluded; corrected real execution is pending.

## Supplemental QA correction — hostname assumption

A receipt audit initially required unique hostnames across serial samples. That condition is not an acceptance criterion, and one hostname repeats in two nonoverlapping jobs with distinct runner IDs. The [diagnostic](tests/cohort-identity-diagnostic.md) records the exact failed condition and correction. The [cohort audit](tests/cohort-isolation.log) now checks actual execution identity, source/run bindings, author/target namespaces and cleanup while preserving physical-host freshness as a limit. No required native behavior was weakened.

## Handover build recovery

Presentation revision 2 failed EEXIST because the strict finalizer refuses to overwrite its prior validation receipt. No invalid replacement was delivered. The builder now uses revision-specific output and receipt paths; revisions 3 and 4 validate successfully. The original failed log is retained as presentation-build-2.log. The native test copy serializes 17.26 as 17.260000000000002; comparison uses a disclosed 1e-12-minute serialization tolerance, not weakened workload criteria. The actual eight values and exact-seconds source remain unchanged.
