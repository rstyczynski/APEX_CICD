# E.18 observed failures

## BUG-18.1 — utPLSQL source directory ownership

Run 45844508366 replica 1 at f2be037 failed in Install pinned utPLSQL. The [actual installer log](tests/trial-45844508366-1/utplsql-install.log) reports SP2-0606 cannot create params.sql.tmp, subsequent missing-file SP2-0310 and ORA-01917 after an unintended EXIT substitution. Docker cp retained a directory not writable by the image's native oracle account. The installed native objects alone do not establish a successful installation.

Correction d878df0 adds an explicit root-owned chown to oracle:oinstall before invoking the vendor installer, retaining the native installer and its error gate. All initial trials were cancelled once the defect was identified; retained observations are diagnostic, excluded from performance results. Corrected real execution remains pending. No external blocker is claimed.
