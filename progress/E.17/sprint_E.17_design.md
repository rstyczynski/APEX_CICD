# E.17 design

Status: Accepted under explicit YOLO delegation.

Use a new hosted Ubuntu runner and distinct technical account, with recorded uid, clean HOME and fresh private input provisioning. Reuse E.16 qualified native SQLcl 25.4.1.022.0618 and pinned Oracle image. Install checksum-pinned APEX 24.2 and pinned ORDS separately; never equate plain Oracle to APEX delivery. Preserve actual native logs and HTTP responses. Export a reviewed existing application fixture into a new workspace through supported APEX installation APIs. Keep experimental fixtures separate from production project metadata.

### Testing Strategy

SM-17 checks Python/workflow syntax. UT-17 verifies private-input rejection and receipt completeness. IT-17 must execute the fresh hosted journey, inspect authoritative terminal success and retained receipts, require actual application access, native installation/upgrade/repeat and data preservation, and verify cleanup. Full unfiltered smoke/unit/integration regression follows. Contract checks cannot establish real-host behavior.

## Test Specification

SM-17 requires clean-host source and valid workflow. UT-17 must reject absent private inputs and incomplete evidence. IT-17 requires fresh host and operator identity, declared prerequisite/tool identities, Database/APEX/ORDS provisioning, application access, native release lifecycle, preserved rows and scoped cleanup. P9 requires actual live increment demonstration plus readable rendered presentation and walkthrough. No missing acceptance observation is waived by YOLO.
