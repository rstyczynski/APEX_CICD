# E.17 design

Status: Accepted under explicit YOLO delegation.

Use a new hosted Ubuntu runner and distinct technical account, with recorded uid, clean HOME and fresh private input provisioning. Reuse E.16 qualified native SQLcl 25.4.1.022.0618 and pinned Oracle image. Install checksum-pinned APEX 24.2 and pinned ORDS separately; never equate plain Oracle to APEX delivery. Preserve actual native logs and HTTP responses. Export a reviewed existing application fixture into a new workspace through supported APEX installation APIs. Keep experimental fixtures separate from production project metadata.

### Testing Strategy

SM-17 checks Python/workflow syntax. UT-17 verifies private-input rejection and receipt completeness. IT-17 must execute the fresh hosted journey, inspect authoritative terminal success and retained receipts, require actual application access, native installation/upgrade/repeat and data preservation, and verify cleanup. Full unfiltered smoke/unit/integration regression follows. Contract checks cannot establish real-host behavior.

## Test Specification

SM-17 requires clean-host source and valid workflow. UT-17 must reject absent private inputs and incomplete evidence. IT-17 requires fresh host and operator identity, declared prerequisite/tool identities, Database/APEX/ORDS provisioning, application access, native release lifecycle, preserved rows and scoped cleanup. P9 requires actual live increment demonstration plus readable rendered presentation and walkthrough. No missing acceptance observation is waived by YOLO.

## Verified resumption and native responsibilities

E.16 correction c7218cd was finalized and published to origin before resumption. Its companion 03f18caa0ff3f1bd5c1d75e280d5bf038f9996e9 supplies the native.yml named lifecycle and the one-invocation sql.sh adapter and validators. E.17 replaces the earlier unrun lifecycle.py invocation with those individual native Actions steps. Fresh provisioning and final application access surround that lifecycle. Earlier draft files are not execution evidence. Platform provisioning remains subject to source review and actual hosted execution; successful historical E.16 tests do not satisfy E.17.
