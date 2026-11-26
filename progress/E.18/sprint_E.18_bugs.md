# E.18 observed failures

## BUG-18.1 — utPLSQL source directory ownership

Run 45844508366 replica 1 at f2be037 failed in Install pinned utPLSQL. The [actual installer log](tests/trial-45844508366-1/utplsql-install.log) reports SP2-0606 cannot create params.sql.tmp, subsequent missing-file SP2-0310 and ORA-01917 after an unintended EXIT substitution. Docker cp retained a directory not writable by the image's native oracle account. The installed native objects alone do not establish a successful installation.

Correction d878df0 adds an explicit root-owned chown to oracle:oinstall before invoking the vendor installer, retaining the native installer and its error gate. All initial trials were cancelled once the defect was identified; retained observations are diagnostic, excluded from performance results. Corrected real execution remains pending. No external blocker is claimed.

## BUG-18.2 — SYS cannot invoke an invoker-rights utPLSQL entry point

Corrected installer trial 45845314659 reaches Execute actual utPLSQL regression, then reports [ORA-06598](tests/trial-45845314659-1/utplsql-tests.log). This confirms that writable installer source alone does not establish usable tests. The original arithmetic fixture was also too narrow to represent the project backend workload; source 1470fb3 replaces it with the existing five-case Hello entry API suite. Source aea3a77 then invokes that suite as E5_TEST through a newly supplied private password rather than SYS. It does not grant inheritance of SYS privileges. The required report line includes zero failed and zero errored tests. All superseded trials are excluded; corrected real execution is pending.
