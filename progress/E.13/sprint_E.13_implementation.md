# E.13 implementation

[Design](sprint_E.13_design.md) is implemented as an isolated real Oracle experiment in [foundation_bridge.py](../../tests/foundation_bridge.py). Existing [Foundation test functions](../../tests/integration/test_foundation.sh) and component/full manifests register its smoke, unit and integration checks. It reuses the E.12 SQL process boundary while redirecting all new experiment SQL/logs into this sprint. The retained application and existing E.12 driver are not changed.

## Behavior and decisions

PBI-082 is challenged before consumer migration: a savepoint protects paired canonical/detail writes when failure occurs after the first write. The caller catches the specific error and commits; an independent SQL assertion requires no partial row. A separate child session terminates with rollback after an uncommitted first write, and an independent session verifies recovery. This is actual Oracle transaction behavior, not a modeled failure result.

PBI-049 uses a new template/name collection entry point and retained arbitrary-text entry point. Two real sessions commit 80 Hello and 80 World calls while Hello alone uses templates. Read-back checks and a complete join compare rendered and structured data. The controlled registry routes Hello back to legacy after version 2 writes and retains historical greeting/settings. Early retirement rejects specifically because old callers remain. After both routes migrate, retirement disables legacy writes; both template consumers continue.

The registry, common rendered history and shared savepoint are implementation choices. These are retained prototype code, not approved production pipeline deployment or production caller discovery. Finite passing traffic establishes its sample only. No component maintenance windows or browser behavior are claimed.

## User documentation

[Walkthrough](sprint_E.13_increment_demo.md) provides complete SQL before invocation, prepared connection prerequisites, exact runnable commands, expected markers and input/output inspection. [Manual](user_manual.md) owns recovery and limits. No new passwords, saved connections or scratch configuration are created. Failed schemas/logs are retained for diagnosis. Unknown templates and post-retirement legacy calls deliberately fail with checked errors. [Test report](sprint_E.13_tests.md) owns final gate results; [checklist](sprint_E.13_remaining_work.md) owns acceptance mapping.
