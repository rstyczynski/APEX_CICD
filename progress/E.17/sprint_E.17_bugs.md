# E.17 diagnostic failures

## Hosted disk exhaustion — folded into PBI-085

Run 45818534213 initialized both Oracle containers, then exhausted runner disk during provisioning. The worker itself failed with System.IO.IOException: No space left on device; normal job logs and artifacts were unavailable. Preserved the authoritative check annotation. Retry 45819313293 explicitly removed unused preinstalled hosted SDKs before pinned Docker startup and progressed past this failure. Scope is disposable hosted job capacity, not cleanup on the prepared laboratory host.

## APEX native error hidden by successful process exit — folded into PBI-085

Run 45819313293 recorded APEX prerequisite rejection: XDB INVALID, followed by ORA-20001. Native apexins returned zero, so the subsequent workspace step failed with PLS-00201 for the absent APEX API. The apparent successful installation step did not establish installation. Added explicit SQL-output error rejection, retained the raw output, and selected the same Oracle release's full image by immutable registry digest. Publisher [image details](https://github.com/gvenzl/oci-oracle-free/blob/main/ImageDetails.md) describe component removals in regular images and intact full installation. This is a supported image configuration choice within Oracle Database, not a replacement technology or waiver of the APEX prerequisite. Trial 45820349969 tests it; success is not yet claimed.

## Common-user password change from a PDB — folded into PBI-085

Run 45820349969 completes native APEX installation/configuration and application import, then ORDS preparation fails with ORA-65066 while attempting ALTER USER SYS in FREEPDB1. The ORDS installer was not yet invoked. Preserved the exact redacted native output and failed-step log. Replaced the statement with a newly generated PDB-local E17_ADMIN account and native DBA grant; the installer uses that account as in the existing isolated-regression procedure. Run 45822055484 was cancelled to avoid re-executing the known defective statement; 45822242040 tests the corrected immutable source. No external blocker is established.

## SQL*Plus statement boundary — folded into PBI-085

Run 45822242040 completes APEX setup/import but ORDS preparation returns ORA-03405 because CREATE USER and GRANT were placed on one SQL*Plus input line. The retained ords-admin-input.log contains the redacted statement and exact error. The installer itself was not invoked. Split those top-level SQL statements onto separate lines and dispatched 45824130390 at immutable companion 4d2488c. Source smoke passes; actual installer and end-to-end qualification remain pending.
