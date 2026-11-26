# E.17 design

Status: Accepted under explicit YOLO delegation.

Use a new hosted Ubuntu runner and distinct technical account, with recorded uid, clean HOME and fresh private input provisioning. Reuse E.16 qualified native SQLcl 25.4.1.022.0618 and pinned Oracle image. Install checksum-pinned APEX 24.2 and pinned ORDS separately; never equate plain Oracle to APEX delivery. Preserve actual native logs and HTTP responses. Export a reviewed existing application fixture into a new workspace through supported APEX installation APIs. Keep experimental fixtures separate from production project metadata.

### Testing Strategy

SM-17 checks Python/workflow syntax. UT-17 verifies private-input rejection and receipt completeness. IT-17 must execute the fresh hosted journey, inspect authoritative terminal success and retained receipts, require actual application access, native installation/upgrade/repeat and data preservation, and verify cleanup. Full unfiltered smoke/unit/integration regression follows. Contract checks cannot establish real-host behavior.

## Test Specification

SM-17 requires clean-host source and valid workflow. UT-17 must reject absent private inputs and incomplete evidence. IT-17 requires fresh host and operator identity, declared prerequisite/tool identities, Database/APEX/ORDS provisioning, application access, native release lifecycle, preserved rows and scoped cleanup. P9 requires actual live increment demonstration plus readable rendered presentation and walkthrough. No missing acceptance observation is waived by YOLO.

## Verified resumption and native responsibilities

E.16 correction c7218cd was finalized and published to origin before resumption. Its companion 03f18caa0ff3f1bd5c1d75e280d5bf038f9996e9 supplies the native.yml named lifecycle and the one-invocation sql.sh adapter and validators. E.17 replaces the earlier unrun lifecycle.py invocation with those individual native Actions steps. Fresh provisioning and final application access surround that lifecycle. Earlier draft files are not execution evidence. Platform provisioning remains subject to source review and actual hosted execution; successful historical E.16 tests do not satisfy E.17.

## Application inspection fixture

The imported example is narrowed to APEX Accounts login and a native PL/SQL page that reads `preserved`, the exact table installed/upgraded by SQLcl PROJECT. This connects the HTTP/UI observation to retained deployment data without importing unrelated earlier component behavior. It is a fixture choice within PBI-085's clean-host experiment, not a claim of full production component delivery. Chromium logs in as a newly created LAB_USER and must render the retained row; a login page alone will not satisfy this chosen observation. Browser dependencies and runtime setup are explicit in Actions. The integration reader requires the actual authenticated receipt in addition to native data assertions.

The ORDS container's inspected image configuration declares user oracle and ORDS 25.3.0. The platform adapter explicitly runs it with the job user's uid/gid and HOME=/tmp so its mode-0700 job-private configuration mount remains writable. Noninteractive native ORDS install uses --proxy-user with fresh administrator and runtime passwords in stdin, following the accepted isolated regression's supported native invocation. No retained credential or new persistent store is introduced.

## Full regression remote boundary

The existing hosted Oracle regression defaults to its historical E.15 repository. E.17 adds HOSTED_ORACLE_REPO selection and uses rstyczynski/APEX_CICD_E.17 for dispatches, preserving the same fresh-run, real greeting, sentinel denial, denied publication and terminal-job assertions. The trusted E.17 baseline includes the already reviewed harmless greeting candidate for standalone regression dispatch. This routes new remote execution into the sprint repository without weakening or replaying a historical regression. E.16 immutable run reads remain read-only evidence verification.
