# E.18 implementation record

## Current execution

Dedicated repository: https://github.com/rstyczynski/APEX_CICD_E.18 at f2be037f2bbd6a3f8757954077e6c9c811f5d041. Maintained source is mirrored in [sprint-work/E.18](../../sprint-work/E.18/). [Design](sprint_E.18_design.md) owns measurement definitions and [checklist](sprint_E.18_checklist.md) tracks acceptance.

Cold serial run 45844508366, cold concurrent run 45844673934 and warm-cache population run 45844682312 are dispatched. All are pending. Population runs are excluded from warm measurements. Jobs run on independent hosted machines; concurrency here measures runner slots and batch completion, not competing databases on one host. Aggregate host counters include the runner and background services. Five-second sampling can miss short peaks. GitHub job start minus workflow creation combines scheduling, capacity queueing and deliberate serial admission; it does not isolate GitHub infrastructure queueing.

The observer records CPU counters, available memory and root-disk free space without collecting process command lines or credentials. Actions API step timestamps provide phase durations; native result files validate successful work. Download caches are verified by the original archive checksums on every use. Database images and utPLSQL source remain pinned. JDK retains E.17's major-version setup policy; exact installed build is a reported measurement input, not an invented immutable pin.

## Initial source checks

A1 source smoke and A2 arithmetic contracts pass 1/1 each. They establish syntax, named E.17 step retention and report arithmetic only. Native execution and cache-hit qualification remain pending. No production performance conclusion follows from these checks.

## UI capture recovery

The browser connector returned “The browser access host is unavailable”. Native Chrome control was available and used to inspect the real first trial. [Gallery](screenshots/index.html) preserves the starting window and framed copy. The failed connector did not block UI inspection.

## Corrected trials

After preserving the initial installer failure, source d878df0 dispatches corrected cold serial 45845297753, cold concurrent 45845306173 and cache population 45845314659. Initial exploratory trials preceded the persisted design specification and are not acceptance samples. The corrected trials follow that specification. The native installer log redacts its vendor-default schema password; job-generated private passwords remain masked.
